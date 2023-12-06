
import sys
import numpy as np
import carla

sys.path.append('D:\carla0.9.13\PythonAPI\carla')
from agents.navigation.basic_agent import BasicAgent
from agents.navigation.behavior_agent import BehaviorAgent


class Car:
    def __init__(self):
        pass
    
    def create_car(self,client,world,speed =50, distance = 10, ):
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
            
            
            # vehicle.apply_control(carla.VehicleControl(Brake = 0.0))
            
            # vehicle.apply_control(carla.VehicleControl( brake = 0))
            perc_speed = -(speed * 100 /vehicle.get_speed_limit())+100
            traffic_manager.global_percentage_speed_difference(perc_speed)
            # all_attr = traffic_manager.get_all_actions(vehicle)
            # print(all_attr)
            # Set Destination
            # vehicle.set_target_speed(150)
            agent_basic = BasicAgent(vehicle)
            # agent = BehaviorAgent(vehicle,behavior='costume')
            agent_basic.set_destination(carla.Location(x=208, y=129, z=1))
            agent_basic.follow_speed_limits(value=True)
            # speed_limit = world.player.get_speed_limit()
            print(vehicle.get_speed_limit())
            # print(vehicle.forward_speed())
            # agent_basic.set_target_speed(0.0000001)
            # agent.set_target_speed(0.0000001)
            print("car was created")
            return vehicle
        except ValueError:
            print(ValueError)
    def start(self,vehicle):
        try:
            vehicle.set_autopilot(True,tm_port = 8000)
        except ValueError:
            print(ValueError)
