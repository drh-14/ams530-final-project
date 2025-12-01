from mpi4py import MPI
from grid import *
from force import *
import matplotlib.pyplot as plt
import time

if __name__ == "__main__":
    comm = MPI.COMM_WORLD 
    rank = comm.Get_rank()
    size = comm.Get_size()
    grid = [[]]

    if rank == 0:
        grid = generate_grid(60, 60, 6, 6, 100, 1900)

    step_size = 10 ** (-6)
    start_time = time.time()
    directions = [[-1,0], [-1,-1], [-1, 1], [1,0], [1, -1], [1,1], [0, 1], [0, -1]]
    for _ in range(100):
        cell = comm.scatter(grid)
        row_index, col_index = rank // 6, rank % 6
        neighbor_cells = []
        for dx, dy in directions:
            nr,nc = row_index + dx, col_index + dy
            if 0 <= nr < 6 and 0 <= nc < 6:
                neighbor_cells.append(comm.sendrecv(sendobj = cell, dest = 6 * nr + nc, source = 6 * nr + nc))
        for particle in cell:
           force = compute_force_total(particle, neighbor_cells)
           update_particle(particle, force, step_size)
        updated_cells = comm.gather(cell)
        if rank == 0:
            if updated_cells:
                for i in range(size):
                    grid[i // 6][i % 6] = updated_cells[i]

    processor_times = comm.gather(time.time() - start_time)
    if rank == 0:
        plt.title("Final Positions of Particles")
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                for lst in grid[i][j]:
                    plt.plot(lst[0][0], lst[0][1])
        plt.savefig("final_positions_plot.png")
        plt.clf()
        if processor_times:
            for i in range(size):
                plt.bar(range(size), processor_times)
        plt.title("Execution Times for Cores")
        plt.savefig("core_execution_times.png")