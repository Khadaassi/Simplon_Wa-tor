
import matplotlib.pyplot as plt



def plot_population(iterations, fish_population, shark_population, megalodon_population):

    plt.figure(figsize=(12, 7))


    plt.plot(iterations, fish_population, color="royalblue", linewidth=2.5, label="Population de Poissons")

    plt.plot(iterations, shark_population, color="darkorange", linewidth=2.5, label="Population de Requins")

    plt.plot(iterations, megalodon_population, color="purple", linewidth=2.5, label="Population de Mégalodons")


    plt.title("Évolution de la Population de Poissons et de Requins au Fil du Temps", fontsize=16, fontweight="bold")
    plt.xlabel("Itérations", fontsize=14)
    plt.ylabel("Population", fontsize=14)


    plt.legend(fontsize=12, loc="upper right")


    plt.grid(visible=True, which="both", linestyle="--", linewidth=0.5, alpha=0.7)

    plt.tight_layout()
    plt.show()
