import random
import numpy as np
from typing import List, Tuple

def generate_grid(N:int, M:int, n:int, m:int, num_black:int, num_white:int) -> List[List[List[Tuple[List[float], List[float]]]]]:
    num_rows, num_cols = N // n, M // m
    grid = [[[] for _ in range(num_cols)] for _ in range(num_rows)]
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            num_points = num_black if (i + j) % 2 == 0 else num_white
            x_start, x_end  = j * m, (j + 1) * m
            y_start, y_end = i * n, (i + 1) * n
            for _ in range(num_points):
                random_x = random.uniform(x_start, x_end)
                random_y = random.uniform(y_start, y_end)
                random_angle = random.uniform(0, 2 * np.pi)
                magnitude = random.uniform(0, 1)
                velocity_x = magnitude * np.cos(random_angle)
                velocity_y = magnitude * np.sin(random_angle)
                grid[i][j].append((np.array([random_x, random_y]), np.array([velocity_x, velocity_y]))) 
    return grid