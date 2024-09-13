
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
