import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


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


def add_intermediate_positions(time_steps, particle_data, steps_per_interval):
    """
    Add intermediate positions between time steps based on custom steps per interval.

    :param time_steps: List of original time steps (collisions).
    :param particle_data: List of particle positions and velocities for each time step.
    :param steps_per_interval: List of the number of intermediate steps to add for each interval.
    :return: New time steps and particle data with interpolated values.
    """
    new_time_steps = []
    new_particle_data = []

    for i in range(len(time_steps) - 1):
        # Current time step and next time step
        t0 = time_steps[i]
        t1 = time_steps[i + 1]
        delta_t = (t1 - t0) / (steps_per_interval[i] + 1)  # Divide time interval

        # Current and next particle positions
        current_positions = particle_data[i]
        next_positions = particle_data[i + 1]

        # Add the current time step and particle positions
        new_time_steps.append(t0)
        new_particle_data.append(current_positions)

        # Interpolate positions between t0 and t1 using MRU
        for k in range(1, steps_per_interval[i] + 1):
            interpolated_time = t0 + k * delta_t
            interpolated_positions = []

            for j in range(len(current_positions)):
                x0, y0, vx0, vy0 = current_positions[j]

                # Use MRU for x and y
                x_interp = x0 + vx0 * k * delta_t
                y_interp = y0 + vy0 * k * delta_t

                interpolated_positions.append((x_interp, y_interp, vx0, vy0))

            new_time_steps.append(interpolated_time)
            new_particle_data.append(interpolated_positions)

    # Append the final time step and positions
    new_time_steps.append(time_steps[-1])
    new_particle_data.append(particle_data[-1])

    return new_time_steps, new_particle_data


def calculate_steps_per_interval(time_steps, total_steps):
    """
    Calculate the number of steps to add between each time interval based on the total required steps.

    :param time_steps: List of time values (e.g., [t0, t1, t2, ...]).
    :param total_steps: Total number of required steps (including original time steps).
    :return: List of steps per interval.
    """
    num_intervals = len(time_steps) - 1
    total_steps_needed = total_steps - len(time_steps)

    # Calculate the length of each interval
    interval_lengths = np.diff(time_steps)

    # Calculate the proportion of steps for each interval based on its length
    total_time = sum(interval_lengths)
    proportional_steps = (interval_lengths / total_time) * total_steps_needed

    # Round the steps and ensure the total matches the required total
    steps_per_interval = np.floor(proportional_steps).astype(int)

    # Distribute any remaining steps (due to rounding) across the intervals
    remaining_steps = total_steps_needed - sum(steps_per_interval)

    for i in range(remaining_steps):
        steps_per_interval[i % num_intervals] += 1

    return steps_per_interval.tolist()


# Animation function
def update(frame, circles, particle_data):

    # print per 5% progress
    if len(particle_data) // 20 and frame % (len(particle_data) // 20) == 0:
        print(f"Progress: {frame / len(particle_data) * 100}")

    for i, circle in enumerate(circles):
        x, y, _, _ = particle_data[frame][i]
        circle.set_center((x, y))

    return circles


def animate_particles(static_config, dynamic_file, interpolate):
    # Load dynamic data
    time_steps, particle_data = load_dynamic_data(dynamic_file)

    if len(time_steps) < 5000 and interpolate:
        steps_per_interval = calculate_steps_per_interval(time_steps, 5000)
        time_steps, particle_data = add_intermediate_positions(
            time_steps, particle_data, steps_per_interval
        )

    # Set up figure and axis size (10, 10)
    fig, ax = plt.subplots(figsize=(10, 10))

    if static_config["domain_type"] == "circular":
        circle = plt.Circle(
            (0, 0), static_config["domain_radius"], color="black", fill=False
        )
        ax.add_artist(circle)
        ax.set_xlim(-static_config["domain_radius"], static_config["domain_radius"])
        ax.set_ylim(-static_config["domain_radius"], static_config["domain_radius"])
    else:
        ax.set_xlim(0, static_config["domain_radius"])
        ax.set_ylim(0, static_config["domain_radius"])

    # no ticks
    ax.set_xticks([])
    ax.set_yticks([])

    # Circles
    particle_radius = static_config["particle_radius"]

    circles = [
        plt.Circle((x, y), particle_radius, color="blue")
        for x, y, _, _ in particle_data[0]
    ]

    print("Creating animation...")

    for circle in circles:
        ax.add_artist(circle)

    ani = animation.FuncAnimation(
        fig,
        update,
        frames=len(time_steps),
        interval=30,
        fargs=(circles, particle_data),
        blit=True,
    )

    ani.save("data/particle_animation.mp4")


# Main
if __name__ == "__main__":
    static_file = "data/static.txt"
    dynamic_file = "data/dynamic.txt"

    static_config = load_static_data(static_file)
    animate_particles(static_config, dynamic_file, True)
