import concurrent.futures
import sys
import shutil
import plots
import utils
import os
import json
import numpy as np

global concurrent_count


def execute_simulation(
    N,
    particle_radius,
    particle_mass,
    domain_type,
    domain_radius,
    obstacle_radius,
    speed,
    t_max,
    repetition,
    root_dir="data",
):

    # Create a unique directory based on the parameters
    name = f"v-{speed}_it-{repetition}"
    unique_dir = f"{root_dir}/{name}"

    os.makedirs(unique_dir, exist_ok=True)

    global concurrent_count

    print(f"Running simulation, {name}")
    print(f"Left to run: {concurrent_count}")

    concurrent_count -= 1

    os.system(
        "java -jar target/event-driven-molecular-dynamics-1.0-SNAPSHOT-jar-with-dependencies.jar -obs fixed "
        + f"-out {unique_dir} -N {N} -r {particle_radius} -m {particle_mass} -v {speed} "
        + f"-t {t_max} -sz {domain_radius} -or {obstacle_radius} -d {domain_type} "
        + "> /dev/null"
    )

    print(f"Simulation {name} completed")

    return unique_dir


def execute_simulations(
    N,
    particle_radius,
    particle_mass,
    domain_type,
    domain_radius,
    obstacle_radius,
    speeds,
    t_max,
    repetitions,
    root_dir="data",
):
    # Create a thread pool for parallel execution
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        # Store futures for all simulation tasks
        futures = []

        global concurrent_count
        concurrent_count = len(speeds) * repetitions

        for v in speeds:
            for repetition in range(repetitions):
                # Submit the simulation task to the executor
                futures.append(
                    executor.submit(
                        execute_simulation,
                        N,
                        particle_radius,
                        particle_mass,
                        domain_type,
                        domain_radius,
                        obstacle_radius,
                        v,
                        t_max,
                        repetition,
                        root_dir + "/simulations",
                    )
                )

        results = []

        # Wait for all tasks to complete and parse the files
        futures = concurrent.futures.as_completed(futures)

        for future in futures:
            try:
                unique_dir = (
                    future.result()
                )  # Get the directory of the completed simulation

                # Parse the static and dynamic files from the simulation
                static_file = os.path.join(unique_dir, "static.txt")
                dynamic_file = os.path.join(unique_dir, "dynamic.txt")

                # Parse static and dynamic files
                parameters = utils.load_static_data(static_file)
                times, particle_data = utils.load_dynamic_data(dynamic_file)

                # TODO: analyze results
                collision_count = utils.get_collision_with_obstacle_count(
                    times, particle_data, obstacle_radius, particle_radius
                )
                first_collision_count = utils.get_first_collision_with_obstacle_count(
                    times, particle_data, obstacle_radius, particle_radius
                )

                # Append the parsed data to results
                results.append(
                    {
                        "parameters": parameters,
                        "collision_count": collision_count,
                        "first_collision_count": first_collision_count,
                    }
                )

            except Exception as e:
                print(f"An error occurred during simulation or parsing: {e}")

        # Delete root_dir/simulations
        shutil.rmtree(root_dir + "/simulations", ignore_errors=True)

        return results  # Return the parsed results


def plot_results(results, output_dir="data"):
    # Create a list of collision counts for speeds, ignore repetitions
    found_speeds = set()
    collision_counts_with_obstacle = []
    first_collision_counts_with_obstacle = []
    labels = []

    for result in results:
        parameters = result["parameters"]
        v = parameters["initial_velocity"]
        if v in found_speeds:
            continue

        found_speeds.add(v)
        collision_count = result["collision_count"]
        first_collision_count = result["first_collision_count"]

        collision_counts_with_obstacle.append(collision_count)
        first_collision_counts_with_obstacle.append(first_collision_count)
        labels.append(f"v={v} (m/s)")

    # Plot collision count vs time
    plots.plot_collision_with_obstacle_vs_time(
        collision_counts_with_obstacle,
        labels,
        "Collision count vs time",
        filename=f"{output_dir}/collision_count_vs_time.png",
    )

    plots.plot_collision_with_obstacle_vs_time(
        first_collision_counts_with_obstacle,
        labels,
        "First collision count vs time",
        filename=f"{output_dir}/first_collision_count_vs_time.png",
    )


if __name__ == "__main__":

    # If arg is generate, generate data
    # If arg is plot, plot data

    if len(sys.argv) < 2:
        print("Usage: python system_behaviour.py [generate|plot]")
        exit(1)

    if sys.argv[1] == "generate":

        N = 100
        particle_radius = 0.001
        particle_mass = 1

        domain_type = "circular"
        domain_radius = 0.1 / 2

        obstacle_radius = 0.005

        speeds = [1, 3, 6, 10]

        t_max = 5

        repetitions = 1

        results = execute_simulations(
            N,
            particle_radius,
            particle_mass,
            domain_type,
            domain_radius,
            obstacle_radius,
            speeds,
            t_max,
            repetitions,
            root_dir="data",
        )

        print("Dumping results")

        # Save as json
        with open("data/results.json", "w") as json_file:
            json.dump(results, json_file, indent=4)

    elif sys.argv[1] == "plot":
        # Read results from json_file
        with open("data/results.json", "r") as json_file:
            results = json.load(json_file)

            plot_results(results, output_dir="data")

    else:
        print("Usage: python system_behaviour.py [generate|plot]")
