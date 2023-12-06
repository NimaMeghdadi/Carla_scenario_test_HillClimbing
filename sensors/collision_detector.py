import carla

class CollisionDetector:
    def __init__(self):
        pass
    def detect(self,world, car):
        blueprint_library = world.get_blueprint_library()
        collision_sensor = world.spawn_actor(blueprint_library.find('sensor.other.collision'),
                                        carla.Transform(), attach_to=car)
        return collision_sensor
        