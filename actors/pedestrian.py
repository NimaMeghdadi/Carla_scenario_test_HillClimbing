
import sys
import random
import carla

sys.path.append('D:\carla0.9.13\PythonAPI\carla')
from agents.navigation.basic_agent import BasicAgent

class Pedestrian:
    def __init__(self):
        pass
    
    def create_pedestrian(self,world):
        try:
            # Blueprint of the pedestrian
            ped_bp=world.get_blueprint_library().filter("walker.pedestrian.*")
            # controller_bp = world.get_blueprint_library().find('controller.ai.walker')
            
            # transform of the pedestrian
            ped_loc = carla.Location(x=225, y=127, z=1)
            ped_trans = carla.Transform(ped_loc)
            
            #spawn the pedestrian
            walker = random.choice(ped_bp)
            actor = world.spawn_actor(walker, ped_trans)
            # actor.WalkerControl
            world.wait_for_tick()
            
            
            
            # controller = world.spawn_actor(controller_bp, carla.Transform(),actor)
            # world.wait_for_tick()
            
            # time.sleep(1)
            # set the destination of the pedestrian
            # controller.start()
            # controller.go_to_location(carla.Location(x=225, y=139, z=1))
            # world.wait_for_tick()
            print("pedestrian was created")
            return actor
        except:
            print('exception: may be the location of the pedestrian is not valid')
    
    def start(self,actor,speed = 0.2):
        actor.apply_control(
                    carla.WalkerControl(speed = speed,direction=carla.Vector3D(0, 8, 0),))
