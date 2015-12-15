import pygame
from pygame.locals import *
from entity import Ant, Leaf, Spider
from random import randint
from gameobjects.vector2 import Vector2
from config import ANT_COUNT, SCREEN_SIZE, NEST_POSITION, NEST_SIZE


class World(object):
    """
    The World class that the simulation entities live in.
    It contain the nest, represented by a circle in the center of the screen, and a number of Ants, Spiders and Leafs
    entities.
    """
    
    def __init__(self):
        
        self.entities = {}
        self.entity_id = 0
        # Draw the nest (a circle) on the background
        self.background = pygame.surface.Surface(SCREEN_SIZE).convert()
        self.background.fill((255, 255, 255))
        pygame.draw.circle(self.background, (200, 222, 187), NEST_POSITION, int(NEST_SIZE))
        
    def add_entity(self, entity):
        """
        Stores the entity then advances the current id.

        :param entity: The entity instance to be added
        :return:
        """
        
        self.entities[self.entity_id] = entity
        entity.id = self.entity_id
        self.entity_id += 1
        
    def remove_entity(self, entity):
        """
        Remove the entity from the world.

        :param entity: The entity instance to be removed
        :return:
        """
        
        del self.entities[entity.id]
                
    def get(self, entity_id):
        """
        Find the entity, given its id (or None if it is not found).

        :param entity_id: The ID of the entity
        :return:
        """
        
        if entity_id in self.entities:
            return self.entities[entity_id]
        else:
            return None
        
    def process(self, time_passed):
        """
        Process every entity in the world.

        :param time_passed: Time passed since the last render
        """
                
        time_passed_seconds = time_passed / 1000.0        
        for entity in self.entities.values():
            entity.process(time_passed_seconds)
            
    def render(self, surface):
        """
        Draw the background and all the entities.

        :param surface: The pygame surface
        """
        
        surface.blit(self.background, (0, 0))
        for entity in self.entities.itervalues():
            entity.render(surface)
            
    def get_close_entity(self, name, location, distance_range=100.):
        """
        Find an entity within range of a location.

        :param name: Name of the entity
        :param location: location
        :param distance_range: The circular distance of the range (circular "field of view")
        """
        
        location = Vector2(*location)        
        
        for entity in self.entities.itervalues():            
            if entity.name == name:                
                distance = location.get_distance_to(entity.location)
                if distance < distance_range:
                    return entity        
        return None

    
def run():
    
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)

    pygame.display.set_caption('Ant Simulation')
        
    world = World()
    
    w, h = SCREEN_SIZE
    
    clock = pygame.time.Clock()
    
    ant_image = pygame.image.load("ant.png").convert_alpha()
    leaf_image = pygame.image.load("leaf.png").convert_alpha()
    spider_image = pygame.image.load("spider.png").convert_alpha()
    
    for ant_no in xrange(ANT_COUNT):
        
        ant = Ant(world, ant_image)
        ant.location = Vector2(randint(0, w), randint(0, h))
        ant.brain.set_state("exploring")
        world.add_entity(ant)
    
    full_screen = False
    while True:
        
        for event in pygame.event.get():
            if event.type == QUIT:
                return        
        if event.type == KEYDOWN:
            if event.key == K_f:
                full_screen = not full_screen
                if full_screen:
                    screen = pygame.display.set_mode(SCREEN_SIZE, FULLSCREEN, 32)
                else:
                    screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
        
        time_passed = clock.tick(30)
        
        if randint(1, 10) == 1:
            leaf = Leaf(world, leaf_image)
            leaf.location = Vector2(randint(0, w), randint(0, h))
            world.add_entity(leaf)
            
        if randint(1, 100) == 1:
            # Make a 'dead' spider image by turning it upside down
            spider = Spider(world, spider_image, pygame.transform.flip(spider_image, 0, 1))
            spider.location = Vector2(-50, randint(0, h))
            spider.destination = Vector2(w+50, randint(0, h))            
            world.add_entity(spider)
        
        world.process(time_passed)
        world.render(screen)
        
        pygame.display.update()


if __name__ == "__main__":    
    run()

