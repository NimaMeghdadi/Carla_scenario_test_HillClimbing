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


def main():
    actor_list = []

    try:
        client = carla.Client('localhost', 2000)
        client.set_timeout(2.0)
        
        world = client.get_world()
        
        ped_bp=world.get_blueprint_library().filter("walker.pedestrian.*")
        controller_bp = world.get_blueprint_library().find('controller.ai.walker')
        
        trans = carla.Transform()
        # trans.location = world.get_random_location_from_navigation()
        
        trans.location.x = 225
        trans.location.y = 125
        trans.location.z = 1
        
        walker = random.choice(ped_bp)
        actor = world.spawn_actor(walker, trans)
        world.wait_for_tick()
        
        controller = world.spawn_actor(controller_bp, carla.Transform(),actor)
        world.wait_for_tick()
        
        controller.start()
        controller.go_to_location(carla.Location(x=225, y=139, z=1))
        
        actor_list.append(actor)
        
        for i in range(0,1000):
            world.wait_for_tick()
            print("step: ",i)
            print("pedestrian",actor.get_location())
            # print(controller.get_location())
            t = world.get_spectator().get_location()
            print ("watcher: ",t)
            time.sleep(1)
    except:
        print('exception: may be the location of the pedestrian is not valid')

    finally:

        print('destroying actors')
        client.apply_batch([carla.command.DestroyActor(x) for x in client.get_world().get_actors() if 'pedestrian' in x.type_id])
        
        print('done.')


if __name__ == '__main__':

    main()