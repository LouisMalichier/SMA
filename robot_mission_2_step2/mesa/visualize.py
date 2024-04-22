from model_Louis import environment
import matplotlib.pyplot as plt


def print_waste_per_step(data, nb_agent):
    plt.plot(data['Waste'])
    plt.title("Number of waste per step" +(str(nb_agent)))
    plt.xlabel("Steps")
    plt.ylabel("Wastes") 




