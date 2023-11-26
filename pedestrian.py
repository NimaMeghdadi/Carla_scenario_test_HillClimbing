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
        trans.location.x = 10
        trans.location.y = -50
        trans.location.z = 1
        # trans.location(carla.location(x=10, y=10, z=1))
        
        walker = random.choice(ped_bp)
        actor = world.spawn_actor(walker, trans)
        world.wait_for_tick()
        
        controller = world.spawn_actor(controller_bp, carla.Transform(),actor)
        world.wait_for_tick()
        
        controller.start()
        controller.go_to_location(carla.Location(x=10, y=-110, z=1))
        
        actor_list.append(actor)
        
        for i in range(0,10):
            world.wait_for_tick()
            print("step: ",i)
            print(actor.get_location())
            print(controller.get_location())
            time.sleep(1)

    finally:

        print('destroying actors')
        client.apply_batch([carla.command.DestroyActor(x) for x in client.get_world().get_actors() if 'pedestrian' in x.type_id])
        
        print('done.')


if __name__ == '__main__':

    main()