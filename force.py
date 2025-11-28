import numpy as np

def LJ_derivative(r):
    return -12 * (1 / np.pow(r, 13) - 1 / np.pow(r, 7))

def compute_force_pairwise(point_1, point_2):
    displacement_vector = np.array([point_2[0] - point_1[0], point_2[1], point_1[1]])
    distance = np.linalg.norm(displacement_vector)
    displacement_vector_normalized = displacement_vector / np.linalg.norm(displacement_vector)
    energy = LJ_derivative(distance)
    return displacement_vector_normalized * energy
    
def compute_force_total(point, points):
    return -0.5 * np.sum([compute_force_pairwise(point, x) for x in points if point != x])  
