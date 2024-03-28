#Group n°2
#22/03/2024
#Members : Badard Alexis, Malichier Louis, Saudreau Nicolas, Maamar Marouane

from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid
from model import SimpleRobotMission  # Adjust the import path based on your project structure
from agents import GreenRobot, Waste  # Adjust the import path
from objects import Radioactivity, WasteDisposalZone  # Adjust the import path

def agent_portrayal(agent):
    portrayal = None
    if type(agent) is GreenRobot:
        portrayal = {"Shape": "circle", "Color": "green", "Filled": "true", "Layer": 2, "r": 0.8}
    elif type(agent) is Waste:
        if agent.waste_type == "green":
            color = "green"
        elif agent.waste_type == "yellow":
            color = "yellow"
        portrayal = {"Shape": "rect", "Color": color, "Filled": "true", "Layer": 1, "w": 0.6, "h": 0.6}
    elif type(agent) is WasteDisposalZone:
        portrayal = {"Shape": "rect", "Color": "blue", "Filled": "true", "Layer": 1, "w": 1, "h": 1}
    elif type(agent) is Radioactivity:
        # Optional visualization for radioactivity
        portrayal = {"Shape": "rect", "Color": "lightgrey", "Filled": "true", "Layer": 1, "w": 1, "h": 1}
    return portrayal

grid = CanvasGrid(agent_portrayal, 4, 4, 500, 500)

server = ModularServer(SimpleRobotMission,
                       [grid],
                       "Simple Robot Mission",
                       {"width": 3, "height": 3, "initial_waste": 4})

server.launch()

