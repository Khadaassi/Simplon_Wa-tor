import matplotlib.pyplot as plt
import numpy as np

#______________________________________________________________________________
#
# region smooth_curve
#______________________________________________________________________________
def smooth_curve(x: list, y: list) -> tuple:
    """
    Smooths a curve using interpolation.

    Parameters:
    x (list): x-axis values.
    y (list): y-axis values.
    """
    x_new = np.linspace(min(x), max(x), num=300)
    y_smooth = np.interp(x_new, x, y)
    return x_new, y_smooth

#______________________________________________________________________________
#
# region plot_population
#______________________________________________________________________________
def plot_population(iterations: list, fish_population: list, shark_population: list, megalodon_population: list) -> None:
    """
    Plots the population of fish, sharks, and megalodons over time in real-time.
    
    Parameters:
    iterations (list): List of iterations.
    fish_population (list): List of fish population.
    shark_population (list): List of shark population.
    megalodon_population (list): List of megalodon population.
    """
    plt.style.use('seaborn-v0_8-darkgrid')
    
    # Initialisation subplot
    fig, axs = plt.subplots(3, 1, figsize=(10, 6))

    # Initialisation of lines
    fish_line, = axs[0].plot([], [], color="lightblue", linewidth=2.5, label="Fish Population")
    shark_line, = axs[1].plot([], [], color="firebrick", linewidth=2.5, label="Shark Population")
    megalodon_line, = axs[2].plot([], [], color="orange", linewidth=2.5, label="Megalodon Population")
    
    # Titles and labels
    for i, ax in enumerate(axs):
        ax.set_xlabel("Iterations", fontsize=14)
        ax.set_ylabel("Population", fontsize=14)
        ax.grid(visible=True)
    axs[0].set_title("Fish Population", fontsize=18)
    axs[1].set_title("Shark Population", fontsize=18)
    axs[2].set_title("Megalodon Population", fontsize=18)
    
    # Legend
    plt.tight_layout()

    # Plotting
    for i in range(len(iterations)):
        fish_x, fish_smooth = smooth_curve(iterations[:i+1], fish_population[:i+1])
        shark_x, shark_smooth = smooth_curve(iterations[:i+1], shark_population[:i+1])
        megalodon_x, megalodon_smooth = smooth_curve(iterations[:i+1], megalodon_population[:i+1])

        fish_line.set_data(fish_x, fish_smooth)
        shark_line.set_data(shark_x, shark_smooth)
        megalodon_line.set_data(megalodon_x, megalodon_smooth)


        axs[0].set_xlim(0, max(iterations))
        axs[1].set_xlim(0, max(iterations))
        axs[2].set_xlim(0, max(iterations))

        axs[0].set_ylim(0, max(fish_population) * 1.1)
        axs[1].set_ylim(0, max(shark_population) * 1.1)
        axs[2].set_ylim(0, max(megalodon_population) * 1.1 if max(megalodon_population) > 0 else 1)


        plt.pause(0.03)  
    plt.savefig("images/wator_populations.png")
    plt.show()

#______________________________________________________________________________
#
# region population_stats
#______________________________________________________________________________
def population_stats(fish_population: list, shark_population: list, megalodon_population: list, iterations: list, world) -> None:
    """
    Appends the population of fish, sharks, and megalodons over time.

    Parameters
    ----------
    fish_population (list): List of fish population.
    shark_population (list): List of shark population.
    megalodon_population (list): List of megalodon population.
    iterations (list): List of iterations.
    world : The world object.
    """
    fish_population.append(world.fish_population)
    shark_population.append(world.shark_population)
    megalodon_population.append(world.megalodon_population)
    iterations.append(world.world_age)
