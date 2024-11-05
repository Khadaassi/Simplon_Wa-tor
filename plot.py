import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
#__________________________________________________________________________
#
# region smooth_curve
#__________________________________________________________________________
def smooth_curve(x: list, y : list) -> tuple:
    """
    Smooths a curve using interpolation.

    Parameters:
    x (list): x-axis values.
    y (list): y-axis values.
    """
    x_new = np.linspace(min(x), max(x), num=300)
    y_smooth = np.interp(x_new, x, y)
    return x_new, y_smooth
#__________________________________________________________________________
#
# region plot_population
#__________________________________________________________________________
def plot_population(iterations: list, fish_population: list, shark_population: list, megalodon_population: list ) -> None:
    """
    Plots the population of fish, sharks, and megalodons over time.
    
    Parameters:
    iterations (list): List of iterations.
    fish_population (list): List of fish population.
    shark_population (list): List of shark population.
    megalodon_population (list): List of megalodon population.
    """
    plt.style.use('seaborn-v0_8-darkgrid')
    
    # Create three subplots (3 rows, 1 column)
    fig, axs = plt.subplots(3, 1, figsize=(12, 15))

    # Smooth the curves
    fish_x, fish_smooth = smooth_curve(iterations, fish_population)
    shark_x, shark_smooth = smooth_curve(iterations, shark_population)
    megalodon_x, megalodon_smooth = smooth_curve(iterations, megalodon_population)

    # Plot fish population
    axs[0].plot(fish_x, fish_smooth, color="lightblue", linewidth=2.5, label="Fish Population")
    axs[0].set_title("Fish Population", fontsize=18)
    axs[0].set_xlabel("Iterations", fontsize=14)
    axs[0].set_ylabel("Population", fontsize=14)
    axs[0].legend()
    axs[0].grid(visible=True)

    # Plot shark population
    axs[1].plot(shark_x, shark_smooth, color="firebrick", linewidth=2.5, label="Shark Population")
    axs[1].set_title("Shark Population", fontsize=18)
    axs[1].set_xlabel("Iterations", fontsize=14)
    axs[1].set_ylabel("Population", fontsize=14)
    axs[1].legend()
    axs[1].grid(visible=True)

    # Plot megalodon population
    axs[2].plot(megalodon_x, megalodon_smooth, color="orange", linewidth=2.5, label="Megalodon Population")
    axs[2].set_title("Megalodon Population", fontsize=18)
    axs[2].set_xlabel("Iterations", fontsize=14)
    axs[2].set_ylabel("Population", fontsize=14)
    axs[2].legend()
    axs[2].grid(visible=True)

    plt.tight_layout()
    plt.savefig("images/populations.png")
    #plt.show()
