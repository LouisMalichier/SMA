# Project Title: Robot Mission in a Hostile Environment

## Description

This agent-based simulation was developed as part of the *Systèmes Multi-Agents (SMA)* course at CentraleSupélec. It uses Mesa, a Python library, to model a scenario where robots navigate through a grid to manage different types of waste. Each robot type—Green, Yellow, and Red—is tasked with handling specific waste types in areas that vary in levels of radioactivity. The simulation investigates three main strategies for optimizing waste collection: random movement, pheromone tracking, and communication between agents. These approaches highlight the potential for autonomous systems to improve efficiency and effectiveness in complex environments.


## Fixed Parameters

To ensure consistency and comparability of results across different simulation strategies, certain parameters were held constant throughout the project:

- **Number of Robots**: Each robot type (Green, Yellow, Red) has a fixed count of two robots.
- **Total Wastes**: The grid starts with 26 pieces of waste distributed as follows:
  - **Green Waste**: 10 pieces
  - **Yellow Waste**: 8 pieces
  - **Red Waste**: 8 pieces
- **Grid Dimensions**: The simulation grid is set at a fixed size of 12 (width) x 10 (height).

These parameters were chosen to maintain a balance between complexity and performance, allowing for meaningful comparisons between different strategies without overwhelming computational demands or oversimplifying the simulation's challenges.

## Strategies

### Random Movement (`robot_mission_2_step1_random`)
**Approach Description**:
- Robots move randomly across the grid to collect and dispose of waste.
- **Key Code Insight**: Each robot has a `knowledge` attribute that keeps track of collected waste and current position. Decisions to move, collect waste or move to the disposal zone are based on this knowledge.

**Performance**:
- Completes the cleaning of all the wastes in 329 steps.
![Random Approach Results](https://github.com/LouisMalichier/SMA/blob/main/results/steps%20to%20clean%20wastes_random_approach.png)

### Pheromone-Based Movement (`robot_mission_2_step1_SwarmInt`)
**Approach Description**:
- Robots leave a pheromone trail that decays over time to minimize revisiting the same areas, enhancing the efficiency of the cleaning process. This strategy mimics natural phenomena observed in some species, such as ants, which use pheromones to communicate and optimize paths.
- **Key Code Insight**: Robots assess the pheromone concentration in adjacent cells and move to the one with the lowest concentration, helping distribute the robots more evenly across the grid and reduce overlap in visited areas.

**Rationale**:
- **Biological Inspiration**: The use of pheromones is inspired by biological entities that mark their paths with chemicals to guide their activities efficiently. This method is particularly effective in distributed systems where individual agents operate semi-autonomously with limited direct communication. We used this strategy to mimic the trails left by a robot in the field or the drop of some liquid to inform other robots about the cell that was discovered .
- **Decay Mechanism**: The pheromone decay (set at a 10% reduction per timestep) ensures that older trails become less influential, allowing newer information to take precedence and more dynamically reflect changes in the environment or task status.
- **Efficiency Optimization**: This approach was chosen because it allows for a self-organizing system where each robot indirectly coordinates with others through environmental modification (pheromone laying), rather than direct communication or central control. It reduces the chances of robots repeatedly cleaning the same areas unnecessarily, thereby speeding up the overall process.


**Performance**:
- Reduces the number of steps to 274.
![Pheromone Approach Results](https://github.com/LouisMalichier/SMA/blob/main/results/steps%20to%20clean%20wastes_intelligence_swarm.png)

### Communication Between Agents (`robot_mission_2_step2`)
**Approach Description**:
- Robots are equipped with communication capabilities that allow them to direct each other towards unhandled waste. This advanced strategy uses targeted communication to reduce redundant travel and increase the efficiency of waste collection across the grid.
- **Key Code Insight**: Robots utilize a sophisticated message passing system, implemented through a custom communication module. When a robot encounters a type of waste it cannot process, it sends a detailed message containing the location and type of this waste to robots that are equipped to handle it.

**Rationale**:
- **Strategic Communication**: This strategy is inspired by distributed systems where efficiency is achieved through cooperation and information sharing. By communicating pertinent information about waste locations, robots can avoid unnecessary exploration and concentrate their efforts where they are most needed.
- **Message Passing Mechanism**: Each message contains specific directives, including the waste type and its precise location. Robots receive these messages and can immediately adjust their paths to target these locations, ensuring a coordinated and systematic cleaning process.
- **Load Balancing**: Messages are not broadcast indiscriminately. Instead, they are sent to the robot that currently has the lowest workload in terms of unprocessed waste, helping to balance the effort across all robots and prevent any single robot from becoming overwhelmed.

**Implementation Details**:
- **Message Storage and Dispatch**: Messages are temporarily stored in a centralized message service within the model. They are dispatched conditionally, based on the robot’s current state and workload, ensuring that messages are processed in a timely and relevant manner.
- **Decision-Making Based on Communication**: Robots deliberate upon receiving new data to decide the most efficient route to the waste, considering their current position and the state of the grid. This decision-making process is crucial for optimizing paths and actions in real-time.

**Performance**:
- This communicative approach drastically reduces the number of steps needed to clear all waste to just 190 steps, demonstrating a substantial increase in process efficiency compared to earlier methods.
![Communication Approach Results](https://github.com/LouisMalichier/SMA/blob/main/results/steps%20to%20clean%20wastes_comm.png)

## Results Summary

The table below summarizes the efficiency of each strategy by showing the number of steps required to clear all waste from the grid. This metric helps in comparing the effectiveness of different approaches implemented in the simulation:

| Strategy                          | Number of Steps |
|-----------------------------------|-----------------|
| Random Movement                   | 329             |
| Pheromone-Based Movement          | 274             |
| Communication Between Agents      | 190             |

These results clearly demonstrate the benefits of advanced strategies such as pheromone tracking and communication over simple random movement.

## Future Perspectives

While the current simulation provides valuable insights into waste management in a hostile environment, there are several enhancements and new features that could be explored to further the capabilities and realism of the model:

### Zoning Improvements
- **Fixed Subzones**: Implement fixed subzones for each robot type to manage, which could improve efficiency by reducing travel time between waste types that are far apart. This would also simulate real-world scenarios where certain teams are dedicated to specific areas within a larger environment.

### Obstacle Handling
- **Dynamic Obstacles**: Introduce dynamic obstacles that robots must navigate around, such as sudden blockages or unsafe zones, which would add complexity and require more sophisticated pathfinding algorithms.
- **Static Obstacles**: Implement static obstacles to test the robots' ability to plan routes at the start of the simulation and adapt their strategies based on the layout of the grid.

### Maintenance and Robot Health
- **Robot Maintenance**: Consider scenarios where robots need periodic maintenance or can suffer malfunctions, requiring them to return to a base station for repairs. This would add a layer of challenge in resource management and scheduling.
- **Robot Health Monitoring**: Incorporate sensors and health monitoring, where robots can assess their operational status and decide when to seek repairs, adding realism and a new layer of decision-making.

### Learning Algorithms
- **Machine Learning**: Integrate machine learning algorithms that allow robots to learn from their environment and previous experiences, improving their efficiency over time based on data collected during past clean-up operations.

### Scalability Tests
- **Larger Grids and More Robots**: Test the scalability of the current algorithms by increasing the number of robots and the size of the grid. This would provide insights into the limits and scalability of the proposed solutions.

### User Interaction
- **Enhanced User Controls**: Develop more interactive controls that allow users to intervene more directly in the simulation, such as manually directing a robot to focus on specific areas or tasks.

These future directions could significantly enhance the model's functionality and provide deeper insights into autonomous robotic systems in complex environments.

## Usage

The simulation is designed to be user-friendly and customizable through various parameters that can be adjusted to see how different settings impact robot behavior and efficiency. Here’s how to get started and make the most of the simulation capabilities:

### Running the Simulation

To start the simulation, navigate to the project directory and execute the `run.py` file:

```bash
python run.py
```
Upon running the script, a graphical user interface (GUI) will launch, displaying a grid where the simulation takes place. This GUI is interactive and allows for real-time adjustments and observations.

### Customizing Parameters
In the GUI, you will find controls that allow you to adjust several aspects of the simulation:

- Number of Robots: Set the number of robots for each type (Green, Yellow, Red) to determine their density on the grid.
- Initial Waste: Adjust how much waste is initially placed on the grid, which can vary by type.
- Grid Dimensions: Modify the size of the grid to explore how different grid sizes affect the simulation.
- Frames Per Second (FPS): Control the speed of the simulation with a slider that adjusts how fast the simulation steps are processed and displayed.

### Dynamic Visualization
Below the main simulation grid, there is a dynamic visualization that tracks and displays the number of wastes processed per step. This feature is crucial for analyzing the efficiency of different strategies in real-time. As the simulation runs, you will see a graph that updates continuously, reflecting the remaining waste at each step. This allows for immediate visual feedback on the impact of parameter changes or different strategies:

- Graph Details: The graph shows the total waste count over time, plotted as the simulation progresses.
- Start/Stop Button: This button allows you to start or pause the simulation at any time, giving you control to stop and analyze the current state or make adjustments.
- Reset Button: Resets the simulation to its initial state based on the current parameters, useful for running multiple trials without restarting the application.

## Installation

Clone the project using:

```bash
git clone https://github.com/LouisMalichier/SMA.git
cd your-repository-name
```

## Contact
Maamar Marouane - @Enaouram

Louis Malichier - @LouisMalichier

Alexis Badard - @AlexisBadard

Nicolas Saudreau - @
