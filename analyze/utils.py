import math


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
    }


# Load dynamic data
def load_dynamic_data(dynamic_file):
    with open(dynamic_file, "r") as file:
        lines = file.readlines()

    times = []
    particle_data = []

    current_time = None
    current_particles = []

    for line in lines:
        parts = line.strip().split()

        if len(parts) == 1:  # New time step
            if current_time is not None:
                times.append(current_time)
                particle_data.append(current_particles)
            current_time = float(parts[0])
            current_particles = []
        else:
            x, y, vx, vy = map(float, parts)
            current_particles.append((x, y, vx, vy))

    # Append the last time step
    if current_time is not None:
        times.append(current_time)
        particle_data.append(current_particles)

    return times, particle_data

# Returns a dict [time, (id, ((x1, y1, vx1, vy1), (x2, y2, vx2, vy2)))]
def get_one_particle_collisions(
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

