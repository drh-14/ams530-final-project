from mpi4py import MPI
from grid import *
from force import *
from motion import *

if __name__ == "__main__":
    comm = MPI.COMM_WORLD 
    rank = comm.Get_rank()
    size = comm.Get_size()
    if rank == 0:
        grid = generate_grid(60, 60, 6, 6, 1900, 100)
    step_size = np.pow(10, -6)
    for _ in range(100):
        if rank == 0:
            # Broadcast points to all other processors.
            comm.bcast(grid)
        # Determine sub-box to work on.
        row_index, column_index = rank // 6, rank % 6
        for i, (point, velocity_vector) in enumerate(grid[row_index][column_index]):
            force = compute_force_total(point, grid)
            new_velocity = update_velocity(velocity_vector, force, step_size)
            new_position = update_position(point, new_velocity, step_size)
        # Send back to root process.
        
        # todo
        
        if rank == 0:
            # Update positions and velocities of points.
            pass
        
    if rank == 0:
        # Output to scatter plot.
        pass