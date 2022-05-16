import numpy as np 
import time 
from threading import Thread, Event
from queue import Queue
import random

class SimulatedRobot(Thread):
    def __init__(self, initial_position:np.array, command_queue: Queue, robot_event: Event) -> None:
        '''
            SimulatedRobot class is a robot simulator, moves to given position by Controller 
            @param : intial_position
                Initial position of the robot as np.array 
            @param : command_queue
                Robot command queue object 
            @param : robot_event
                Event object to control the navigation events for robot
        '''
        super(SimulatedRobot, self).__init__()
        print("Robot :: Creating SimulatedRobot")
        self.position = initial_position
        self.command_queue = command_queue
        self.robot_maneuver_event = robot_event
        self.stop_robot = False

    def get_position(self) -> np.array:
        '''
            Fetches the current position of the robot
        '''
        return self.position

    def stop(self) -> None:
        '''
            Stops the current Robot thread
        '''
        print("Robot :: Stop command called from controller")
        self.stop_robot = True

    def run(self) -> None:
        print("Robot :: Started robot thread")
        while not self.stop_robot:
            if not self.command_queue.empty():
                position_to_move = self.command_queue.get_nowait()
                if not np.array_equal(position_to_move, self.position):
                    print(f"Robot :: Robot is moving to position {position_to_move}")
                    self.robot_maneuver_event.wait(random.uniform(1.0, 2.0))
                    if self.robot_maneuver_event.is_set():
                        print(f"Robot :: New Trajectory set")
                        self.robot_maneuver_event.clear()
                        continue
                    else:
                        self.position = position_to_move
                    print(f"Robot :: Robot is now at position {self.position}")
                else:
                    print(f"Robot :: Robot is already at {self.position}")
            else:
                continue
        print("Robot :: Stopped robot")




