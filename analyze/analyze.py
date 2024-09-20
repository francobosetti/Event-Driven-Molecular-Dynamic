import concurrent.futures
import sys
import shutil
import plots
import utils
import os
import subprocess
import json
import numpy as np


def execute_simulations(
    N,
    particle_radius,
    particle_mass,
    domain_type,
    domain_radius,
    obstacle_radius,
    speeds,
    t_max,
    time_slot_duration,
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
        return utils.execute_simulation(
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
            snapshots_file = os.path.join(unique_dir, "snapshots.txt")
            events_file = os.path.join(unique_dir, "events.txt")

            # Parse static and dynamic files
            parameters = utils.load_static_data(static_file)
            event_times, events = utils.load_event_data(
                events_file, parameters["event_count"]
            )
            snapshot_times, snapshots = utils.load_snapshot_data(
                snapshots_file,
                parameters["particle_count"],
                parameters["snapshot_count"],
            )

            obstacle_collision_times = utils.get_collisions_with_obstacle(
                event_times, events, t_max
            )

            obstacle_collision_times = list(obstacle_collision_times.keys())

            wall_collision_times = utils.get_collision_with_wall(
                event_times, events, t_max
            )

            wall_collision_times = list(wall_collision_times.keys())

            wall_collision_frequency = len(wall_collision_times) / max(
                wall_collision_times
            )
            obstacle_collision_frequency = len(obstacle_collision_times) / max(
                obstacle_collision_times
            )

            ratio = wall_collision_frequency / obstacle_collision_frequency

            print(f"Wall collision frequency / Obstacle collision frequency: {ratio}")

            print(f"Analyzing simulation on {unique_dir}")
            # TODO: analyze results
            collision_count = utils.get_collision_with_obstacle_count(
                event_times, events, t_max
            )
            first_collision_count = utils.get_first_collision_with_obstacle_count(
                event_times, events, t_max
            )

            obstacle_pressures, wall_pressures = utils.get_system_pressure(
                event_times,
                events,
                domain_radius,
                obstacle_radius,
                time_slot_duration,
                particle_mass,
                t_max,
            )

            temperature = utils.get_system_temperature(
                snapshots, parameters["particle_mass"]
            )

            # 5 digits of precision
            temperature = round(temperature, 5)

            # Append the parsed data to results
            results.append(
                {
                    "parameters": parameters,
                    "collision_count": collision_count,
                    "first_collision_count": first_collision_count,
                    "temperature": temperature,
                    "obstacle_pressures": obstacle_pressures,
                    "wall_pressures": wall_pressures,
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


def plot_results(results, time_slot_duration, output_dir="data"):
    # Create a list of collision counts for speeds, ignore repetitions
    found_speeds = set()
    collision_counts_with_obstacle = []
    first_collision_counts_with_obstacle = []
    labels = []

    # Dict of t -> list of slope
    slopes = {}
    # Dict of t -> time to all collisions
    time_to_all_collisions = {}
    # Dict of t -> list of mean pressures
    mean_pressures = {}
    std_pressures = {}

    obstacle_pressures = []
    wall_pressures = []

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

        if temperature not in slopes:
            slopes[temperature] = []
        slopes[temperature].append(slope)

        if temperature not in time_to_all_collisions:
            time_to_all_collisions[temperature] = []

        time_to_limit = 0
        for time, count in first_collision_count.items():
            if count == first_collision_limit:
                time_to_limit = float(time)
                break

        if time_to_limit == 0:
            print(f"Could not find time to limit for v={v}")

        time_to_all_collisions[temperature].append(time_to_limit)

        system_pressures = [
            (wall_pressure + obstacle_pressure) / 2
            for wall_pressure, obstacle_pressure in zip(
                result["wall_pressures"][1:], result["obstacle_pressures"][1:]
            )
        ]

        wall_pressure = np.mean(result["wall_pressures"])
        obstacle_pressure = np.mean(result["obstacle_pressures"])
        print(
            f"Wall mean pressure: {wall_pressure}, Obstacle mean pressure: {obstacle_pressure}, Ratio: {wall_pressure / obstacle_pressure if obstacle_pressure != 0 else 0}"
        )


        mean_pressure = np.mean(system_pressures)
        std_pressure = np.std(system_pressures)

        if temperature not in mean_pressures:
            mean_pressures[temperature] = []
            std_pressures[temperature] = []

        mean_pressures[temperature].append(mean_pressure)
        std_pressures[temperature].append(std_pressure)

        if v in found_speeds:
            continue

        found_speeds.add(v)

        collision_counts_with_obstacle.append(collision_count)
        first_collision_counts_with_obstacle.append(first_collision_count)
        labels.append(f"v={v} (m/s)")

        obstacle_pressures.append(result["obstacle_pressures"])
        wall_pressures.append(result["wall_pressures"])

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

    labels_1_3 = [label for label in labels if label == "v=3.0 (m/s)" or label == "v=1.0 (m/s)"]
    wall_pressure_1_3 = [ wall_pressures[i] for i, label in enumerate(labels) if label == "v=3.0 (m/s)" or label == "v=1.0 (m/s)"]
    obstacle_pressure_1_3 = [ obstacle_pressures[i] for i, label in enumerate(labels) if label == "v=3.0 (m/s)" or label == "v=1.0 (m/s)"]

    labels_6_10 = [label for label in labels if label == "v=6.0 (m/s)" or label == "v=10.0 (m/s)"]
    wall_pressure_6_10 = [ wall_pressures[i] for i, label in enumerate(labels) if label == "v=6.0 (m/s)" or label == "v=10.0 (m/s)"]
    obstacle_pressure_6_10 = [ obstacle_pressures[i] for i, label in enumerate(labels) if label == "v=6.0 (m/s)" or label == "v=10.0 (m/s)"]

    plots.plot_pressure_vs_time(
        wall_pressure_1_3,
        obstacle_pressure_1_3,
        labels_1_3,
        text,
        time_slot_duration=time_slot_duration,
        filename=f"{output_dir}/wall_and_obstacle_pressures_vs_time_1_3.png",
    )

    plots.plot_pressure_vs_time(
        wall_pressure_6_10,
        obstacle_pressure_6_10,
        labels_6_10,
        text,
        time_slot_duration=time_slot_duration,
        filename=f"{output_dir}/wall_and_obstacle_pressures_vs_time_6_10.png",
    )

    plots.plot_pressure_vs_time(
        wall_pressures,
        obstacle_pressures,
        labels,
        text,
        time_slot_duration=time_slot_duration,
        filename=f"{output_dir}/wall_and_obstacle_pressures_vs_time.png",
    )


    mean_mean_pressures = []
    std_mean_pressures = []

    for temperature, pressures, std_pressures in zip(
        mean_pressures.keys(),
        mean_pressures.values(),
        std_pressures.values(),
    ):
        mean_total_pressure = np.mean(pressures)

        std_total_pressure = 0
        for mean_pressure, std_pressure in zip(pressures, std_pressures):
            std_total_pressure += (
                std_pressure**2 + (mean_pressure - mean_total_pressure) ** 2
            )

        std_total_pressure /= len(pressures)
        std_total_pressure = np.sqrt(std_total_pressure)

        mean_mean_pressures.append(mean_total_pressure)
        std_mean_pressures.append(std_total_pressure)


    # Plot mean pressure vs temperature
    plots.plot_pressure_vs_temperature(
        mean_mean_pressures,
        std_mean_pressures,
        temperatures,
        text,
        filename=f"{output_dir}/mean_pressure_vs_temperature.png",
    )


if __name__ == "__main__":

    # If arg is generate, generate data
    # If arg is plot, plot data

    if len(sys.argv) < 2:
        print("Usage: python system_behaviour.py <generate|plot> [concurrent_workers] ")
        exit(1)

    time_slot_duration = 0.01

    if sys.argv[1] == "generate":

        N = 200
        particle_radius = 0.001
        particle_mass = 1

        domain_type = "circular"
        domain_radius = 0.05

        obstacle_radius = 0.005

        speeds = [1, 3, 6, 10]

        t_max = 10

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
            time_slot_duration,
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

            plot_results(results, time_slot_duration, output_dir="data")

    else:
        print("Usage: python analyze.py <generate|plot> [concurrent_workers] ")
