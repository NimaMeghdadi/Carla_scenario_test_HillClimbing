import carla
import random
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


def main():
    actor_list = []
    car = actors.vehicle.Car()
    pedestrian = actors.pedestrian.Pedestrian()
    try:
        # Setup Carla settings
        client = carla.Client('localhost', 2000)
        client.set_timeout(20.0)
        world = client.get_world() 
        
        # change map if nessary
        if world.get_map().name != 'Carla/Maps/Town01':
            print("Town01 is loading")
            client.set_timeout(1000.0)
            world = client.load_world('Town01')
        world.wait_for_tick()
        
        # creat the pedestrian and car
        car = car.create_car(client,world,speed=300, distance=42)
        time.sleep(4.5)
        ped = pedestrian.create_pedestrian(world)
        
        # add to actor list
        actor_list.append(car)
        actor_list.append(ped)
        
        # illustrate the movement of the pedestrian and the vehicles
        for i in range(0,100):
                print("step: ",i)
                print("pedestrian",ped.get_location())
                print("car",car.get_location())
                # print("car speed: ",car.get_speed())
                print ("watcher: ",world.get_spectator().get_location())
                time.sleep(1)
                
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

# def spector():
#     spec = world.get_spectator()
#     spaw = world.get_map().get_spawn_points()
#     start = spaw[0]
#     spe_pos = carla.Transform(start.location+carla.Location(z=50),carla.Rotation(pitch=-90))
#     spec.set_transform(spe_pos)
    

if __name__ == '__main__':

    main()