import matplotlib.pyplot as plt


class Visualisation():
    def print_waste_per_step(data):
        plt.plot(data['Waste'])
        plt.title("Number of waste per step")
        plt.xlabel("Steps")
        plt.ylabel("Wastes") 





