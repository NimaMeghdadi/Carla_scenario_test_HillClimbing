import glob
import os
import sys
# from agents.navigation.basic_agent import BasicAgent
try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

sys.path.append('D:\carla0.9.13\PythonAPI\carla')
from agents.navigation.basic_agent import BasicAgent
import carla
import random
import time


def main():
    actor_list = []

    try:
        # Setup Carla settings
        client = carla.Client('localhost', 2000)
        client.set_timeout(2.0)
        traffic_manager = client.get_trafficmanager(8000)
        world = client.get_world()
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
        
        actor_list.append(vehicle)
        print('created %s' % vehicle.type_id)
        
        # Set Destination
        agent = BasicAgent(vehicle)
        agent.set_destination(carla.Location(x=208, y=129, z=1))
        
        # Get location of the vehicle and the spectator (watcher) every second
        for i in range(0,1000):
            world.wait_for_tick()
            print("step: ",i)
            print("Vehicle",vehicle.get_location())
            print ("watcher: ",world.get_spectator().get_location())
            time.sleep(1)
    except:
        print('exception: maybe the location of the pedestrian is not valid')

    finally:

        print('destroying actors')
        client.apply_batch([carla.command.DestroyActor(x) for x in client.get_world().get_actors() if 'vehicle' in x.type_id])
        
        print('done.')


if __name__ == '__main__':

    main()