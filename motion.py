def update_velocity(curr_velocity, force, time_step):
    return (curr_velocity[0] + (force[0] * time_step), curr_velocity[1] + (force[1] * time_step))

def update_position(curr_position, velocity, time_step):
    return (curr_position[0] + (velocity[0] * time_step), curr_position[1] + (velocity[1] * time_step))