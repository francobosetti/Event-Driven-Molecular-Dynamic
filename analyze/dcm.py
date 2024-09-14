'''
Finalmente considerar que el obstáculo es una partícula libre de masa M = 3 kg que
inicialmente está en reposo. Teniendo en cuenta que la velocidad inicial de las partículas pequeñas
es v0 = 1 m/s, calcular el desplazamiento cuadrático medio de la partícula grande como función del
tiempo. Luego realizar un ajuste lineal siguiendo las indicaciones del método mostrado en la clase
Teórica 0 para obtener el coeficiente de difusión (D). Describir con detalle como se eligen lostiempos en los cuales se calcula el DCM, dado que el estado del sistema fue guardado con pasos
temporales (dt) no uniformes debido a la inhomogeneidad de los eventos.
'''
import numpy as np

def find_closest_time(times, t):
    return (np.abs(times - t)).argmin()

def get_big_particle_data(dynamic_file, particle_count, time_increment):
    with open(dynamic_file, 'r') as file:
        lines = file.readlines()

    step = particle_count + 1 # 1x el tiempo otro x la big particle
    times = [float(line.strip().split()[0]) for line in lines[::step]]

    big_particle_data = np.array([line.strip().split()[0:2] for line in lines[step-1::step]], dtype=float)

    squared_displacements = []
    initial_pos = big_particle_data[0]
    max_time = times[-1]

    for t in np.arange(0, max_time, time_increment):
        i = find_closest_time(times, t)
        pos = big_particle_data[i]

        squared_displacement = np.sum((pos - initial_pos) **2)
        squared_displacements.append(squared_displacement)
    
    print(squared_displacements)

    
    # time slices fijas (para poder hacer el promedio)
    # tomar evento mas cercano

    
import sys
import utils
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python dcm.py <directory>")
        sys.exit(1)
    
    static_file = sys.argv[1] + "/static.txt"
    dynamic_file = sys.argv[1] + "/dynamic.txt"
    static_config = utils.load_static_data(static_file)
    get_big_particle_data(dynamic_file, static_config["particle_count"], 0.1)
