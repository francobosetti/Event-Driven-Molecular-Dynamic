import concurrent.futures
import sys
import shutil
import plots
import utils
import os
import subprocess
import json
import numpy as np


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
    memory_gigs,
    root_dir="data",
):

    # Create a unique directory based on the parameters
    name = f"v-{speed}_it-{repetition}"
    unique_dir = os.path.join(root_dir, name)

    os.makedirs(unique_dir, exist_ok=True)

    # Build the command
    command = [
        "java",
        f"-Xmx{memory_gigs}G",  # Maximum heap size
        f"-Xms{memory_gigs}G",  # Initial heap size
        "-jar",
        "target/event-driven-molecular-dynamics-1.0-SNAPSHOT-jar-with-dependencies.jar",
        "-obs",
        "fixed",
        "-out",
        unique_dir,
        "-N",
        str(N),
        "-r",
        str(particle_radius),
        "-m",
        str(particle_mass),
        "-v",
        str(speed),
        "-t",
        str(t_max),
        "-sz",
        str(domain_radius),
        "-or",
        str(obstacle_radius),
        "-d",
        str(domain_type),
        "-sk",
        "100000000",
    ]

    try:
        print(f"Running simulation with speed {speed}, repetition {repetition}")
        subprocess.run(command, check=True, capture_output=True, text=True)
        print(
            f"Simulation completed successfully for speed {speed}, repetition {repetition}"
        )
    except subprocess.CalledProcessError as e:
        print(f"Simulation failed for speed {speed}, repetition {repetition}")
        print(f"Error Output: {e.stderr}")
        raise e

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
    is_concurrent=True,
    max_workers=4,
):

    available_memory = 12
    memory_per_simulation = (
        available_memory if not is_concurrent else int(available_memory / max_workers)
    )

    def submit_simulation(v, repetition):
        """Helper function to submit or execute simulation"""
        return execute_simulation(
            N,
            particle_radius,
            particle_mass,
            domain_type,
            domain_radius,
            obstacle_radius,
            v,
            t_max,
            repetition,
            memory_per_simulation,
            os.path.join(root_dir, "simulations"),
        )

    remaining_simulations = len(speeds) * repetitions
    dirs = []

    if is_concurrent:
        print(
            f"Executing {remaining_simulations} simulations concurrently, with {max_workers} workers"
        )
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [
                executor.submit(submit_simulation, v, repetition)
                for v in speeds
                for repetition in range(repetitions)
            ]
            # Collect the directories from the futures
            for future in concurrent.futures.as_completed(futures):
                try:
                    dir = future.result()
                    dirs.append(dir)
                    remaining_simulations -= 1
                except Exception as e:
                    print(f"An error occurred during simulation: {e}")

    else:
        print(f"Executing {remaining_simulations} simulations")
        for v in speeds:
            for repetition in range(repetitions):
                try:
                    dir = submit_simulation(v, repetition)
                    dirs.append(dir)
                    remaining_simulations -= 1
                    print(
                        f"Completed simulation on {dir}, {remaining_simulations} remaining"
                    )
                except Exception as e:
                    print(f"An error occurred during simulation: {e}")

    results = []

    remaining_simulations = len(dirs)
    print(f"Processing {remaining_simulations} simulations")

    for unique_dir in dirs:
        try:

            print(f"Reading simulation on {unique_dir}")
            # Parse the static and dynamic files from the simulation
            static_file = os.path.join(unique_dir, "static.txt")
            dynamic_file = os.path.join(unique_dir, "dynamic.txt")

            # Parse static and dynamic files
            parameters = utils.load_static_data(static_file)
            times, particle_data = utils.load_dynamic_data(
                dynamic_file, parameters["particle_count"], parameters["event_count"]
            )

            print(f"Analyzing simulation on {unique_dir}")
            # TODO: analyze results
            collision_count = utils.get_collision_with_obstacle_count(
                times, particle_data, obstacle_radius, particle_radius
            )
            first_collision_count = utils.get_first_collision_with_obstacle_count(
                times, particle_data, obstacle_radius, particle_radius
            )
            temperature = utils.get_system_temperature(
                particle_data, parameters["particle_mass"]
            )

            print(f"Collision count: {max(collision_count.values())}")

            # 5 digits of precision
            temperature = round(temperature, 5)

            # Append the parsed data to results
            results.append(
                {
                    "parameters": parameters,
                    "collision_count": collision_count,
                    "first_collision_count": first_collision_count,
                    "temperature": temperature,
                }
            )

            remaining_simulations -= 1
            print(
                f"Processed simulation on {unique_dir}, {remaining_simulations} remaining"
            )

        except Exception as e:
            print(f"An error occurred during processing: {e}")

    # Delete root_dir/simulations
    try:
        print("Cleaning up")
        shutil.rmtree(root_dir + "/simulations", ignore_errors=True)
    except Exception as e:
        print(f"An error occurred during cleanup: {e}")

    return results  # Return the parsed results


def plot_results(results, output_dir="data"):
    # Create a list of collision counts for speeds, ignore repetitions
    found_speeds = set()
    collision_counts_with_obstacle = []
    first_collision_counts_with_obstacle = []
    labels = []

    # Dict of t -> list of slope
    slopes = {}
    # Dict of t -> time to all collisions
    time_to_all_collisions = {}

    N = results[0]["parameters"]["particle_count"]
    first_collision_limit = N * 0.9
    particle_radius = results[0]["parameters"]["particle_radius"]
    particle_mass = results[0]["parameters"]["particle_mass"]

    for result in results:
        parameters = result["parameters"]
        v = parameters["initial_velocity"]

        collision_count = result["collision_count"]
        first_collision_count = result["first_collision_count"]

        # Collision counts is a list of dict [time, count].
        # Calculate the slope of the collision count
        times = [float(time) for time in collision_count.keys()]
        counts = list(collision_count.values())

        # Calculate the slope of the collision count
        slope = np.polyfit(times, counts, 1)[0]
        temperature = result["temperature"]

        # Time to all collisions
        max_time = max(first_collision_count.keys())
        if first_collision_count[max_time] < first_collision_limit:
            print(
                f"Simulation did not complete for v={v}, t={max_time}, count={first_collision_count[max_time]}"
            )

        if temperature not in slopes:
            slopes[temperature] = []
        slopes[temperature].append(slope)

        if temperature not in time_to_all_collisions:
            time_to_all_collisions[temperature] = []
        time_to_all_collisions[temperature].append(float(max_time))

        if v in found_speeds:
            continue

        found_speeds.add(v)

        collision_counts_with_obstacle.append(collision_count)
        first_collision_counts_with_obstacle.append(first_collision_count)
        labels.append(f"v={v} (m/s)")

    mean_slopes = []
    std_slopes = []

    for temperature, slope in slopes.items():
        mean_slopes.append(np.mean(slope))
        std_slopes.append(np.std(slope))

    temperatures = list(slopes.keys())

    # N, r, and m
    text = f"N={N}\nr={particle_radius} m\nm={particle_mass} kg"

    # Plot collision slope vs temperature
    plots.plot_collision_slope_vs_temperature(
        mean_slopes,
        std_slopes,
        temperatures,
        text,
        filename=f"{output_dir}/collision_slope_vs_temperature.png",
    )

    mean_times = []
    std_times = []

    for temperature, times in time_to_all_collisions.items():
        mean_times.append(np.mean(times))
        std_times.append(np.std(times))

    temperatures = list(time_to_all_collisions.keys())

    # Plot time to first collision vs temperature
    plots.plot_time_to_first_collision_vs_temperature(
        mean_times,
        std_times,
        temperatures,
        text,
        filename=f"{output_dir}/time_to_first_collision_vs_temperature.png",
    )

    # Plot collision count vs time
    plots.plot_collision_with_obstacle_vs_time(
        collision_counts_with_obstacle,
        labels,
        text,
        filename=f"{output_dir}/collision_count_vs_time.png",
    )

    plots.plot_collided_particles_count_vs_time(
        first_collision_counts_with_obstacle,
        labels,
        first_collision_limit,
        text,
        filename=f"{output_dir}/collided_particles_count_vs_time.png",
    )


if __name__ == "__main__":

    # If arg is generate, generate data
    # If arg is plot, plot data

    if len(sys.argv) < 2:
        print("Usage: python system_behaviour.py <generate|plot> [concurrent_workers] ")
        exit(1)

    if sys.argv[1] == "generate":

        N = 200
        particle_radius = 0.001
        particle_mass = 1

        domain_type = "circular"
        domain_radius = 0.1 / 2

        obstacle_radius = 0.005

        speeds = [1, 3, 6, 10]

        t_max = 3

        repetitions = 10

        is_concurrent = True if len(sys.argv) == 3 else False
        workers = int(sys.argv[2]) if is_concurrent else 4

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
            is_concurrent=is_concurrent,
            max_workers=workers,
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
        print("Usage: python analyze.py <generate|plot> [concurrent_workers] ")
