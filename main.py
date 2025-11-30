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
        grid = generate_grid(60, 60, 6, 6, 1900, 100)

    step_size = 10 ** (-6)
    start_time = time.time()
    for _ in range(100):
        grid = comm.bcast(grid)
        # Determine sub-box to work on.
        updated_subgrid = []
        row_index, column_index = rank // 6, rank % 6
        for lst in grid[row_index][column_index]:
            point, velocity_vector = lst
            force = compute_force_total(point, grid)
            new_velocity = update_velocity(velocity_vector, force, step_size)
            new_position = update_position(point, new_velocity, step_size)
            updated_subgrid.append((new_position, new_velocity))

        # Send back to root process.
        updated_data = comm.gather(updated_subgrid)
        
        if rank == 0:
            # Update positions and velocities of points.
            if updated_data:
               for i in range(len(grid)):
                   for j in range(len(grid[0])):
                       grid[i][j] = updated_data[i][j]
            
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