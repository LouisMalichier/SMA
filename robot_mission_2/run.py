#Group n°2
#22/03/2024
#Members : Badard Alexis, Malichier Louis, Saudreau Nicolas, Maamar Marouane

from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from model import RobotMission 
from agents import GreenRobot, YellowRobot, RedRobot, Waste  
from objects import Radioactivity, WasteDisposalZone  
from visualize import Visualisation
import time

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
        #Visualization for radioactivity can adjust color based on level, for simplicity using lightgrey
        portrayal = {"Shape": "rect", "Color": "lightgrey", "Filled": "true", "Layer": 0, "w": 1, "h": 1}
    else:
        portrayal = {"Shape": "rect", "Color": "white", "Filled": "false", "Layer": 0, "w": 1, "h": 1}
    return portrayal

grid = CanvasGrid(agent_portrayal, 12, 10, 500, 500)  # 12x10 grid, 500x500 pixels
chart_element = ChartModule(
    [
        {"Label": "Waste", "Color": "#AA0000"},
    ]
)

robot_mission=RobotMission(width=12,height=10,initial_green_waste=10,initial_yellow_waste=8,initial_red_waste=4)
server = ModularServer(RobotMission,
                       [grid,chart_element],
                       "Robot Waste Collection Mission",
                       {'width':12,'height':10,'initial_green_waste':10,'initial_yellow_waste':8,'initial_red_waste':4}
                       )
server.port = 8523  # The default
print("server launched")
server.launch()
# time.sleep(5)
# server.run_until_visualized()
# server.quit()
# data=robot_mission.datacollector.get_model_vars_dataframe()
# print(data)

# print("get data")
# data.head()
# visualisation=Visualisation()
# visualisation.print_waste_per_step(data)