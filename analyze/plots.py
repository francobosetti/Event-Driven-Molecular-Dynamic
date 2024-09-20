import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm


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

    ax.set_xlabel("Tiempo (s)")
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

    ax.set_xlabel("Tiempo (s)")
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
    ax.set_ylabel("Frecuencia (colisiones / s)")

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
        times, mean_squared_displacement, std_squared_displacement, non_stationary_period, filename="data/msd.png"
):
    plt.figure(figsize=(8, 6))
    plt.errorbar(
        times,
        mean_squared_displacement,
        yerr=std_squared_displacement,
        fmt="o",
        capsize=5,
    )
    plt.axvline(non_stationary_period, color="r", linestyle="--")
    plt.xlabel("Tiempo (s)")
    plt.ylabel("<z$^2$> (m$^2$)")
    plt.ticklabel_format(style="sci", axis="y", scilimits=(0, 0))
    plt.grid(True)
    plt.savefig(filename)
    plt.close()


def plot_msd_with_fit(
        times,
        mean_squared_displacement,
        std_squared_displacement,
        best_fit_msd,
        best_d,
        filename="data/msd_fit.png",
):
    plt.figure(figsize=(8, 6))
    plt.errorbar(
        times,
        mean_squared_displacement,
        yerr=std_squared_displacement,
        fmt="o",
        capsize=5,
        label="<z$^2$> observado",
    )
    plt.plot(times, best_fit_msd, "r-", label=f"Ajuste Lineal, D = {best_d:.1e} m$^2$/s")
    plt.xlabel("Tiempo (s)")
    plt.ylabel("<z$^2$> (m$^2$)")
    plt.legend()
    plt.grid(True)
    plt.ticklabel_format(style="sci", axis="y", scilimits=(0, 0))
    plt.savefig(filename)
    plt.close()


def plot_se_vs_D(D_values, mse_values, best_D, filename="data/mse_vs_D.png"):
    plt.figure(figsize=(8, 6))
    plt.plot(D_values, mse_values, marker="o", linestyle="-")

    # Mejor D
    plt.axvline(best_D, color="r", linestyle="--", label=f"Mejor D = {best_D:.1e} m$^2$/s")

    plt.xlabel(r"$D$ (m$^2$/s)")
    plt.ylabel("Error cuadrático (m$^2$)")

    plt.ticklabel_format(style="sci", axis="y", scilimits=(0, 0))
    plt.ticklabel_format(style="sci", axis="x", scilimits=(0, 0))

    plt.legend()

    plt.grid(True)

    plt.savefig(filename)


def plot_pressure_vs_time(
        wall_pressures: list[list[float]],
        obstacle_pressures: list[list[float]],
        speed_labels: list[str],
        parameter_text: str,
        time_slot_duration: float,
        filename: str
):
    # Number of time steps
    num_timesteps = len(wall_pressures[0])
    time = np.arange(0, num_timesteps * time_slot_duration, time_slot_duration)

    if len(wall_pressures[0]) != len(time):
        time = time[:-1]
    
    # Number of speed groups
    num_speeds = len(wall_pressures)
    
    # Use a colormap with more contrast
    cmap = cm.get_cmap('Paired')  # Use Set1 for higher contrast

    plt.figure(figsize=(10, 6))

    # Store line objects for custom grouped legends by speed
    lines = []
    labels = []

    
    for i in range(num_speeds):

        if "v=10.0 (m/s)" in speed_labels:
            light_color = cmap(2 * i + 4)
            dark_color = cmap(2 * i + 5)
        else:
            # Darker color for wall pressure
            light_color = cmap(2*i)
            dark_color = cmap(2*i + 1)

        # Plot inner pressure
        inner_line, = plt.plot(time, obstacle_pressures[i], label=f"{speed_labels[i]} Obs.", color=light_color, linewidth=2)
        # Plot wall pressure
        wall_line, = plt.plot(time, wall_pressures[i], label=f"{speed_labels[i]} Pared", color=dark_color, linewidth=2)

        lines.append(inner_line)
        lines.append(wall_line)

        labels.append(f"{speed_labels[i]} Obs.")
        labels.append(f"{speed_labels[i]} Pared")



    
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Presión (N/m)')
    plt.grid(True)

    plt.ticklabel_format(style="sci", axis="y", scilimits=(0, 0))


    # Add text above the legend box (surronded by a box)

    ax = plt.gca()

    # Shrinks the plot by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    ax.text(
        1.05,
        0.85,
        parameter_text,
        transform=ax.transAxes,
        fontsize=12,
        verticalalignment="top",
        bbox=dict(facecolor="none", edgecolor="grey", boxstyle="round,pad=0.1"),
    )
    # Custom grouped legend by speed, combining wall and inner pressures
    plt.legend(lines[::-1], labels[::-1], loc='center left', bbox_to_anchor=(1, 0.5))

    # Save the figure to file
    plt.savefig(filename)
    plt.close()

def plot_pressure_vs_temperature(
        mean_pressures,
        std_pressures,
        temperatures,
        text,
        filename="pressure_vs_temperature.png",
):
    fig, ax = plt.subplots()

    ax.errorbar(
        temperatures,
        mean_pressures,
        yerr=std_pressures,
        fmt="o",
        ecolor="black",
        capsize=5,
        elinewidth=1,
    )

    ax.set_xlabel("Temperatura (J)")
    ax.set_ylabel("Presión (N/m)")

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


