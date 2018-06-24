from os.path import join, dirname
from unittest import TestCase

from idleiss import core

path_to_file = lambda fn: join(dirname(__file__), 'data', fn)


class CoreTestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_base_game(self):
        engine = core.GameEngine(path_to_file('Small_Universe_Config.json'), path_to_file('validload.json'))
        self.assertTrue(engine)

    def test_update_world_basic(self):
        engine = core.GameEngine(path_to_file('Small_Universe_Config.json'), path_to_file('validload.json'))
        user_list = set(['an_user'])
        engine.update_world(active_list=user_list, timestamp=1000)
        # manually set one of the income rates
        engine.users['an_user'].resources.basic_materials_income = 1
        engine.users['an_user'].resources.advanced_materials_income = 1
        engine.users['an_user'].resources.money_income = 1

        # check that income is paid properly
        engine.update_world(active_list=user_list, timestamp=1007)
        self.assertEqual(engine.users['an_user'].resources.basic_materials, 7)
        self.assertEqual(engine.users['an_user'].resources.advanced_materials, 7)
        self.assertEqual(engine.users['an_user'].resources.money, 7)

        # can't trigger the same events again I guess?
        engine.update_world(active_list=user_list, timestamp=1007)
        self.assertEqual(engine.users['an_user'].resources.basic_materials, 7)
        self.assertEqual(engine.users['an_user'].resources.advanced_materials, 7)
        self.assertEqual(engine.users['an_user'].resources.money, 7)

        engine.update_world(active_list=user_list, timestamp=1008)
        self.assertEqual(engine.users['an_user'].resources.basic_materials, 8)
        self.assertEqual(engine.users['an_user'].resources.advanced_materials, 8)
        self.assertEqual(engine.users['an_user'].resources.money, 8)

    def test_offline_users_do_not_earn_resources(self):
        engine = core.GameEngine(path_to_file('Small_Universe_Config.json'), path_to_file('validload.json'))
        user_list = set(['user1', 'user2'])
        engine.update_world(active_list=user_list, timestamp=1000)
        engine.users['user1'].resources.basic_materials_income = 1
        engine.users['user2'].resources.basic_materials_income = 1
        user_list = set(['user1'])
        engine.update_world(active_list=user_list, timestamp=1001)

        # now user1 and user2 should both have 1 basic_material
        self.assertEqual(engine.users['user1'].resources.basic_materials, 1)
        self.assertEqual(engine.users['user2'].resources.basic_materials, 1)

        engine.update_world(active_list=user_list, timestamp=1002)
        # now user1 should have 2, while user2 still has only 1
        self.assertEqual(engine.users['user1'].resources.basic_materials, 2)
        self.assertEqual(engine.users['user2'].resources.basic_materials, 1)

    def test_events_skip_time(self):
        engine = core.GameEngine(path_to_file('Small_Universe_Config.json'), path_to_file('validload.json'))
        user_list = set(['an_user'])
        engine.update_world(active_list=user_list, timestamp=1000)
        # manually set one of the income rates
        engine.users['an_user'].resources.basic_materials_income = 1
        engine.users['an_user'].resources.advanced_materials_income = 1
        engine.users['an_user'].resources.money_income = 1
        engine.update_world(active_list=user_list, timestamp=2100)

        # check that income was paid properly
        self.assertEqual(engine.users['an_user'].resources.basic_materials, 1100)
        self.assertEqual(engine.users['an_user'].resources.advanced_materials, 1100)
        self.assertEqual(engine.users['an_user'].resources.money, 1100)

    def test_backwards_in_time_failure(self):
        engine = core.GameEngine(path_to_file('Small_Universe_Config.json'), path_to_file('validload.json'))
        user_list = set(['an_user'])
        engine.update_world(active_list=user_list, timestamp=1000)
        with self.assertRaises(core.TimeOutofBounds) as context:
            engine.update_world(active_list=user_list, timestamp=999)
        self.assertEqual(str(context.exception), "'already processed this timestamp'")

    def test_event_engine_add(self):
        def some_event(name='foo'):
            return name

        engine = core.GameEngine(path_to_file('Small_Universe_Config.json'), path_to_file('validload.json'))
        engine.add_event(some_event, name='foo')
        self.assertEqual(engine._engine_events[0].func, some_event)
        self.assertEqual(engine._engine_events[0].kw, {'name': 'foo'})

    def test_event_engine_backwards_in_time(self):
        def time_dependent_event(timestamp):
            return timestamp

        engine = core.GameEngine(path_to_file('Small_Universe_Config.json'), path_to_file('validload.json'))
        engine.update_world(active_list=set(), timestamp=100)
        engine.add_event(time_dependent_event, timestamp=50)
        # timestamp argument magically forced to be the last time the
        # world was updated.

        self.assertEqual(engine._engine_events[0].kw['timestamp'], 100)

        # note that the order of events that got added to the engine do
        # matter very much.  i.e. if login and logout happened at about
        # the same time but the order they were added in were reversed,
        # bad things probably will happen.  Problem belongs to the user
        # of the engine, i.e. the chatroom interface.

