import carla
import time

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
import  actors
import sensors


def main():
    distance_ped_start = 8
    distance_car_start = 45
    speed_car=34
    speed_ped = 0.2
    
    actor_list = []
    vehicle = actors.vehicle.Car()
    pedestrian = actors.pedestrian.Pedestrian()
    detect_collision = sensors.collision_detector.CollisionDetector()
    try:
        # Setup Carla settings
        client = carla.Client('localhost', 2000)
        client.set_timeout(20.0)
        world = client.get_world() 
        
        # change map if needed
        if world.get_map().name != 'Carla/Maps/Town01':
            print("Town01 is loading")
            client.set_timeout(1000.0)
            world = client.load_world('Town01')
        world.wait_for_tick()
        
        # create the pedestrian and car
        car = vehicle.create_car(client,world,distance=distance_car_start,speed=speed_car)
        ped = pedestrian.create_pedestrian(world)
        
        
        # add to actor list
        actor_list.append(car)
        actor_list.append(ped)
        
        vehicle.start(car)
        
        distances_ped_car = []
        collision_sensor = detect_collision.detect(world,car)
        collision = collision_sensor.listen(lambda event: distances_ped_car.append(0) )
        # illustrate the movement of the pedestrian and the vehicles
        for i in range(0,10000000):
            distance_ped_car = distance(ped.get_location().x,ped.get_location().y,car.get_location().x-2.7,car.get_location().y)
            distances_ped_car.append(distance_ped_car)
            print("step: ",i)
            print(f"pedestrian: {ped.get_location()}")
            print(f"car: {car.get_location()}")
            print(f"distance: {distances_ped_car[-1]}")
            print (f"watcher: {world.get_spectator().get_location()}")
            if distances_ped_car[-1] < distance_ped_start:
                pedestrian.start(ped,speed = speed_ped)
                print("pedestrian is moving")
            if i > 6 and distances_ped_car[-1] > distances_ped_car[-2]+1 : break 
            time.sleep(0.1)
    except ValueError:
        print(ValueError)
    except KeyboardInterrupt:
        print('\nCancelled by user. Bye!')
    except RuntimeError:
        print(RuntimeError)
    except Exception as e:
        client.apply_batch([carla.command.DestroyActor(x) for x in client.get_world().get_actors() if 'vehicle' in x.type_id])
        print(e)
    finally:
        print('destroying actors')
        client.apply_batch([carla.command.DestroyActor(x) for x in client.get_world().get_actors() if 'vehicle' in x.type_id])
        client.apply_batch([carla.command.DestroyActor(x) for x in client.get_world().get_actors() if 'walker' in x.type_id])
        
        for actor in actor_list:
            actor.destroy()
        print('done.')
        print(f'Report: distance car stop:{distances_ped_car[-2]} speed car: {speed_car} distance: {distance_ped_start} speed pedestrian: {speed_ped}')


def distance(x1,y1,x2,y2):
    return ((x1-x2)**2+(y1-y2)**2)**0.5




if __name__ == '__main__':

    main()