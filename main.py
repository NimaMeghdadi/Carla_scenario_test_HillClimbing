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
    distance_car_start = 45
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
        scenario_runner,train,run_hill_climbing = hp.welcome_text()

        if scenario_runner == 1:
            client,world = hp.set_up_carla()
            hp.scenario_runner(client,world,vehicle,pedestrian,detect_collision,distance_ped_starts,distance_car_start,speed_cars,speed_peds)
        if train == 1:
            model = mlp.train()
            model = mlp.load_model()
        if run_hill_climbing == 1:
            opt = hill_climbing.optimize(distance_ped_starts,speed_cars,speed_peds)
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