import math
import os
import subprocess

# Load static configuration
def load_static_data(static_file):
    with open(static_file, "r") as file:
        particle_count = int(file.readline().strip())
        particle_radius = float(file.readline().strip())
        particle_mass = float(file.readline().strip())
        initial_velocity = float(file.readline().strip())

        domain_type = file.readline().strip()
        if domain_type == "circular":
            domain_radius = float(file.readline().strip())
        else:
            domain_side = float(file.readline().strip())

        obstacle_type = file.readline().strip()
        obstacle_radius = float(file.readline().strip())
        if obstacle_type == "free":
            obstacle_mass = float(file.readline().strip())
        else:
            obstacle_mass = None
        snapshot_count = int(file.readline().strip())
        event_count = int(file.readline().strip())

    return {
        "particle_count": particle_count,
        "particle_radius": particle_radius,
        "particle_mass": particle_mass,
        "initial_velocity": initial_velocity,
        "domain_type": domain_type,
        "domain_radius": domain_radius if domain_type == "circular" else domain_side,
        "obstacle_type": obstacle_type,
        "obstacle_radius": obstacle_radius,
        "obstacle_mass": obstacle_mass,
        "snapshot_count": snapshot_count,
        "event_count": event_count,
    }


import numpy as np


# Load dynamic data
def load_snapshot_data(snapshots_file, particle_count, snapshot_count):

    # Preallocate the 3D array: (num_time_steps, num_particles, 4)
    snapshots = np.zeros((snapshot_count, particle_count, 4), dtype=np.float64)
    times = np.zeros(snapshot_count, dtype=np.float64)

    # Fill the preallocated arrays
    with open(snapshots_file, "r") as file:
        current_time_step = -1
        current_particle = 0

        for line in file:
            parts = line.strip().split()

            if len(parts) == 1:  # New time step
                current_time_step += 1
                current_particle = 0
                times[current_time_step] = float(parts[0])
            else:
                snapshots[current_time_step, current_particle] = list(map(float, parts))
                current_particle += 1

    return times, snapshots


# Loads events from the events file
def load_event_data(events_file, event_count):
    events = np.zeros((event_count, 3), dtype=object)
    times = np.zeros(event_count, dtype=np.float64)

    with open(events_file, "r") as file:
        for i, line in enumerate(file):
            parts = line.strip().split()

            times[i] = float(parts[0])

            event_type = parts[1]
            particle_id = int(parts[2])
            event_data = list(map(float, parts[3:]))

            events[i] = (event_type, particle_id, event_data)


    return times, events


def get_collisions_with_obstacle(times, events):

    collision_times = {}

    for time, (event_type, particle_id, event_data) in zip(times, events):
        if event_type == "O":
            x, y, vx1, vy1, vx2, vy2 = event_data
            collision_times[time] = (particle_id, ((x, y, vx1, vy1, vx2, vy2)))

    return collision_times


def get_collision_with_wall(times, events):
    collision_times = {}

    for time, (event_type, particle_id, event_data) in zip(times, events):
        if event_type == "W":
            x, y, vx1, vy1, vx2, vy2 = event_data
            collision_times[time] = (particle_id, ((x, y, vx1, vy1, vx2, vy2)))

    return collision_times


def get_collision_with_obstacle_count(
    times, events
):

    collisions = get_collisions_with_obstacle(
        times, events
    )

    collision_count = {}
    count = 0

    for time, _ in collisions.items():
        count += 1
        collision_count[time] = count

    return collision_count


def get_first_collision_with_obstacle_count(
    times, events
):

    collisions = get_collisions_with_obstacle(
        times, events
    )

    collision_count = {}
    already_collided = set()
    count = 0

    for time, (id, _) in collisions.items():
        if id in already_collided:
            continue

        count += 1
        collision_count[time] = count
        already_collided.add(id)

    return collision_count


def get_system_temperature(particle_data, particle_mass):

    # All collisions are elastic, so the energy is conserved
    velocities = particle_data[0]
    particle_count = len(velocities)

    kinetic_energy = 0

    for _, _, vx, vy in velocities:
        kinetic_energy += 0.5 * particle_mass * (vx**2 + vy**2)

    return kinetic_energy / particle_count


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
    obstacle="fixed",
    om=3,
    skip=100000000,
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
        str(obstacle),
        "-om",
        str(om),
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
        str(skip)
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

def get_system_pressure(times, events, domain_radius, time_slot_duration, particle_mass):    
    collisions_obstacle = get_collisions_with_obstacle(times, events)
    collisions_wall = get_collision_with_wall(times, events)

    obstacle_momentums = [0]
    wall_momentums = [0]

    # Calculate the momentum of the particles that collide with the obstacle, dividing them into groups of time_slot_duration
    current_time_slot = 0
    for time, (_, ((x, y, vx1, vy1, _, _))) in collisions_obstacle.items():
        if time > current_time_slot * time_slot_duration:
            obstacle_momentums[current_time_slot] /= time_slot_duration * 2 * math.pi * domain_radius
            current_time_slot += 1
            obstacle_momentums.append(0)

        # get normal component
        normal = (x / math.sqrt(x ** 2 + y ** 2), y / math.sqrt(x ** 2 + y ** 2))

        v1_normal = vx1 * normal[0] + vy1 * normal[1]

        obstacle_momentums[current_time_slot] += 2 * v1_normal * particle_mass

    obstacle_momentums[current_time_slot] /= time_slot_duration * 2 * math.pi * domain_radius

    # Calculate the momentum of the particles that collide with the wall, dividing them into groups of time_slot_duration
    current_time_slot = 0
    for time, (_, ((x, y, vx1, vy1, _, _))) in collisions_wall.items():
        if time > current_time_slot * time_slot_duration:
            wall_momentums[current_time_slot] /= time_slot_duration * 2 * math.pi * domain_radius
            current_time_slot += 1
            wall_momentums.append(0)

        # get normal component
        normal = (x / math.sqrt(x ** 2 + y ** 2), y / math.sqrt(x ** 2 + y ** 2))

        v1_normal = vx1 * normal[0] + vy1 * normal[1]

        wall_momentums[current_time_slot] += 2 * v1_normal * particle_mass

    wall_momentums[current_time_slot] /= time_slot_duration * 2 * math.pi * domain_radius

    return obstacle_momentums, wall_momentums
    
