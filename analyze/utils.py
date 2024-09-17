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
        "event_count": event_count,
    }

import numpy as np

# Load dynamic data
def load_dynamic_data(dynamic_file, num_particles, num_time_steps):
    

    # Preallocate the 3D array: (num_time_steps, num_particles, 4)
    particle_data = np.zeros((num_time_steps, num_particles, 4), dtype=np.float64)
    times = np.zeros(num_time_steps, dtype=np.float64)

    # Second pass: fill the preallocated arrays
    with open(dynamic_file, "r") as file:
        current_time_step = -1
        current_particle = 0

        for line in file:
            parts = line.strip().split()

            if len(parts) == 1:  # New time step
                current_time_step += 1
                current_particle = 0
                times[current_time_step] = float(parts[0])
            else:
                particle_data[current_time_step, current_particle] = list(map(float, parts))
                current_particle += 1

    return times, particle_data

def get_one_particle_collisions(times, particle_data):
    collision_times = {}

    # Particle velocities in each time step
    vels_t1 = particle_data[:-1, :, 2:]  # velocities at time t1 (vx1, vy1)
    vels_t2 = particle_data[1:, :, 2:]   # velocities at time t2 (vx2, vy2)

    # Boolean array where True indicates a change in velocity, i.e., a collision
    velocity_change = np.any(vels_t1 != vels_t2, axis=2)

    for i, changes in enumerate(velocity_change):
        # Get indices of particles with velocity change
        colliding_particles = np.where(changes)[0]

        # Skip if no collision or more than one particle collides (as it implies a multi-particle collision)
        if len(colliding_particles) != 1:
            continue

        particle_id = colliding_particles[0]
        x1, y1, vx1, vy1 = particle_data[i, particle_id]
        x2, y2, vx2, vy2 = particle_data[i + 1, particle_id]

        collision_times[times[i + 1]] = (particle_id, ((x1, y1, vx1, vy1), (x2, y2, vx2, vy2)))

    return collision_times

# Returns a dict [time, (id, ((x1, y1, vx1, vy1), (x2, y2, vx2, vy2)))]
def get_one_particle_collisions_slow(
    times, particle_data
):

    collision_times = {}

    # From 1 to len(times) - 1
    for i in range(1, len(times)):

        collisions = []

        for particle_id, ((x1, y1, vx1, vy1), (x2, y2, vx2, vy2)) in enumerate(
            zip(particle_data[i - 1], particle_data[i])
        ):

            # There is a collision if particle speed changes in the next time step
            if vx1 != vx2 or vy1 != vy2:
                collisions.append(
                    (particle_id, ((x1, y1, vx1, vy1), (x2, y2, vx2, vy2)))
                )

        # If there are two collisions in the same time step
        # Skip as it is between two particles
        if len(collisions) != 1:
            continue

        collision = collisions[0]

        collision_times[times[i]] = collision


    return collision_times

def get_collisions_with_obstacle(
    times, particle_data, obstacle_radius, particle_radius
):

    epsilon = 1e-5
    
    collisions = get_one_particle_collisions(times, particle_data)

    collisions_with_obstacle = {}

    for time, (id, ((x1, y1, vx1, vy1), (x2, y2, vx2, vy2))) in collisions.items():

        center_to_center_distance = math.sqrt(x2 ** 2 + y2 ** 2)
        distance_to_obstacle = abs(center_to_center_distance - (obstacle_radius + particle_radius))

        if distance_to_obstacle <= epsilon:
            collisions_with_obstacle[time] = (id, ((x1, y1, vx1, vy1), (x2, y2, vx2, vy2)))

    return collisions_with_obstacle

def get_collision_with_wall(times, particle_data, domain_radius, particle_radius):

    epsilon = 1e-5

    collisions = get_one_particle_collisions(times, particle_data)

    wall_collisions = {}

    for time, (id, ((x1, y1, vx1, vy1), (x2, y2, vx2, vy2))) in collisions.items():

        center_to_center_distance = math.sqrt(x2 ** 2 + y2 ** 2)
        distance_to_wall = abs(domain_radius - (center_to_center_distance + particle_radius))

        if distance_to_wall <= epsilon:
            wall_collisions[time] = (id, ((x1, y1, vx1, vy1), (x2, y2, vx2, vy2)))

    return wall_collisions


def get_collision_with_obstacle_count(
    times, particle_data, obstacle_radius, particle_radius
):

    collisions = get_collisions_with_obstacle(
        times, particle_data, obstacle_radius, particle_radius
    )

    collision_count = {}
    count = 0

    for time, _ in collisions.items():
        count += 1
        collision_count[time] = count

    return collision_count


def get_first_collision_with_obstacle_count(
    times, particle_data, obstacle_radius, particle_radius
):

    collisions = get_collisions_with_obstacle(
        times, particle_data, obstacle_radius, particle_radius
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
        kinetic_energy += 0.5 * particle_mass * (vx ** 2 + vy ** 2)

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
    obstacle = "fixed",
    om = 3,
    skip = 100000000
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
