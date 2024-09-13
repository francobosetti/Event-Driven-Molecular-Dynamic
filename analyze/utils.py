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


def get_collision_with_obstacle_count(times, particle_data, obstacle_radius, particle_radius):
    
    epsilon = 1e-6

    # Map of time to collision count

    collision_count = {}

    count = 0

    # From 1 to len(times) - 1
    for i in range(1, len(times)):

        collisions = []

        for (_, _, vx1, vy1), (x2, y2, vx2, vy2) in zip(particle_data[i], particle_data[i - 1]):
            
            # There is a collision if particle speed changes in the next time step
            if vx1 != vx2 or vy1 != vy2:
                collisions.append((x2, y2))

        # If there are two collisions in the same time step
        # Skip as it is between two particles
        if len(collisions) != 1:
            continue

        x, y = collisions[0]

        # Check if the collision is with the obstacle
        if math.sqrt(x ** 2 + y ** 2) <= obstacle_radius + particle_radius + epsilon:
            count += 1

        collision_count[times[i]] = count

    return collision_count

def get_first_collision_with_obstacle_count(times, particle_data, obstacle_radius, particle_radius):
    
    epsilon = 1e-6

    # Map of time to collision count

    already_collided_particles = set()

    collision_count = {}

    count = 0

    # From 1 to len(times) - 1
    for i in range(1, len(times)):

        collisions = []

        for particle_id, ((_, _, vx1, vy1), (x2, y2, vx2, vy2)) in enumerate(zip(particle_data[i], particle_data[i - 1])):
            
            # There is a collision if particle speed changes in the next time step
            if vx1 != vx2 or vy1 != vy2:
                collisions.append((particle_id, (x2, y2)))

        # If there are two collisions in the same time step
        # Skip as it is between two particles
        if len(collisions) != 1:
            continue

        particle_id, (x, y) = collisions[0]

        if particle_id in already_collided_particles:
            continue

        already_collided_particles.add(particle_id)

        # Check if the collision is with the obstacle
        if math.sqrt(x ** 2 + y ** 2) <= obstacle_radius + particle_radius + epsilon:
            count += 1

        collision_count[times[i]] = count

    return collision_count

        



            
            


            
