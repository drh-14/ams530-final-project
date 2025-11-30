import numpy as np
from numpy.typing import NDArray
from typing import List, Tuple

def LJ_derivative(r: np.float64):
    return -12 * (1 / np.pow(r, 13) - 1 / np.pow(r, 7)) if r < 3 else 0

def compute_force_pairwise(point_1: NDArray[np.float64], point_2: NDArray[np.float64]):
    displacement_vector = np.array([point_2[0] - point_1[0], point_2[1] - point_1[1]])
    distance = np.linalg.norm(displacement_vector)
    displacement_vector_normalized = displacement_vector / np.linalg.norm(displacement_vector)
    energy = LJ_derivative(np.float64(distance))
    return displacement_vector_normalized * energy
    
def compute_force_total(point: NDArray[np.float64], grid: List[List[List[Tuple[NDArray[np.float64], NDArray[np.float64]]]]]):
    total_force = np.array([0.0, 0.0])
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            for lst in grid[i][j]:   
                curr_point = lst[0]
                if not np.allclose(curr_point, point):
                    total_force += compute_force_pairwise(point, curr_point)
    return -0.5 * total_force
