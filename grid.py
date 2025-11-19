import numpy as np
def generate_grid(N, M, n, m):
    # N x M grid, n row subbox, y col subbox
    num_rows, num_cols = N // n, M // m
    grid = [[[] for _ in range(num_cols)] for _ in range(num_rows)]

def place_points(num_points_black, num_points_white, grid: list[list[list[int]]]):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            num_points = num_points_black if (i + j) % 2 == 0 else num_points_white
            x_start, x_end  = 0, 0
            x_difference = x_end - x_start
            y_start, y_end = 0, 0
            y_difference = y_end - y_start
            random_x = np.random.rand(num_points)
            random_y = np.random.rand(num_points)
            grid[i][0][j] = np.array(
                [(x_difference * random_x[i] + x_start, 
                  y_difference * random_y[i] + y_start) 
                  for i in range(num_points)]
                )
    return grid