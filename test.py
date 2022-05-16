
import time
import numpy as np

from mission_controller import MissionController
from simulated_robot import SimulatedRobot
from threading import Event
from queue import Queue


def test_normal_operation():
    command_queue = Queue(10) # Thread safe data structure
    robot_signal = Event() # Best practise to use Event to control the robot thread from Controller thread
    simulated_robot = SimulatedRobot(initial_position=np.array([0.0, 0.0]), command_queue=command_queue, robot_event=robot_signal)
    controller = MissionController(simulated_robot)

    
    # set the first trajectory
    controller.set_trajectory(np.array([[0.0, 0.0], [1.0, 0.0], [2.0, 0.0]]))
    time.sleep(10)
    # now set a different trajectory before the first trajectory completes
    controller.set_trajectory(np.array([[2.0, 0.0], [3.0, 0.0], [3.0, 1.0]]))
    time.sleep(4)
    controller.set_trajectory(np.array([])) 
    controller_thread = controller.get_controller_threadobj()
    controller_thread.join()
    simulated_robot.join()
    print("Test complete")
    return 


if __name__ == "__main__":
    test_normal_operation()
    exit(0)
