import numpy as np 
import time
from queue import Queue 
from simulated_robot import SimulatedRobot
from threading import Thread

class MissionController:
    def __init__(self, robot:SimulatedRobot):
        '''
            Controller Class to control the movement of robot 
            @robot : SimulatedRobot 
                Takes the instantiated robot object as input
        '''
        print("Controller :: Creating MissionController")
        self._robot = robot
        self._stop = False
        self.trajectory = None 
        self.robot_command_queue = self._robot.command_queue
        self.robot_maneuver_signal = self._robot.robot_maneuver_event
        self._robot.start()
        self._trajectory_counter = 0
        self._controller_command_queue = Queue(10)
        self._command_thread = Thread(target=self._navigation_command_thread, daemon=True)
        self._command_thread.start()

    def get_controller_threadobj(self):
        '''
            Public method : Getter to fetch command thread to join to main thread
        '''
        return self._command_thread

    def stop_command_thread(self):
        '''
            Public method : Stops the Controller thread
        '''
        self._stop = True
        print("Controller :: Killing command thread")
    
    def set_trajectory(self, trajectory:np.array):
        '''
            Sets Trajectory to robot on demand ( can interrupt robot's current movement )
        '''
        self._trajectory_counter += 1
        print(f"Controller :: New Trajectory received {trajectory}")

        if trajectory.size == 0:
            print("Controller :: Stopping the robot")
            self._robot.stop()
            self.stop_command_thread()
        
        self.trajectory = trajectory
        self._controller_command_queue.put(self.trajectory)

    def _send_navigation_command(self, current_trajectory, start_counter):
        '''
            Internal private method from controller thread to send position to robot
        '''
        for _, pos in enumerate(current_trajectory):
            print(f"Controller :: Sending waypoint {pos} to robot")
            time.sleep(1)
            if start_counter < self._trajectory_counter: # Checks if new trajectory has been received during the current trajectory is being sent
                print("Controller :: Trajectory change event")
                self.robot_maneuver_signal.set()
                return
            self.robot_command_queue.put(pos)
        
    def _navigation_command_thread(self):
        '''
            Controller Thread target function
        '''
        print("Controller :: Started Controller thread")
        while not self._stop:
            current_trajectory = self._controller_command_queue.get()
            current_trajectory_counter = self._trajectory_counter 
            self._send_navigation_command(current_trajectory, current_trajectory_counter)
        print("Controller :: Stopped command thread")
            
            
            



         
        