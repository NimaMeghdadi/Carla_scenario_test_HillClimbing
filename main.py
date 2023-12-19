import carla
import os,sys, glob
import numpy as np
import matplotlib.pyplot as plt
import random
import itertools
from itertools import permutations
import pickle
import constant
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
    # Instantiate classes
    hc = search_alg.hill_climbing.HillClimbing()
    vehicle = actors.vehicle.Car()
    pedestrian = actors.pedestrian.Pedestrian()
    detect_collision = sensors.collision_detector.CollisionDetector()
    mlp = neural_network.mlpregressor.MlpRegressor()
    hp = helpers.Helpers()
    rm = search_alg.random_search.RandomSearch()
    # Set up parameters
    # distance_car_start,distance_ped_starts,speed_cars,speed_peds = hp.params(step_distance_ped_starts=2,
    #                                         step_speed_cars=2,
    #                                         step_speed_peds=2)
    # Welcome text
    scenario_runner,train,run_search = hp.welcome_text()
    # Set up carla and run scenario
    if scenario_runner == 1:
        distance_car_start,distance_ped_starts,speed_cars,speed_peds = hp.params(step_distance_ped_starts=10,
                                        step_speed_cars=20,
                                        step_speed_peds=5)
        client,world = hp.set_up_carla()
        hp.scenario_runner(client,world,vehicle,pedestrian,
                            detect_collision,distance_ped_starts,
                            distance_car_start,speed_cars,speed_peds)
    # Train model
    if train == 1:
        model = mlp.train(name_csv="result3.csv",
                            y_name="collision_time",
                            save_name="collision_time5_model")

        model = mlp.train(name_csv="result3.csv",
                            y_name="collision_distance",
                            save_name="collision_distance5_model")
    # Run search algorithms
    if run_search == 1:
        # Set up parameters
        distance_car_start,distance_ped_starts,speed_cars,speed_peds = hp.params(step_distance_ped_starts=100,
                                        step_speed_cars=200,
                                        step_speed_peds=100)
        for _ in range(10):
            x=[random.choice(speed_cars),random.choice(distance_ped_starts),random.choice(speed_peds)]
            # Hill climbing
            opt_hc,hc_selected_y,hc_selected_y1 = hc.optimize(distance_ped_starts,
                                                                        speed_cars,speed_peds,
                                                                        x=x,
                                                                        no_model=5)
            # Random search
            opt_rs,selected_y,selected_y1 = rm.optimize(distance_ped_starts,
                                                        speed_cars,speed_peds,
                                                        iteration = len(hc_selected_y)-1,
                                                        x=x,no_model=5)
            # illustrate result
            nn_distance = pickle.load(open(constant.MODEL_DIR+"collision_distance4_model.pickle", "rb"))
            nn_time = pickle.load(open(constant.MODEL_DIR+"collision_time4_model.pickle", "rb"))
            scaler = pickle.load(open(constant.MODEL_DIR+"scaler.pickle", "rb"))
            # print("hill",opt_hc,mlp.predict(opt_hc))
            # print("random search",opt_rs,mlp.predict(opt_rs))
            # print("hill_select",hc_selected_y)
            # print("random_select",selected_y)
            
            # Plot
            fig, (ax1, ax2) = plt.subplots(1, 2)
            fig.suptitle("Compare Hill Climbing and Random Search")
            ax1.set_title("Distance to collision")
            ax2.set_title("Time to collision")
            ax1.plot(hc_selected_y, label = "HC")
            ax2.plot(hc_selected_y1, label = "HC")
            ax1.plot(selected_y, label = "RS")
            ax2.plot(selected_y1, label = "RS")
            ax1.set(xlabel='Iteration', ylabel='Distance to collision')
            ax2.set(xlabel='Iteration', ylabel='time to collision')
            plt.legend()
            plt.show()
        
    # except ValueError:
    #     print(ValueError)
    
    # except KeyboardInterrupt:
    #     print('\nCancelled by user. Bye!')
    
    # except RuntimeError:
    #     print(RuntimeError)
    
    # except Exception as e:
    #     print(e)
    
        
if __name__ == '__main__':
    main()