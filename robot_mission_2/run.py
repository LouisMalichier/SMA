#Group n°2
#22/03/2024
#Members : Badard Alexis, Malichier Louis, Saudreau Nicolas, Maamar Marouane

from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid
from model import RobotMission  # Ensure this matches your project structure and class name
from agents import GreenRobot, YellowRobot, RedRobot, Waste  # Ensure correct import paths
from objects import Radioactivity, WasteDisposalZone  # Ensure correct import paths

def agent_portrayal(agent):
    portrayal = None
    if isinstance(agent, GreenRobot):
        portrayal = {"Shape": "circle", "Color": "green", "Filled": "true", "Layer": 2, "r": 0.5}
    elif isinstance(agent, YellowRobot):
        portrayal = {"Shape": "circle", "Color": "yellow", "Filled": "true", "Layer": 2, "r": 0.5}
    elif isinstance(agent, RedRobot):
        portrayal = {"Shape": "circle", "Color": "red", "Filled": "true", "Layer": 2, "r": 0.5}
    elif isinstance(agent, Waste):
        color = agent.waste_type  # Assuming waste_type directly corresponds to color
        portrayal = {"Shape": "rect", "Color": color, "Filled": "true", "Layer": 1, "w": 0.3, "h": 0.3}
    elif isinstance(agent, WasteDisposalZone):
        portrayal = {"Shape": "rect", "Color": "blue", "Filled": "true", "Layer": 1, "w": 1, "h": 1}
    elif isinstance(agent, Radioactivity):
        #Visualization for radioactivity can adjust color based on level, for simplicity using lightgrey
        portrayal = {"Shape": "rect", "Color": "lightgrey", "Filled": "true", "Layer": 0, "w": 1, "h": 1}
    else:
        portrayal = {"Shape": "rect", "Color": "white", "Filled": "false", "Layer": 0, "w": 1, "h": 1}
    return portrayal

grid = CanvasGrid(agent_portrayal, 12, 10, 500, 500)  # Adjust grid size and canvas size as needed

server = ModularServer(RobotMission,
                       [grid],
                       "Robot Waste Collection Mission",
                       {"width": 12, "height": 10, "initial_green_waste": 10, "initial_yellow_waste": 8, "initial_red_waste": 4})
                        

server.port = 8523  # The default
server.launch()


