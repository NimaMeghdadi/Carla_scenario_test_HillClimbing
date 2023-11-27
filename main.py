import glob
import os
import sys

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla
import random
import time
import helpers 

def main():
    actor_list = []
    actors = helpers.Actors()
    try:
        # Setup Carla settings
        client = carla.Client('localhost', 2000)
        client.set_timeout(20.0)
        # if yo want to change the map, uncomment the following line
        world = client.get_world() # world = client.load_world('Town01')
        world.wait_for_tick()
        # creat the pedestrian and car
        ped = actors.pedestrian(world)
        car = actors.vehicle(client, world)
        
        # add to actor list
        actor_list.append(ped)
        actor_list.append(car)
        
        # illustrate the movement of the pedestrian and the vehicles
        for i in range(0,100):
                print("step: ",i)
                print("pedestrian",ped.get_location())
                print("car",car.get_location())
                print ("watcher: ",world.get_spectator().get_location())
                time.sleep(1)

    finally:

        print('destroying actors')
        for actor in actor_list:
            actor.destroy()
        print('done.')


if __name__ == '__main__':

    main()