"""
Finalmente considerar que el obstáculo es una partícula libre de masa M = 3 kg que
inicialmente está en reposo. Teniendo en cuenta que la velocidad inicial de las partículas pequeñas
es v0 = 1 m/s, calcular el desplazamiento cuadrático medio de la partícula grande como función del
tiempo. Luego realizar un ajuste lineal siguiendo las indicaciones del método mostrado en la clase
Teórica 0 para obtener el coeficiente de difusión (D). Describir con detalle como se eligen lostiempos en los cuales se calcula el DCM, dado que el estado del sistema fue guardado con pasos
temporales (dt) no uniformes debido a la inhomogeneidad de los eventos.
"""

import numpy as np
import utils
import plots
import sys


def calculate_big_particle_squared_dispacement(
    dynamic_file, particle_count, event_count, discrete_times
):
    with open(dynamic_file, "r") as file:
        lines = file.readlines()

    step = particle_count + 1  # 1x el tiempo otro x la big particle
    event_times = np.array([float(line.strip().split()[0]) for line in lines[::step]])

    # _, particles = utils.load_dynamic_data(dynamic_file, particle_count, event_count)
    # print(particles[:,-1:][:,:,0:2].reshape(event_count, 2))
    big_particle_data = np.array(
        [line.strip().split()[0:2] for line in lines[step - 1 :: step]], dtype=float
    )
    # print(big_particle_data)
    squared_displacements = []
    initial_pos = big_particle_data[0]

    for t in discrete_times:
        i = (np.abs(event_times - t)).argmin()
        pos = big_particle_data[i]

        squared_displacement = np.sum((pos - initial_pos) ** 2)
        squared_displacements.append(squared_displacement)

    return squared_displacements


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python dcm.py <plot|generate>")
        sys.exit(1)

    if sys.argv[1] == "generate":

        N = 200
        r = 0.001
        m = 1
        v = 1

        out = "data"

        t = 2

        domain = "circular"
        obs = "free"
        sz = 0.05
        o_m = 3
        o_r = 0.005

        all_displacements = []
        num_simulations = 10
        time_step = 0.02

        times = np.arange(0, t, time_step)

        for i in range(num_simulations):
            dir = utils.execute_simulation(
                N, r, m, domain, sz, o_r, v, t, i, 12, out, obs, o_m, 100
            )
            static_file = dir + "/static.txt"
            static_config = utils.load_static_data(static_file)
            snapshots_file = dir + "/snapshots.txt"
            displacement = calculate_big_particle_squared_dispacement(
                snapshots_file,
                static_config["particle_count"],
                static_config["event_count"],
                discrete_times=times,
            )
            all_displacements.append(displacement)

        all_displacements = np.array(all_displacements)

        mean_squared_displacement = np.mean(all_displacements, axis=0)
        std_squared_displacement = np.std(all_displacements, axis=0)

        np.savetxt("data/msd.txt", mean_squared_displacement)
        np.savetxt("data/std_msd.txt", std_squared_displacement)
        np.savetxt("data/times.txt", times)


        sys.exit(0)

    elif sys.argv[1] == "plot":

        mean_squared_displacement = np.loadtxt("data/msd.txt")
        std_squared_displacement = np.loadtxt("data/std_msd.txt")
        times = np.loadtxt("data/times.txt")



        plots.plot_msd(times, mean_squared_displacement, std_squared_displacement, "data/msd.png")


        # Stationary period from 0.5s, so we split up to 0.5
        non_stationary_period = 0.5

        mean_squared_displacement = mean_squared_displacement[times < non_stationary_period]
        std_squared_displacement = std_squared_displacement[times < non_stationary_period]
        times = times[times < non_stationary_period]

        # Range of diffusion coefficients (D values) to test
        D_values = np.linspace(0, 3e-3, 50)

        # Calculo error cuadratico
        se_values = []
        for D in D_values:

            # Linea de ajuste
            predicted_msd = 2 * D * times

            # Error cuadratico medio
            se = np.sum((mean_squared_displacement - predicted_msd) ** 2)
            se_values.append(se)

        mse_values = np.array(se_values)

        # Minimo error
        best_D_index = np.argmin(mse_values)
        best_D = D_values[best_D_index]

        
        best_fit_msd = 2 * best_D * times

        plots.plot_msd_with_fit(times, mean_squared_displacement, std_squared_displacement, best_fit_msd, "data/msd_fit.png")
        plots.plot_se_vs_D(D_values, mse_values, best_D, "data/mse_vs_D.png")

        sys.exit(0)

    else:
        print("Usage: python dcm.py <plot|generate>")
        sys.exit(1)
