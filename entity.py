from config import SCREEN_SIZE
from random import randint
from gameobjects.vector2 import Vector2
from state import StateMachine, AntStateExploring, AntStateSeeking, AntStateDelivering, AntStateHunting


class SimulationEntity(object):
    """
    The Base Class for the simulation Entity.
    """

    def __init__(self, world, name, image):
        """
        Constructor of the SimulationEntity instance.

        :param world: The world which the entity belongs
        :param name: Name of the entity
        :param image: Sprite of the entity
        """
        self.world = world
        self.name = name
        self.image = image
        self.location = Vector2(0, 0)
        self.destination = Vector2(0, 0)
        self.speed = 0.
        self.id = 0
        self.brain = StateMachine()

    def render(self, surface):
        """
        Draw the entity.

        :param surface: pygame surface object
        """
        x, y = self.location
        w, h = self.image.get_size()
        surface.blit(self.image, (x - w / 2, y - h / 2))

    def process(self, time_passed):
        """
        Process the entity data.

        :param time_passed: Time passed since the last render
        """
        self.brain.think()

        if self.speed > 0. and self.location != self.destination:
            vec_to_destination = self.destination - self.location
            distance_to_destination = vec_to_destination.get_length()
            heading = vec_to_destination.get_normalized()
            travel_distance = min(distance_to_destination, time_passed * self.speed)
            self.location += travel_distance * heading


class Ant(SimulationEntity):
    """
    The Ant Entity Class
    """

    def __init__(self, world, image):
        """
        Constructor of the Ant instance.

        :param world: The world which the entity belongs
        :param image: Sprite of the Ant
        """

        SimulationEntity.__init__(self, world, "ant", image)

        exploring_state = AntStateExploring(self)
        seeking_state = AntStateSeeking(self)
        delivering_state = AntStateDelivering(self)
        hunting_state = AntStateHunting(self)

        self.brain.add_state(exploring_state)
        self.brain.add_state(seeking_state)
        self.brain.add_state(delivering_state)
        self.brain.add_state(hunting_state)

        self.carry_image = None

    def carry(self, image):
        """
        Set carry image.

        :param image: the carry image
        """

        self.carry_image = image

    def drop(self, surface):

        if self.carry_image:
            x, y = self.location
            w, h = self.carry_image.get_size()
            surface.blit(self.carry_image, (x - w, y - h / 2))
            self.carry_image = None

    def render(self, surface):
        """
        Draw the ant.

        :param surface: pygame surface object
        """

        SimulationEntity.render(self, surface)

        if self.carry_image:
            x, y = self.location
            w, h = self.carry_image.get_size()
            surface.blit(self.carry_image, (x - w, y - h / 2))


class Leaf(SimulationEntity):
    """
    The Leaf Entity Class
    """

    def __init__(self, world, image):
        """
        Constructor of the Leaf instance.

        :param world: The world which the entity belongs
        :param image: Sprite of the Leaf
        """
        SimulationEntity.__init__(self, world, "leaf", image)


class Spider(SimulationEntity):
    """
    The Spider Entity Class
    """

    def __init__(self, world, image, dead_image):
        """
        Constructor of the Spider instance.

        :param world: The world which the entity belongs
        :param image: Sprite of the default spider
        :param dead_image: Sprite of the dead spider
        """

        SimulationEntity.__init__(self, world, "spider", image)
        self.dead_image = dead_image
        self.health = 35
        self.speed = 50. + randint(-20, 20)

    def bitten(self):
        """
        Execute when spider has been bitten.
        """

        self.health -= 1
        if self.health <= 0:
            self.speed = 0.
            self.image = self.dead_image
        self.speed = 140.

    def render(self, surface):
        """
        Draw the spider.

        :param surface: pygame surface object
        """

        SimulationEntity.render(self, surface)

        # Draw a health bar
        x, y = self.location
        w, h = self.image.get_size()
        bar_x = x - 12
        bar_y = y + h / 2
        surface.fill((255, 0, 0), (bar_x, bar_y, 25, 4))
        surface.fill((0, 255, 0), (bar_x, bar_y, self.health, 4))

    def process(self, time_passed):
        """
        Process the spider data.

        :param time_passed: Time passed since the last render
        """

        x, y = self.location
        if x > SCREEN_SIZE[0] + 2:
            self.world.remove_entity(self)
            return

        SimulationEntity.process(self, time_passed)
