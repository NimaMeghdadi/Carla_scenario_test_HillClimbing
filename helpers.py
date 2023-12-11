import carla
import time
import csv
import glob
import os
import sys
import json
import pandas as pd
import json
import numpy as np
from csv import writer
try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

class Helpers:
    def __init__(self):
        pass
    def set_up_carla(self):
        client = carla.Client('localhost', 2000)
        client.set_timeout(20.0)
        world = client.get_world()
        self.change_map(world,client)
        return client,world
        
    def change_map(self,world,client):
        if world.get_map().name != 'Carla/Maps/Town01':
            print("Town01 is loading")
            client.set_timeout(1000.0)
            world = client.load_world('Town01')
        world.wait_for_tick()

    def scenario_runner(self,client,world,vehicle,pedestrian,detect_collision,distance_ped_starts,distance_car_start,speed_cars,speed_peds):
        self.write_csv(reset=True)
        for speed_ped in speed_peds:
                for distance_ped_start in distance_ped_starts:
                    for speed_car in speed_cars:
                        collision= self.start_scenario(client,
                                                world,
                                                vehicle,
                                                pedestrian,
                                                detect_collision,
                                                distance_ped_start,
                                                distance_car_start,
                                                speed_car,
                                                speed_ped)
                        self.write_csv(collision,speed_car,distance_ped_start,speed_ped)

    def start_scenario(self,client,world,vehicle,pedestrian,detect_collision,distance_ped_start,distance_car_start,speed_car,speed_ped):
        car = vehicle.create(client,world,distance=distance_car_start,speed=speed_car)
        ped = pedestrian.create(world)
        # add to actor list
        
        vehicle.start(car)
        
        distances_ped_car = []
        collision_sensor = detect_collision.detect(world,car)
        collision_sensor.listen(lambda event:   distances_ped_car.append(0) )
        # illustrate the movement of the pedestrian and the vehicles
        for i in range(0,1000):
            distance_ped_car = self.distance(ped.get_location().x,ped.get_location().y,car.get_location().x-2.7,car.get_location().y)
            distances_ped_car.append(distance_ped_car)
            # print("step: ",i)
            # print(f"pedestrian: {ped.get_location()}")
            # print(f"car: {car.get_location()}")
            # print(f"distance: {distances_ped_car[-1]}")
            # print (f"watcher: {world.get_spectator().get_location()}")
            if distances_ped_car[-1] < distance_ped_start:
                pedestrian.start(ped,speed = speed_ped)
                # print("pedestrian is moving")
            if ped.get_location() == carla.Location(y=135): break
            time.sleep(0.01)
        print(distances_ped_car)
        print(f'Report: distance car stop: {min(distances_ped_car)} speed car: {speed_car} distance: {distance_ped_start} speed pedestrian: {speed_ped}')
        self.destroy_actors(client)
        world.wait_for_tick()
        return min(distances_ped_car)

    def destroy_actors(self,client):
        print('destroying actors')
        client.apply_batch([carla.command.DestroyActor(x) for x in client.get_world().get_actors() if 'vehicle' in x.type_id])
        client.apply_batch([carla.command.DestroyActor(x) for x in client.get_world().get_actors() if 'walker' in x.type_id])
        client.apply_batch([carla.command.DestroyActor(x) for x in client.get_world().get_actors() if 'sensor' in x.type_id])




    def write_csv(self,collision=-1,speed_car=-1,start_distance=-1,speed_ped = -1,reset=False):
        if reset:
            with open('./neural_network/result.csv', 'w', newline='') as csvfile:
                spamwriter = csv.writer(csvfile, delimiter=',',
                                        quotechar=',', quoting=csv.QUOTE_MINIMAL)
                spamwriter.writerow(['collision'] +["speed_car"] + ['distance_ped_start']+['speed_ped'])
        else:
            List=[collision,speed_car,start_distance,speed_ped]
            with open('result.csv', 'a', newline='') as csvfile:
                writer_object = writer(csvfile)
                writer_object.writerow(List)
    
        # python object to be appended
    def distance(self,x1,y1,x2,y2):
        return ((x1-x2)**2+(y1-y2)**2)**0.5