import random

def generate_grid(N, M, n, m, num_black, num_white):
    num_rows, num_cols = N // n, M // m
    grid = [[[] for _ in range(num_cols)] for _ in range(num_rows)]
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            num_points = num_black if (i + j) % 2 == 0 else num_white
            x_start, x_end  = j * m, (j + 1) * m
            y_start, y_end = i * n, (i + 1) * n
            random_x = [random.uniform(x_start, x_end)] * num_points
            random_y = [random.uniform(y_start, y_end)] * num_points
            for k in range(num_points):
                grid[i][j].append((random_x[k], random_y[k]))     
    return grid