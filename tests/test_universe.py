from unittest import TestCase

from idleiss.universe import UniverseManager
from idleiss.universe import SolarSystem

class UniverseTestCase(TestCase):

    def setUp(self):
        pass

    def test_can_generate_universe(self):
        uni = UniverseManager()

        the_list = [ # galaxy
            [#arm
                SolarSystem(1,1,1,0,0,0,0), SolarSystem(1,1,2,0,0,0,0)
            ],
            [#arm2
                 SolarSystem(1,2,1,0,0,0,0), SolarSystem(1,2,2,0,0,0,0)
            ],
            [#arm3
                SolarSystem(1,3,1,0,0,0,0), SolarSystem(1,3,2,0,0,0,0)
            ]
        ],
        self.assertEqual(len(the_list), 1)
