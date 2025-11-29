import numpy as np

def LJ_derivative(r):
    return -12 * (1 / np.pow(r, 13) - 1 / np.pow(r, 7))

def compute_force_pairwise(point_1, point_2):
    displacement_vector = np.array([point_2[0] - point_1[0], point_2[1] - point_1[1]])
    distance = np.linalg.norm(displacement_vector)
    displacement_vector_normalized = displacement_vector / np.linalg.norm(displacement_vector)
    energy = LJ_derivative(distance)
    return displacement_vector_normalized * energy
    
def compute_force_total(point, points):
    total_force = np.array([0.0, 0.0])
    for i in range(len(points)):
        for j in range(len(points[0])):
            for lst in points[i][j]:   
                curr_point = lst[0]
                if curr_point != point:
                    total_force += compute_force_pairwise(point, curr_point)
    return -0.5 * total_force
