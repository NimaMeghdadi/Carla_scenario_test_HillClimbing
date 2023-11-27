
import sys
sys.path.append('D:\carla0.9.13\PythonAPI\carla')
from agents.navigation.basic_agent import BasicAgent
import random
import time
import carla

class Actors:
    def __init__(self):
        print("Actor created")
    
    def pedestrian(self,world):
        print("pedestrian")
        try:
            # Blueprint of the pedestrian
            ped_bp=world.get_blueprint_library().filter("walker.pedestrian.*")
            controller_bp = world.get_blueprint_library().find('controller.ai.walker')
            
            # transform of the pedestrian
            ped_loc = carla.Location(x=225, y=125, z=1)
            ped_trans = carla.Transform(ped_loc)
            
            #spawn the pedestrian
            walker = random.choice(ped_bp)
            actor = world.spawn_actor(walker, ped_trans)
            world.wait_for_tick()
            controller = world.spawn_actor(controller_bp, carla.Transform(),actor)
            world.wait_for_tick()
            
            # set the destination of the pedestrian
            controller.start()
            controller.go_to_location(carla.Location(x=225, y=139, z=1))

            return actor
        except:
            print('exception: may be the location of the pedestrian is not valid')
            
            
    def vehicle(self,client,world):
        try:
            # Setup Carla settings
            traffic_manager = client.get_trafficmanager(8000)
            blueprint_library = world.get_blueprint_library()
            
            # Paste the blueprint ID here:
            vehicle_bp = blueprint_library.find('vehicle.lincoln.mkz_2020') 
            
            # Set up the vehicle transform
            vehicle_loc = carla.Location(x=243, y=129, z=1)
            vehicle_rot = carla.Rotation(pitch=0.0, yaw=180.0, roll=0.0)
            vehicle_trans = carla.Transform(vehicle_loc,vehicle_rot)
            
            # Spawn the vehicle
            vehicle = world.spawn_actor(vehicle_bp, vehicle_trans)
            
            #set autopilot
            vehicle.set_autopilot( True,traffic_manager.get_port())
            
            # Set Destination
            agent = BasicAgent(vehicle)
            agent.set_destination(carla.Location(x=208, y=129, z=1))
            
            return vehicle
        except:
            print('exception: maybe the location of the pedestrian is not valid')
