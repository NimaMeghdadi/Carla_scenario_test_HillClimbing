import carla
import time
import csv
import os,sys, glob
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from csv import writer

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import actors
import sensors
import neural_network
import search_alg
import helpers

def main():
    distance_car_start = 45
    # distance_ped_starts = [9,10,12,15,17,20]
    # speed_cars=[35,40,50,55,60,70,80]
    # speed_peds = [0.2,0.3,0.4]
    distance_ped_starts = np.linspace(9.0, 20.0, num=100)
    speed_cars = np.linspace(30.8, 80.0, num=100)
    speed_peds = np.linspace(0.2, 0.5, num=50)
    actor_list = []
    
    hill_climbing = search_alg.hill_climbing.HillClimbing()
    vehicle = actors.vehicle.Car()
    pedestrian = actors.pedestrian.Pedestrian()
    detect_collision = sensors.collision_detector.CollisionDetector()
    mlp = neural_network.mlpregressor.MlpRegressor()
    hp = helpers.Helpers()
    try:
        print("Welcome to Carla scenario test")
        print("here we have 3 parameters:if you don't want to change it, just press enter. This will run default setting which is just run Hill Climbing algorithm in pre designed dataset")
        print("1: yes 0: no")
        scenario_runner = raw_input("run scenario runner?(this will require to open carla)")
        train = raw_input("you want to train the mlp regressor on result csv?")
        hill_climbing = raw_input("run Hill Climbing algorithm?")
        if scenario_runner == "1":
            client,world = hp.set_up_carla()
            hp.scenario_runner(client,world,vehicle,pedestrian,detect_collision,distance_ped_starts,distance_car_start,speed_cars,speed_peds)
        if train == "1":
            model = mlp.train()
            model = mlp.load_model()
        if hill_climbing == "1":
            opt = hill_climbing.optimize(distance_ped_starts,speed_cars,speed_peds)
            print(opt,mlp.predict(opt))
        
        # Setup Carla settings
        # client,world = hp.set_up_carla()
        # hp.scenario_runner(client,world,vehicle,pedestrian,detect_collision,distance_ped_starts,distance_car_start,speed_cars,speed_peds)
        
        # model = mlp.train() 
        # model = mlp.load_model()
        # result = mlp.predict([40,9,0.2],model)
        # print(result)
        
    except ValueError:
        print(ValueError)
    except KeyboardInterrupt:
        print('\nCancelled by user. Bye!')
    except RuntimeError:
        print(RuntimeError)
    except Exception as e:
        # client.apply_batch([carla.command.DestroyActor(x) for x in client.get_world().get_actors() if 'vehicle' in x.type_id])
        print(e)
    finally:
        # destroy_actors(client)
        print('done.')
        



if __name__ == '__main__':

    main()