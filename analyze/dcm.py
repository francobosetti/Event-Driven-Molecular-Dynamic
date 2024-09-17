'''
Finalmente considerar que el obstáculo es una partícula libre de masa M = 3 kg que
inicialmente está en reposo. Teniendo en cuenta que la velocidad inicial de las partículas pequeñas
es v0 = 1 m/s, calcular el desplazamiento cuadrático medio de la partícula grande como función del
tiempo. Luego realizar un ajuste lineal siguiendo las indicaciones del método mostrado en la clase
Teórica 0 para obtener el coeficiente de difusión (D). Describir con detalle como se eligen lostiempos en los cuales se calcula el DCM, dado que el estado del sistema fue guardado con pasos
temporales (dt) no uniformes debido a la inhomogeneidad de los eventos.
'''
import numpy as np
import utils
import matplotlib.pyplot as plt

def calculate_big_particle_squared_dispacement(dynamic_file, particle_count, event_count, discrete_times):
    with open(dynamic_file, 'r') as file:
        lines = file.readlines()

    step = particle_count + 1 # 1x el tiempo otro x la big particle
    event_times = np.array([float(line.strip().split()[0]) for line in lines[::step]])

    #_, particles = utils.load_dynamic_data(dynamic_file, particle_count, event_count)
    #print(particles[:,-1:][:,:,0:2].reshape(event_count, 2))
    big_particle_data = np.array([line.strip().split()[0:2] for line in lines[step-1::step]], dtype=float)
    #print(big_particle_data)
    squared_displacements = []
    initial_pos = big_particle_data[0]

    for t in discrete_times:
        i = (np.abs(event_times - t)).argmin()
        pos = big_particle_data[i]

        squared_displacement = np.sum((pos - initial_pos) **2)
        squared_displacements.append(squared_displacement)
    
    return squared_displacements

        
if __name__ == "__main__":
#    if len(sys.argv) != 2:
#        print("Usage: python dcm.py <directory>")
#        sys.exit(1)
    
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
    time_step = 0.01

    times = np.arange(0, t, time_step)

    for i in range(num_simulations):
        dir = utils.execute_simulation(N, r, m, domain, sz, o_r, v, t, i, 12, out, obs, o_m, 100)
        static_file = dir + "/static.txt"
        static_config = utils.load_static_data(static_file)
        dynamic_file = dir + "/dynamic.txt"
        displacement = calculate_big_particle_squared_dispacement(dynamic_file, static_config["particle_count"], static_config["event_count"], discrete_times=times)
        all_displacements.append(displacement)
    
    
    all_displacements = np.array(all_displacements)

    mean_squared_displacement = np.mean(all_displacements, axis=0)
    

    plt.figure(figsize=(8, 6))
    plt.plot(times, mean_squared_displacement, marker='o', linestyle='-', color='b')
    plt.xlabel('Time (s)')
    plt.ylabel('Mean Squared Displacement (MSD)')
    plt.title('Mean Squared Displacement (MSD) of the Big Particle Over Time')
    plt.grid(True)
    plt.show()