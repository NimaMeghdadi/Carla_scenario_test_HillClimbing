import carla
import os,sys, glob
import numpy as np

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
    # parameters
    actor_list = []
    
    hill_climbing = search_alg.hill_climbing.HillClimbing()
    vehicle = actors.vehicle.Car()
    pedestrian = actors.pedestrian.Pedestrian()
    detect_collision = sensors.collision_detector.CollisionDetector()
    mlp = neural_network.mlpregressor.MlpRegressor()
    hp = helpers.Helpers()
    
    distance_car_start,distance_ped_starts,speed_cars,speed_peds = hp.params()
    try:
        scenario_runner,train,run_hill_climbing = hp.welcome_text()

        if scenario_runner == 1:
            client,world = hp.set_up_carla()
            hp.scenario_runner(client,world,vehicle,pedestrian,detect_collision,distance_ped_starts,distance_car_start,speed_cars,speed_peds)
        if train == 1:
            model = mlp.train(y_name="collision_time")
            model = mlp.load_model(name="collision_time_model.pickle")
        if run_hill_climbing == 1:
            distance_car_start,distance_ped_starts,speed_cars,speed_peds = hp.params(step_distance_ped_starts=100,step_speed_cars=100,step_speed_peds=100)
            opt = hill_climbing.optimize(distance_ped_starts,speed_cars,speed_peds,model_name='collision_time_model.pickle')
            print(opt,mlp.predict(opt))
            
        
    except ValueError:
        print(ValueError)
    except KeyboardInterrupt:
        print('\nCancelled by user. Bye!')
    except RuntimeError:
        print(RuntimeError)
    except Exception as e:
        print(e)
    finally:
        print('done.')
        
if __name__ == '__main__':



    main()