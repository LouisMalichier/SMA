from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid
from model import MultiZoneRobotMission  # Adjust the import path based on your project structure
from agents import GreenRobot, Waste  # Adjust the import path
from objects import WasteDisposalZone  # Adjust the import path

def agent_portrayal(agent):
    portrayal = None
    if type(agent) is GreenRobot:
        portrayal = {"Shape": "circle", "Color": "green", "Filled": "true", "Layer": 2, "r": 0.8}
    elif type(agent) is Waste:
        portrayal = {"Shape": "rect", "Color": "brown", "Filled": "true", "Layer": 1, "w": 0.6, "h": 0.6}
    elif type(agent) is WasteDisposalZone:
        portrayal = {"Shape": "rect", "Color": "blue", "Filled": "true", "Layer": 1, "w": 1, "h": 1}
    return portrayal

grid = CanvasGrid(agent_portrayal, 9+3, 3, 500, 150)  # Adjust the grid size to accommodate all zones

server = ModularServer(MultiZoneRobotMission,
                       [grid],
                       "Multi Zone Robot Mission",
                       {"width": 9, "height": 3, "initial_waste": 4})

server.launch()
