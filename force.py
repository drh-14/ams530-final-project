import numpy as np
from numpy.typing import NDArray
from typing import List

def LJ_derivative(r: np.float64):
    return -12 * (1 / np.pow(r, 13) - 1 / np.pow(r, 7)) if r < 3 else 0

def compute_force_pairwise(point_1: List[NDArray[np.float64]], point_2: List[NDArray[np.float64]]):
    displacement_vector = point_2[0] - point_1[0]
    distance = np.linalg.norm(displacement_vector)
    inv_r = 1.0 / distance
    displacement_vector_normalized = inv_r * displacement_vector
    return displacement_vector_normalized * LJ_derivative(np.float64(distance))
    
def compute_force_total(particle: List[NDArray[np.float64]], neighbor_cells) -> NDArray[np.float64]:
    total_force = np.zeros(2)
    for cell in neighbor_cells:
        for other_point in cell:
            if not np.allclose(particle[0], other_point[0]):
                total_force += compute_force_pairwise(particle, other_point)
    return -total_force

def update_particle(particle: List[NDArray[np.float64]], force: NDArray[np.float64], time_step: float):
    particle[1] += (time_step * force)
    particle[0] += (time_step * particle[1])
