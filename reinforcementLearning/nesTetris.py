from nes_py import NESEnv


class FooGame(NESEnv):
    """An OpenAI Gym interface to the NES game Tetris"""

    def __init__(self):
        """Initialize a new Tetris environment."""
        super(FooGame, self).__init__("roms/Tetris.nes")
        # setup any variables to use in the below callbacks here

    def _will_reset(self):
        """Handle any RAM hacking after a reset occurs."""
        # use this method to perform setup before and episode resets.
        # the method returns None
        pass

    def _did_reset(self):
        """Handle any RAM hacking after a reset occurs."""
        # use this method to access the RAM of the emulator 
        # and perform setup for each episode. 
        # the method returns None
        pass

    def _did_step(self, done):
        """
        Handle any RAM hacking after a step occurs.

        Args:
            done: whether the done flag is set to true

        Returns:
            None

        """
        pass

    def _get_reward(self):
        """Return the reward after a step occurs."""
        return 0

    def _get_done(self):
        """Return True if the episode is over, False otherwise."""
        return False

    def _get_info(self):
        """Return the info after a step occurs."""
        return {}


# explicitly define the outward facing API for the module
__all__ = [FooGame.__name__]