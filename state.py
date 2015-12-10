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

        self.states = {}
        self.active_state = None

    def add_state(self, state):
        """
        Add a instance to the internal dictionary.
        :param state: the name of the state
        :return:
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
        Change states and perform any exit / entry actions
        :param new_state_name: name of the state to be set
        :return:
        """

        if self.active_state is not None:
            self.active_state.exit_actions()

        self.active_state = self.states[new_state_name]
        self.active_state.entry_actions()