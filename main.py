from multiprocessing import Pool
from grid import *
from force import *
import matplotlib.pyplot as plt
import time

def update_cell(cell, neighbors, time_step):
    start_time = time.time()
    for j in range(len(cell)): 
        force = compute_force_total(cell[j], neighbors)
        cell[j][1] += (force * time_step)
        cell[j][0] += (cell[j][1] * time_step)
    return (cell, time.time() - start_time)

def update_task(t):
    i, neighbor_indices = t
    return update_cell(grid[i], [grid[n] for n in neighbor_indices], step_size)

if __name__ == "__main__":
    grid = generate_grid(60, 60, 10, 10, 1900, 100)
    grid = [grid[i][j] for i in range(6) for j in range(6)]
    times = []
    step_size = 1e-6
    directions = [[-1,0], [-1,-1], [-1,1], [1,0], [1,-1], [1,1], [0,1], [0,-1]]

    tasks = []
    for i in range(36):
        cell = grid[i]
        neighbors = []
        r,c = i // 6, i % 6
        for dx, dy in directions:
            ni = r + dx
            nj = c + dy
            idx = 6 * ni + nj
            if 0 <= idx < 36:
                neighbors.append(idx)
        tasks.append((i, neighbors))
    
    with Pool(processes = 36) as p:
            for _ in range(100):
                results = p.map(update_task, tasks)
                grid = [r[0] for r in results]
                iter_times = [r[1] for r in results]
                for i in range(len(iter_times)):
                     times[i] += iter_times[i]
                new_grid = [[] for _ in range(36)]
                for i in range(len(grid)):
                    for particle in grid[i]:
                        x,y = particle[0]
                        row, col = int(y // 10), int(x // 10)
                        new_grid[6 * row + col].append(particle)
                grid = new_grid


    x_coords, y_coords = [], []
    for i in range(36):
            lst = grid[i]
            for particle in lst:
                pos, _ = particle
                x,y = pos 
                x_coords.append(x)
                y_coords.append(y)
    plt.scatter(x_coords, y_coords, s = 5)

    plt.title("Final Positions of Particles After 100 Iterations")
    plt.savefig("final_positions_plot.png")
    plt.clf()
    plt.bar(range(36), times)
    plt.title("Execution Times for 36 Cores")
    plt.savefig("core_execution_times_chart.png")


    