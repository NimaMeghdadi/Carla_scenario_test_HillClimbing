import carla
import time
import csv
import glob
import os
import sys
import json
import pandas as pd
import json
from csv import writer
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
    distance_ped_starts = [9,10]
    distance_car_start = 45
    speed_cars=[35,34]
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
        write_csv(reset=True)
        for distance_ped_start in distance_ped_starts:
            for speed_car in speed_cars:
                collision= start_scenario(client,
                                        world,
                                        vehicle,
                                        pedestrian,
                                        detect_collision,
                                        distance_ped_start,
                                        distance_car_start,
                                        speed_car,
                                        speed_ped)
                write_csv(round(collision,2),speed_car,distance_ped_start)
        
        
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
        destroy_actors(client)
        print('done.')
        


def start_scenario(client,world,vehicle,pedestrian,detect_collision,distance_ped_start,distance_car_start,speed_car,speed_ped):
    car = vehicle.create(client,world,distance=distance_car_start,speed=speed_car)
    ped = pedestrian.create(world)
    # add to actor list
    
    vehicle.start(car)
    
    distances_ped_car = []
    collision_sensor = detect_collision.detect(world,car)
    collision_sensor.listen(lambda event: distances_ped_car.append(0) )
    # illustrate the movement of the pedestrian and the vehicles
    for i in range(0,2500):
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
        if i > 5 and distances_ped_car[-1] > distances_ped_car[-2] : break 
        time.sleep(0.01)
    print(f'Report: distance car stop: {distances_ped_car[-2]} speed car: {speed_car} distance: {distance_ped_start} speed pedestrian: {speed_ped}')
    destroy_actors(client)
    world.wait_for_tick()
    return distances_ped_car[-2]

def destroy_actors(client):
    client.apply_batch([carla.command.DestroyActor(x) for x in client.get_world().get_actors() if 'vehicle' in x.type_id])
    client.apply_batch([carla.command.DestroyActor(x) for x in client.get_world().get_actors() if 'walker' in x.type_id])
    client.apply_batch([carla.command.DestroyActor(x) for x in client.get_world().get_actors() if 'sensor' in x.type_id])




def write_csv(collision=-1,speed_car=-1,start_distance=-1,reset=False):
    if reset:
        with open('result.csv', 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=' ',
                                    quotechar=' ', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(['collision'] +["speed_car"] + ['distance_ped_start'])
    else:
        List=[collision,speed_car,start_distance]
        with open('result.csv', 'a', newline='') as csvfile:
            writer_object = writer(csvfile)
            writer_object.writerow(List)
    
    


 
 
# function to add to JSON
def write_json(new_data, filename='data.json'):
    with open(filename,'r+') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data["collision_detail"].append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4)
 
    # python object to be appended

     


def distance(x1,y1,x2,y2):
    return ((x1-x2)**2+(y1-y2)**2)**0.5


if __name__ == '__main__':

    main()