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
        traffic_manager = client.get_trafficmanager(8000)
        world = client.get_world()

        blueprint_library = world.get_blueprint_library()
        bp = random.choice(blueprint_library.filter('vehicle'))

        transform = random.choice(world.get_map().get_spawn_points())
        print("below is transform")
        # print(transform.location)
        vehicle = world.spawn_actor(bp, transform)
        time.sleep(5)
        # print("below is vehicle")
        print(vehicle.get_location())
        vehicle.set_autopilot( True,traffic_manager.get_port())
        # world.tick()
        # SetAutopilot = carla.command.SetAutopilot
        # SetAutopilot(vehicle, True, traffic_manager.get_port())
        # tm_port = traffic_manager.get_port()
        # for v in actor_list:
        #     v.set_autopilot(True,tm_port)
        actor_list.append(vehicle)
        print('created %s' % vehicle.type_id)
        time.sleep(20)


        # camera_bp = blueprint_library.find('sensor.camera.depth')
        # camera_transform = carla.Transform(carla.Location(x=1.5, z=2.4))
        # camera = world.spawn_actor(camera_bp, camera_transform, attach_to=vehicle)


      
        # print("below is 2 location")
        # print(vehicle.get_location())
        # location = vehicle.get_location()
        # location.x += 40
        # vehicle.set_location(location)
        # print('moved vehicle to %s' % location)

      

        time.sleep(5)

    finally:

        print('destroying actors')
        for actor in actor_list:
            actor.destroy()
        print('done.')


if __name__ == '__main__':

    main()