from world import World

def console_print(world: World) -> None:
    """
    Print the current state of the world in the console

    Parameters
    ----------
    world : World
        The world to print
    
    Returns
    -------
    None
    """
    print("Current iteration : ", world.world_age)
    world.print_grid()
    print(
        f"Fish pop : {world.fish_population} ; Shark pop : {world.shark_population} ; Megalodon pop : {world.megalodon_population}; Pacman score : {world.pacman_score}"
        )
    print(f"Killed by storms : {world.killed_by_storm}")