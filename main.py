from multiprocessing import Pool
from grid import *
from force import *
import matplotlib.pyplot as plt

def update_cell(i, neighbor_indices, grid, time_step):
    for j in range(len(grid[i])): 
        force = compute_force_total(grid[i][j], [grid[j] for j in neighbor_indices])
        grid[i][j][1] += (force * time_step)
        grid[i][j][0] += (grid[i][j][1] * time_step)
    return grid[i]

if __name__ == "__main__":
    grid = generate_grid(60, 60, 10, 10, 100, 1900)
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
                 new_grid = p.map(lambda t: update_cell(t[0], t[1], grid, step_size), tasks)
                 grid = new_grid

    for i in range(6):
        for j in range(6):
            lst = grid[i][j]
            pos, _ = lst 
            x,y = pos 
            plt.plot(x,y)

    plt.title("Final Positions of Particles")
    plt.savefig("final_positions_plot.png")
    plt.clf()
    plt.bar(range(36), times)
    plt.title("Execution Times for 36 Cores")
    plt.savefig("core_execution_times_chart.png")


    