import numpy as np
from numpy.typing import NDArray
def update_velocity(curr_velocity: NDArray[np.float64], force: NDArray[np.float64], time_step: float) -> NDArray[np.float64]:
    return curr_velocity + force * time_step

def update_position(curr_position: NDArray[np.float64], velocity: NDArray[np.float64], time_step: float) -> NDArray[np.float64]:
    return curr_position + velocity * time_step