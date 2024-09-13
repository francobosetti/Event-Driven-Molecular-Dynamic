import matplotlib.pyplot as plt

def plot_collision_with_obstacle_vs_time(collision_counts, labels, text, filename="collision_with_obstacle_vs_time.png"):

    fig, ax = plt.subplots()



    # Collision counts is a list of dict [time, count].
    # e.g. {0: 0, 1: 1, 2: 20}
    for i, collision_count in enumerate(collision_counts):
        times = list(collision_count.keys())

        # Times is string, convert to double
        times = [float(time) for time in times]

        counts = list(collision_count.values())

        ax.plot(times, counts, label=labels[i])

    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Collision count")

    # Ticks every 10 %
    max_times = [max(collision_count.keys()) for collision_count in collision_counts]
    max_time = float(max(max_times))
    step = max_time / 10
    steps = [i * step for i in range(11)]
    ax.set_xticks(steps)

    # Shrinks the plot by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    # Put a legend to the right of the current axis
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))


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


