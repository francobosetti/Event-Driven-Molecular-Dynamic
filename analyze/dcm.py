'''
Finalmente considerar que el obstáculo es una partícula libre de masa M = 3 kg que
inicialmente está en reposo. Teniendo en cuenta que la velocidad inicial de las partículas pequeñas
es v0 = 1 m/s, calcular el desplazamiento cuadrático medio de la partícula grande como función del
tiempo. Luego realizar un ajuste lineal siguiendo las indicaciones del método mostrado en la clase
Teórica 0 para obtener el coeficiente de difusión (D). Describir con detalle como se eligen lostiempos en los cuales se calcula el DCM, dado que el estado del sistema fue guardado con pasos
temporales (dt) no uniformes debido a la inhomogeneidad de los eventos.
'''

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

def get_big_particle_data(dynamic_file, particle_count):
    with open(dynamic_file, 'r') as file:
        lines = file.readlines()

    step = particle_count + 2 # 1x el tiempo otro x la big particle
    times = [line.strip().split()[0] for line in lines[::step]]
    '''print(f'times:\n{times}')
    print()'''
    big_particle_data = [(map(float, line.strip().split())) for line in lines[step-1::step]]
    '''print('particle_data:\n')
    for p in big_particle_data:
        x, y, vx, vy = p
        print(f'x: {x}')
        print(f'y: {y}')
        print(f'vx: {vx}')
        print(f'vy: {vy}')'''
    
    # time slices fijas (para poder hacer el promedio)
    # tomar evento mas cercano

    
import sys
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python dcm.py <directory>")
        sys.exit(1)
    
    static_file = sys.argv[1] + "/static.txt"
    dynamic_file = sys.argv[1] + "/dynamic.txt"
    static_config = load_static_data(static_file)
    get_big_particle_data(dynamic_file, static_config["particle_count"])
