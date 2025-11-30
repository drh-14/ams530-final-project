from mpi4py import MPI
from grid import *
from force import *
from motion import *
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
    directions = [[-1,0], [-1,-1], [-1, 1], [1,0], [1, -1], [1,1], [0, 1], [0, -1], [0, 0]]
    for i in range(100):
        # Send main cell.
        if rank == 0:
            for j in range(1, size):
               comm.send(grid[j // 6][j % 6], dest = j)
       
        cell = grid[0][0] if rank == 0 else comm.recv(source = 0)
        row_index, col_index = rank // 6, rank % 6
        neighbor_cells = []
        for dx, dy in directions:
            nr,nc = row_index + dx, col_index + dy
            if 0 <= nr < 6 and 0 <= nc < 6:
                neighbor_cells.append(comm.sendrecv(sendobj = cell, dest = 6 * nr + nc, source = 6 * nr + nc))
        
        force = compute_force_total(cell, neighbor_cells) # type: ignore
        new_velocity = update_velocity(cell[1][1], force, step_size) # type: ignore
        new_position = update_position(cell[0], new_velocity, step_size) # type: ignore
        new_cell = (new_velocity, new_position)
        updated_cells = comm.gather(new_cell)
        if rank == 0:
            for i in range(size):
                grid[i // 6][i % 6] = updated_cells # type: ignore

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