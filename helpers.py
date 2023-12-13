import carla
import time
import csv
from csv import writer
import numpy as np

import glob,os, sys
try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import constant

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
                        collision_distance, collision_time = self.start_scenario(client,
                                                world,
                                                vehicle,
                                                pedestrian,
                                                detect_collision,
                                                distance_ped_start,
                                                distance_car_start,
                                                speed_car,
                                                speed_ped)
                        self.write_csv(collision_distance,collision_time,speed_car,distance_ped_start,speed_ped)

    def start_scenario(self,client,world,vehicle,pedestrian,detect_collision,distance_ped_start,distance_car_start,speed_car,speed_ped):
        try:
            car = vehicle.create(client,world,distance=distance_car_start,speed=speed_car)
            ped = pedestrian.create(world)
            
            vehicle.start(car)
            
            distances_ped_car = []
            TTC = []
            collision_sensor = detect_collision.detect(world,car)
            collision_sensor.listen(lambda event:   distances_ped_car.append(0) )
            # collision_sensor.listen(lambda event:   TTC.append(0) )
            for i in range(0,1000):
                distance_ped_car = self.distance(ped.get_location().x,ped.get_location().y,car.get_location().x-2.7,car.get_location().y)
                distances_ped_car.append(distance_ped_car)
                TTC.append(self.time_to_collision(car,ped))
                # print("step: ",i)
                # print(f"pedestrian: {ped.get_location()}")
                # print(f"car: {-(car.get_velocity().x*3.6)}")
                # print(f"time collision: {self.time_to_collision(car,ped)}")
                # print(f"distance: {distances_ped_car[-1]}")
                # print (f"watcher: {world.get_spectator().get_location()}")
                if distances_ped_car[-1] < distance_ped_start:
                    pedestrian.start(ped,speed = speed_ped)
                if ped.get_location() == carla.Location(y=135): break
                time.sleep(0.01)
            print(f'Report: distance car stop: {min(distances_ped_car)} speed car: {speed_car} distance: {distance_ped_start} speed pedestrian: {speed_ped}')
            world.wait_for_tick()
            if min(distances_ped_car) == 0:
                TTC.append(0)
        finally:
            self.destroy_actors(client)
            world.wait_for_tick()
        return min(distances_ped_car), min (TTC)

    def destroy_actors(self,client):
        print('destroying actors')
        client.apply_batch([carla.command.DestroyActor(x) for x in client.get_world().get_actors() if 'vehicle' in x.type_id])
        client.apply_batch([carla.command.DestroyActor(x) for x in client.get_world().get_actors() if 'walker' in x.type_id])
        client.apply_batch([carla.command.DestroyActor(x) for x in client.get_world().get_actors() if 'sensor' in x.type_id])




    def write_csv(self,collision_distance=-1,collision_time=-1,speed_car=-1,start_distance=-1,speed_ped = -1,reset=False):
        if reset:
            with open(constant.DATA_DIR +'result.csv', 'w', newline='') as csvfile:
                spamwriter = csv.writer(csvfile, delimiter=',',
                                        quotechar=',', quoting=csv.QUOTE_MINIMAL)
                spamwriter.writerow(['collision_distance'] +["collision_time"]+["speed_car"] + ['distance_ped_start']+['speed_ped'])
        else:
            List=[collision_distance,collision_time,speed_car,start_distance,speed_ped]
            with open(constant.DATA_DIR+'result.csv', 'a', newline='') as csvfile:
                writer_object = writer(csvfile)
                writer_object.writerow(List)
    
        # python object to be appended
    def distance(self,x1,y1,x2,y2):
        return ((x1-x2)**2+(y1-y2)**2)**0.5
    
    def time_to_collision(self,car,ped):
        distance = self.distance(car.get_location().x,car.get_location().y,ped.get_location().x,ped.get_location().y)
        speed = abs(car.get_velocity().x)
        if speed == 0:
            speed = 0.000000001
        time_collision = distance/speed
        return time_collision
    
    def welcome_text(self):
        print("Welcome to Carla scenario test")
        print("here we have 3 parameters:if you don't want to change it, just press enter. This will run default setting which is just run Hill Climbing algorithm in pre designed dataset")
        print("1: yes 0: no")
        scenario_runner = int(input("run scenario runner?(this will require to open carla and takes time default = 0): ") or "0")
        train = int(input("you want to train the mlp regressor on result csv?(default = 0): ") or "0")
        run_hill_climbing = int(input("run Hill Climbing algorithm?(default = 1): ") or "1")
        
        return scenario_runner,train,run_hill_climbing
    
    def params(self,s_distance_ped_starts = 5,e_distance_ped_starts=20,step_distance_ped_starts=10,s_speed_cars=30,e_speed_cars=80,step_speed_cars=10,s_speed_peds=0.2,e_speed_peds=0.5,step_speed_peds=3):
        
        distance_car_start = 45
        distance_ped_starts = np.linspace(s_distance_ped_starts, e_distance_ped_starts, num= step_distance_ped_starts)
        speed_cars = np.linspace(s_speed_cars, e_speed_cars, num=step_speed_cars)
        speed_peds = np.linspace(s_speed_peds, e_speed_peds, num=step_speed_peds)
        
        return distance_car_start,distance_ped_starts,speed_cars,speed_peds