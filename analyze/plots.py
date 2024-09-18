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
        collided_particles_count,
        labels,
        limit,
        text,
        filename="collided_particles_vs_time.png",
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
        mean_slopes,
        std_slopes,
        temperatures,
        text,
        filename="collision_slope_vs_temperature.png",
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


def plot_msd(
        times, mean_squared_displacement, std_squared_displacement, filename="data/msd.png"
):
    plt.figure(figsize=(8, 6))
    plt.errorbar(
        times,
        mean_squared_displacement,
        yerr=std_squared_displacement,
        fmt="o",
        capsize=5,
    )
    plt.xlabel("Instante (s)")
    plt.ylabel("MSD (m$^2$)")
    plt.ticklabel_format(style="sci", axis="y", scilimits=(0, 0))
    plt.grid(True)
    plt.savefig(filename)
    plt.close()


def plot_msd_with_fit(
        times,
        mean_squared_displacement,
        std_squared_displacement,
        best_fit_msd,
        filename="data/msd_fit.png",
):
    plt.figure(figsize=(8, 6))
    plt.errorbar(
        times,
        mean_squared_displacement,
        yerr=std_squared_displacement,
        fmt="o",
        capsize=5,
        label="MSD promedio observado",
    )
    plt.plot(times, best_fit_msd, "r-", label=f"y = 4 * D * t")
    plt.xlabel("Instante (s)")
    plt.ylabel("MSD (m$^2$)")
    plt.legend()
    plt.grid(True)
    plt.ticklabel_format(style="sci", axis="y", scilimits=(0, 0))
    plt.savefig(filename)
    plt.close()


def plot_se_vs_D(D_values, mse_values, best_D, filename="data/mse_vs_D.png"):
    plt.figure(figsize=(8, 6))
    plt.plot(D_values, mse_values, marker="o", linestyle="-")

    # Mejor D
    plt.axvline(best_D, color="r", linestyle="--", label=f"Best D = {best_D:.3e} m^2/s")

    plt.xlabel(r"$D$ (m$^2$/s)")
    plt.ylabel("Error cuadrático")

    plt.ticklabel_format(style="sci", axis="y", scilimits=(0, 0))
    plt.ticklabel_format(style="sci", axis="x", scilimits=(0, 0))

    plt.grid(True)

    plt.savefig(filename)


def plot_pressure_vs_time(
        wall_pressures: list[list[float]],
        obstacle_pressures: list[list[float]],
        speed_labels,
        parameter_text,
        time_slot_duration: float,
        filename
):
    # Each pressure value is separated by time_slot_duration
    # Plot in the same graph the pressures of the wall and the obstacle. Each list of floats corresponds to the same parameters
    # If I have 3 sets of parameters, there will be 3 lists in wall_pressures and 3 lists in obstacle_pressures
    # The time will be the same for all the sets of parameters, and it will be calculated as time_slot_duration * i for each i in range(len(wall_pressure))
    # If there are 3 sets of parameters, 3 plots need to be outputed. Each plot will contain the pressures of the wall and the obstacle for the same set of parameters
    # The x axis will be the time, and the y axis will be the pressure

    for i in range(len(wall_pressures)):
        fig, ax = plt.subplots()

        times = [time_slot_duration * i for i in range(len(wall_pressures[i]))]

        ax.plot(times, wall_pressures[i], label="Pared")
        ax.plot(times, obstacle_pressures[i], label="Obstáculo")

        ax.set_xlabel("Tiempo (s)")
        ax.set_ylabel("Presión (N/m)")

        # 10 Ticks
        max_time = max(times)
        min_time = min(times)
        step = (max_time - min_time) / 4
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
            parameter_text + f"\n{speed_labels[i]}",
            transform=ax.transAxes,
            fontsize=12,
            verticalalignment="top",
            bbox=dict(facecolor="none", edgecolor="grey", boxstyle="round,pad=0.1"),
        )

        plt.savefig(f"{filename}_{i}.png")
        plt.close()
