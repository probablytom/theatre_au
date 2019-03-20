import unittest
import theatre_au
import functools


class DummyActor(object):
    '''
    An actor class that fulfils the most simple requirement of what our clock expects.
    '''

    def __init__(self, dummy_action=lambda: None):
        self.dummy_state = {}
        self.dummy_action = dummy_action

    def perform(self):
        while True:
            yield self.dummy_action()

    def yield_tasks(self):
        while True:
            yield self.dummy_action


class BasicTests(unittest.TestCase):
    def setUp(self):
        self.clock = theatre_au.Clock(max_ticks=5)

    def test_ticking_to_completion(self):
        # The clock will let anything listen that can `perform`.
        actor = DummyActor()
        self.clock.add_listener(actor)
        self.clock.tick()
        self.assertEquals(self.clock.ticks_passed, self.clock.max_ticks)

    def test_actors_can_do_things(self):

        def action(actor):
            actor.dummy_state["invocations"] += 1

        actor = DummyActor()
        action = functools.partial(action, actor)
        action = theatre_au.task(1)(action)
        actor.dummy_action = action
        actor.dummy_state['invocations'] = 0

        self.clock.add_listener(actor)
        self.clock.tick()

        self.assertEquals(self.clock.max_ticks, actor.dummy_state['invocations'])


    def test_actors_can_tick_slowly(self):

        def action(actor):
            actor.dummy_state["invocations"] += 1

        actor = DummyActor()
        action = functools.partial(action, actor)
        action = theatre_au.task(4)(action)
        actor.dummy_action = action
        actor.dummy_state['invocations'] = 0

        self.clock.add_listener(actor)
        self.clock.tick(5)

        self.assertEqual(actor.dummy_state['invocations'], 1)


    def test_actors_can_tick_quickly(self):

        def action(actor):
            actor.dummy_state["invocations"] += 1

        actor = DummyActor()
        action = functools.partial(action, actor)
        action = theatre_au.task(0.4)(action)
        actor.dummy_action = action
        actor.dummy_state['invocations'] = 0

        self.clock.add_listener(actor)
        self.clock.tick(5)

        self.assertGreater(actor.dummy_state['invocations'], 5)

if __name__ == '__main__':
    unittest.main()
