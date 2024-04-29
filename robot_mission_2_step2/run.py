#Group n°2
#22/03/2024
#Members : Badard Alexis, Malichier Louis, Saudreau Nicolas, Maamar Marouane

from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from model import RobotMission 
from agents import GreenRobot, YellowRobot, RedRobot, Waste  
from objects import Radioactivity, WasteDisposalZone  
import mesa

def agent_portrayal(agent):
    portrayal = None
    if isinstance(agent, GreenRobot):
        portrayal = {"Shape": "circle", "Color": "green", "Filled": "true", "Layer": 2, "r": 0.5}
    elif isinstance(agent, YellowRobot):
        portrayal = {"Shape": "circle", "Color": "yellow", "Filled": "true", "Layer": 2, "r": 0.5}
    elif isinstance(agent, RedRobot):
        portrayal = {"Shape": "circle", "Color": "red", "Filled": "true", "Layer": 2, "r": 0.5}
    elif isinstance(agent, Waste):
        color = agent.waste_type  # Color by waste type
        portrayal = {"Shape": "rect", "Color": color, "Filled": "true", "Layer": 1, "w": 0.3, "h": 0.3}
    elif isinstance(agent, WasteDisposalZone):
        portrayal = {"Shape": "rect", "Color": "blue", "Filled": "true", "Layer": 1, "w": 1, "h": 1}
    elif isinstance(agent, Radioactivity):
        # Assign color based on the zone
        color = "white"  # Default color
        if agent.zone == "z1":
            color = "lightgreen"
        elif agent.zone == "z2":
            color = "lightyellow"
        elif agent.zone == "z3":
            color = "lightcoral"
        return {"Shape": "rect", "Color": color, "Filled": "true", "Layer": 0, "w": 1, "h": 1}
    else:
        portrayal = {"Shape": "rect", "Color": "white", "Filled": "false", "Layer": 0, "w": 1, "h": 1}
    return portrayal

grid = CanvasGrid(agent_portrayal, 12, 10, 500, 500)  # 12x10 grid, 500x500 pixels
chart_element = ChartModule(
    [
        {"Label": "Waste", "Color": "#AA0000"},
    ])

model_params = {
    "width": 12,
    "height": 10,
    "initial_green_waste": mesa.visualization.Slider("Initial Green Waste", 10, 1, 15),
    "initial_yellow_waste": mesa.visualization.Slider("Initial Yellow Waste", 8, 1, 15),
    "initial_red_waste": mesa.visualization.Slider("Initial Red Waste", 8, 1, 15),
    "nb_green_agent": mesa.visualization.Slider("Number of Green Robots", 2, 1, 5),
    "nb_yellow_agent": mesa.visualization.Slider("Number of Yellow Robots", 2, 1, 5),
    "nb_red_agent": mesa.visualization.Slider("Number of Red Robots", 2, 1, 5)
}

server = ModularServer(RobotMission,
                       [grid, chart_element],
                       "Robot Waste Collection Mission",
                       model_params)
                        

server.port = 8523  # The default
server.launch()


