import matplotlib.pyplot as plt


def plot_collision_with_obstacle_vs_time(
    collision_counts, labels, text, filename="collision_with_obstacle_vs_time.png"
):

    fig, ax = plt.subplots()

    # Collision counts is a list of dict [time, count].
    # e.g. {0: 0, 1: 1, 2: 20}
    for i, collision_count in enumerate(collision_counts):
        times = list(collision_count.keys())

        # Times is string, convert to double
        times = [float(time) for time in times]

        counts = list(collision_count.values())

        ax.plot(times, counts, label=labels[i])

    ax.set_xlabel("Instante (s)")
    ax.set_ylabel("Colisiones")

    # 10 Ticks
    max_time = max(
        [
            max(map(float, collision_count.keys()))
            for collision_count in collision_counts
        ]
    )
    min_time = min(
        [
            min(map(float, collision_count.keys()))
            for collision_count in collision_counts
        ]
    )
    step = (max_time - min_time) / 4  # 9 intervals create 10 ticks
    steps = [round(min_time + i * step, 2) for i in range(5)]
    ax.set_xticks(steps)

    # Shrinks the plot by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    # Put a legend to the right of the current axis
    ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))

    # Add text above the legend box (surronded by a box)
    ax.text(
        1.05,
        0.8,
        text,
        transform=ax.transAxes,
        fontsize=12,
        verticalalignment="top",
        bbox=dict(facecolor="none", edgecolor="grey", boxstyle="round,pad=0.1"),
    )

    plt.savefig(filename)
    plt.close()


def plot_collided_particles_count_vs_time(
    collided_particles_count, labels, limit, text, filename="collided_particles_vs_time.png"
):

    fig, ax = plt.subplots()

    # Collision counts is a list of dict [time, count].
    # e.g. {0: 0, 1: 1, 2: 20}
    for i, collision_count in enumerate(collided_particles_count):
        times = list(collision_count.keys())

        # Times is string, convert to double
        times = [float(time) for time in times]

        counts = list(collision_count.values())

        ax.plot(times, counts, label=labels[i])

    ax.set_xlabel("Instante (s)")
    ax.set_ylabel("Particulas colisionadas")

    # 10 Ticks
    max_time = max(
        [
            max(map(float, collision_count.keys()))
            for collision_count in collided_particles_count
        ]
    )
    min_time = min(
        [
            min(map(float, collision_count.keys()))
            for collision_count in collided_particles_count
        ]
    )
    step = (max_time - min_time) / 4  # 9 intervals create 10 ticks
    steps = [round(min_time + i * step, 2) for i in range(5)]
    ax.set_xticks(steps)

    # add a horizontal line at y=limit
    ax.axhline(y=limit, color="r", linestyle="--")

    # Shrinks the plot by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    # Put a legend to the right of the current axis
    ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))

    # Add text above the legend box (surronded by a box)
    ax.text(
        1.05,
        0.8,
        text,
        transform=ax.transAxes,
        fontsize=12,
        verticalalignment="top",
        bbox=dict(facecolor="none", edgecolor="grey", boxstyle="round,pad=0.1"),
    )

    plt.savefig(filename)
    plt.close()


def plot_collision_slope_vs_temperature(
    mean_slopes, std_slopes, temperatures, text, filename="collision_slope_vs_temperature.png"
):

    fig, ax = plt.subplots()

    ax.errorbar(
        temperatures,
        mean_slopes,
        yerr=std_slopes,
        fmt="o",
        ecolor="black",
        capsize=5,
        elinewidth=1,
    )

    ax.set_xlabel("Temperatura (J)")
    ax.set_ylabel("Pendiente (colisiones / s)")

    # Add text above the legend box (surronded by a box)
    ax.text(
        0.8,
        0.17,
        text,
        transform=ax.transAxes,
        fontsize=12,
        verticalalignment="top",
        bbox=dict(facecolor="none", edgecolor="grey", boxstyle="round,pad=0.2"),
    )

    plt.savefig(filename)
    plt.close()


def plot_time_to_first_collision_vs_temperature(
    mean_times,
    std_times,
    temperatures,
    text,
    filename="time_to_first_collision_vs_temperature.png",
):

    fig, ax = plt.subplots()

    ax.errorbar(
        temperatures,
        mean_times,
        yerr=std_times,
        fmt="o",
        ecolor="black",
        capsize=5,
        elinewidth=1,
    )

    ax.set_xlabel("Temperatura (J)")
    ax.set_ylabel("Tiempo hasta 90% colisionadas (s)")

    # Add text above the legend box (surronded by a box)
    ax.text(
        0.8,
        0.97,
        text,
        transform=ax.transAxes,
        fontsize=12,
        verticalalignment="top",
        bbox=dict(facecolor="none", edgecolor="grey", boxstyle="round,pad=0.2"),
    )

    plt.savefig(filename)
    plt.close()
