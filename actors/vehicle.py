
import sys
import numpy as np
import carla

sys.path.append('D:\carla0.9.13\PythonAPI\carla')
from agents.navigation.basic_agent import BasicAgent
from agents.navigation.behavior_agent import BehaviorAgent


class Car:
    def __init__(self):
        pass
    
    def create_car(self,client,world,speed =30, distance = 10):
        try:
            
            x_car = 225+distance
            # Setup Carla settings
            traffic_manager = client.get_trafficmanager(8000)
            blueprint_library = world.get_blueprint_library()
            # Paste the blueprint ID here:
            vehicle_bp = blueprint_library.find('vehicle.lincoln.mkz_2020') 
            # Set up the vehicle transform
            vehicle_loc = carla.Location(x= x_car, y=129, z=1)
            vehicle_rot = carla.Rotation(pitch=0.0, yaw=180.0, roll=0.0)
            vehicle_trans = carla.Transform(vehicle_loc,vehicle_rot)
            
            # Spawn the vehicle
            vehicle = world.spawn_actor(vehicle_bp, vehicle_trans)
            world.wait_for_tick()
            
            #set autopilot
            vehicle.set_autopilot( True,traffic_manager.get_port())
            
            # vehicle.apply_control(carla.VehicleControl(Brake = 0.0))
            
            # vehicle.apply_control(carla.VehicleControl( brake = 0))
            
            # Set Destination
            # vehicle.set_target_speed(150)
            agent_basic = BasicAgent(vehicle)
            agent = BehaviorAgent(vehicle,behavior='aggressive')
            agent.set_destination(carla.Location(x=208, y=129, z=1))
            agent_basic.set_target_speed(150)
            # agent.set_target_speed(speed)
            print("car was created")
            return vehicle
        except ValueError:
            print(ValueError)
