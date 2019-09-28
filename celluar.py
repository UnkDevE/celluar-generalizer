import cellpylib as cpl
import sys

def rot(n, rot_x, rot_y, x, y):
    if rot_y == 0:
        if rot_x == 1:
            x = (n - 1) - x
            y = (n - 1) - y
    x, y = y, x
    return [x, y]

def n_to_point(n, dimension):
    pos = [0, 0]
    rot_x = n
    rot_y = n
    inter = n
    for s in range(1, dimension):
        s *= 2 
        rot_x = 1 & (inter//2)
        rot_y = 1 & (inter ^ rot_x)
        pos = rot(s, rot_x, rot_y, pos[0], pos[1])
        pos[0] += s * rot_x
        pos[1] += s * rot_y
        inter //= 4
    return pos

def point_to_n(dimension, point):
    rot_x = 0
    rot_y = 0 
    sol = 0

    for s in range(0, dimension // 2):
        s //= 2
        rot_x = (point[0] & s) > 0
        rot_y = (point[1] & s) > 0
        sol += s * s * ((3 * rot_x) ^ rot_y)
        point = rot(dimension, rot_x, rot_y, x, y)

    return sol

def byte_to_point(byte):
    return n_to_point(byte, 3)

def file_to_points(filename):
    binary_file = open(filename, "rb")
    byte_list = list(binary_file.read())
    binary_file.close()
    return [byte_to_point(byte) for byte in byte_list]

def add_points(points, automata):
    for point in points:
        automata[:, [point[0]], [point[1]]] = 1
    return automata

def points_to_bin(points):
    byte_list = []
    for point in points:
        byte_list.append(point_to_n(3, point))

    return byte_list

def compare_bytes(bytes_a, bytes_b):
    return len(set(bytes_a).intersection(bytes_b)) / len(bytes_a)

def main():
    test = False
    train_points = []
    test_points = []

    for arg in sys.argv:
        if arg == "-t":
           test = True
        if test:
           test_points.append(file_to_points(arg))
        else:
            train_points.append(file_to_points(arg))
    
    automata = cpl.init_simple2d(8, 8)
    for points in train_points:
        add_points(points, automata) 
        automata = cpl.evolve(automata, timesteps=100, neighbroughood='Moore',
                apply_rule=cpl.game_of_life_rule)
        
    
    for test_point in test_points: 
        test_automata = cpl.init_simple2d(8, 8)
        add_points(test_point, test_automata)
        test_automata = cpl.evolve(test_automata, timesteps=100, neighbroughood='Moore',
            apply_rule=cpl.game_of_life_rule)
        print(compare_bytes(automata, test_automata)
         

if __name__ == "__main__" :
    main()


    
        

