import numpy as np
from numpy.typing import NDArray
from typing import List

def LJ_derivative(r: np.float64):
    return -12 * (1 / np.pow(r, 13) - 1 / np.pow(r, 7)) if r < 3 else 0

def compute_force_pairwise(point_1: List[NDArray[np.float64]], point_2: List[NDArray[np.float64]]):
    displacement_vector = np.array([point_2[0][0] - point_1[0][0], point_2[0][1] - point_1[0][1]])
    distance = np.linalg.norm(displacement_vector)
    displacement_vector_normalized = displacement_vector / np.linalg.norm(displacement_vector)
    energy = LJ_derivative(np.float64(distance))
    return displacement_vector_normalized * energy
    
def compute_force_total(point: List[NDArray[np.float64]], neighbor_cells) -> NDArray[np.float64]:
    total_force = np.array([0.0, 0.0])
    for i in range(len(neighbor_cells)):
        for j in range(len(neighbor_cells[0])):
            for lst in neighbor_cells[i][j]:   
                curr_point = lst[0]
                if not np.allclose(curr_point, point):
                    total_force += compute_force_pairwise(point, curr_point)
    return -0.5 * total_force

def update_cell(cell: List[List[NDArray[np.float64]]], force: NDArray[np.float64], time_step: float):
    for i in range(len(cell)):
        cell[i][1] += (force * time_step)
    for i in range(len(cell)):
        cell[i][0] += (cell[i][1] * time_step)
