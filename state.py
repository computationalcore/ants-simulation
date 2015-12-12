from random import randint
from gameobjects.vector2 import Vector2
from config import SCREEN_SIZE, NEST_POSITION, NEST_SIZE


class State(object):
    """
    Base Class for a State
    """
    def __init__(self, name):
        self.name = name

    def do_actions(self):
        pass

    def check_conditions(self):
        pass

    def entry_actions(self):
        pass

    def exit_actions(self):
        pass


class StateMachine(object):
    """
    The class that manage all states.
    The StateMachine class stores an instance of each of the states in a dictionary and manages the currently active
    state.
    """
    def __init__(self):
        """
        Class constructor that initialize states dictionary and set state to none.
        """

        self.states = {}
        self.active_state = None

    def add_state(self, state):
        """
        Add a instance to the internal dictionary.
        :param state: the name of the state
        """
        self.states[state.name] = state

    def think(self):
        """
        Runs once per frame,
        :return:
        """

        # Only continue if there is an active state
        if self.active_state is None:
            return
        # Perform the actions of the active state, and check conditions
        self.active_state.do_actions()

        new_state_name = self.active_state.check_conditions()
        if new_state_name is not None:
            self.set_state(new_state_name)

    def set_state(self, new_state_name):
        """
        Change states and perform any exit / entry actions.

        :param new_state_name: name of the state to be set
        """

        if self.active_state is not None:
            self.active_state.exit_actions()

        self.active_state = self.states[new_state_name]
        self.active_state.entry_actions()


class AntStateExploring(State):
    """
    The Exploring State for Ants.
    The ant moves randomly over the screen area.
    """
    def __init__(self, ant):
        """
        Call the base class constructor to initialize the State.

        :param ant: ant instance that this state belongs to
        """

        State.__init__(self, "exploring")
        self.ant = ant

    def random_destination(self):
        """
        Select a point randomly in the screen
        """

        w, h = SCREEN_SIZE
        self.ant.destination = Vector2(randint(0, w), randint(0, h))

    def do_actions(self):
        """
        Change ant direction, 1 in 20 calls
        """

        if randint(1, 20) == 1:
            self.random_destination()

    def check_conditions(self):
        """
        Check conditions of the ant and environment to decide if state should change.
        """

        # If there is a nearby leaf, switch to seeking state
        leaf = self.ant.world.get_close_entity("leaf", self.ant.location)
        if leaf is not None:
            self.ant.leaf_id = leaf.id
            return "seeking"

        # If there is a nearby spider, switch to hunting state
        spider = self.ant.world.get_close_entity("spider", NEST_POSITION, NEST_SIZE)
        if spider is not None:
            if self.ant.location.get_distance_to(spider.location) < 100.:
                self.ant.spider_id = spider.id
                return "hunting"

        return None

    def entry_actions(self):
        """
        Actions executed by the ant when it enter explore state.
        """

        # Start with random speed and heading
        self.ant.speed = 120. + randint(-30, 30)
        self.random_destination()


class AntStateSeeking(State):
    """
    The Seeking State for Ants.
    The ant moves toward a leaf that gets closer to it.
    """

    def __init__(self, ant):
        """
        Call the base class constructor to initialize the State.
        :param ant: ant instance that this state belongs to
        """

        State.__init__(self, "seeking")
        self.ant = ant
        self.leaf_id = None

    def check_conditions(self):
        """
        Check conditions of the ant and environment to decide if state should change.
        """

        # If the leaf is gone, then go back to exploring
        leaf = self.ant.world.get(self.ant.leaf_id)
        if leaf is None:
            return "exploring"

        # If we are next to the leaf, pick it up and deliver it
        if self.ant.location.get_distance_to(leaf.location) < 5.0:
            self.ant.carry(leaf.image)
            self.ant.world.remove_entity(leaf)
            return "delivering"

        return None

    def entry_actions(self):
        """
       Actions executed by the ant when it enter explore state.
       """

        # Set the destination to the location of the leaf
        leaf = self.ant.world.get(self.ant.leaf_id)
        if leaf is not None:
            self.ant.destination = leaf.location
            self.ant.speed = 160. + randint(-20, 20)


class AntStateDelivering(State):
    """
    The Delivering State for Ants.
    The ant moves toward the nest with the collected object.
    """

    def __init__(self, ant):
        """
        Call the base class constructor to initialize the State.

        :param ant: ant instance that this state belongs to
        """

        State.__init__(self, "delivering")
        self.ant = ant

    def check_conditions(self):
        """
        Check conditions of the ant and environment to decide if state should change.
        """

        # If inside the nest, randomly drop the object
        if Vector2(*NEST_POSITION).get_distance_to(self.ant.location) < NEST_SIZE:
            if randint(1, 10) == 1:
                self.ant.drop(self.ant.world.background)
                return "exploring"

        return None

    def entry_actions(self):
        """
        Actions executed by the ant when it enter explore state.
        """

        # Move to a random point in the nest
        self.ant.speed = 60.
        random_offset = Vector2(randint(-20, 20), randint(-20, 20))
        self.ant.destination = Vector2(*NEST_POSITION) + random_offset


class AntStateHunting(State):
    """
    The Delivering State for Ants.
    The ant moves toward the spider with random speed.
    """

    def __init__(self, ant):
        """
        Call the base class constructor to initialize the State.

        :param ant: ant instance that this state belongs to
        """

        State.__init__(self, "hunting")
        self.ant = ant
        self.got_kill = False
        self.speed = 0

    def do_actions(self):
        """
        Check conditions of the ant and environment to decide if state should change.
        """

        spider = self.ant.world.get(self.ant.spider_id)

        if spider is None:
            return

        self.ant.destination = spider.location

        if self.ant.location.get_distance_to(spider.location) < 15.:
            # Give the spider a fighting chance
            if randint(1, 5) == 1:
                spider.bitten()
                # If the spider is dead, move it back to the nest
                if spider.health <= 0:
                    self.ant.carry(spider.image)
                    self.ant.world.remove_entity(spider)
                    self.got_kill = True

    def check_conditions(self):
        """
        Check conditions of the ant and environment to decide if state should change.
        """

        if self.got_kill:
            return "delivering"

        spider = self.ant.world.get(self.ant.spider_id)

        # If the spider has been killed then return to exploring state
        if spider is None:
            return "exploring"

        # If the spider gets far enough away, return to exploring state
        if spider.location.get_distance_to(NEST_POSITION) > NEST_SIZE * 3:
            return "exploring"

        return None

    def entry_actions(self):
        """
        Actions executed by the ant when it enter hunting state.
        """

        self.speed = 160. + randint(0, 50)

    def exit_actions(self):
        """
        Exit state action.
        """

        self.got_kill = False