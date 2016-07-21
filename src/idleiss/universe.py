class SolarSystem(object):
    def __init__(self, galaxy_id, arm_id, sol_id, owner, cit_lvl, drill_lvl, indy_lvl):
        self.galaxy_id = galaxy_id
        self.arm_id = arm_id
        self.sol_id = sol_id
        self.owner = owner
        self.citadel_level = cit_lvl
        self.drilling_level = drill_lvl
        self.industry_level = indy_lvl

    def address_string(self):
        return str(self.galaxy_id)+':'+str(self.arm_id)+':'+str(self.sol_id)

    def address_array(self):
        return [self.galaxy_id, self.arm_id, self.sol_id]

class UniverseManager(object):
    def __init__(self, saved_universe=None, galaxies=1, galactic_arms=4, systems_per_arm=100):
        #for now the universe will be composed of:
        #   1 galaxy
        #   4 arms
        #   100 star systems per arm where the first star system is closest to the core and 100 is furthest
        #In this way we can say [1:(1-4):(1-100)]
        #movement along an arm is the fastest with star 1 being the furthest from star 100 and there is no "wrapping"
        #movement from one arm to another always takes the same length of time
        if saved_universe is None:
            self.system_list = self.generate_empty_universe(galaxies, galactic_arms, systems_per_arm)
        else:
            self.system_list = saved_universe

    def generate_empty_universe(self, galaxies, galactic_arms, systems_per_arm):
        #list[x] -> galaxy x
        #list[x][y] -> galaxy x's arm y
        #list[x][y][z] -> galaxy x's arm y's system z
        return [[[SolarSystem(z,y,x,0,0,0,0) for x in xrange(systems_per_arm)] \
            for y in xrange(galactic_arms)] \
            for z in xrange(galaxies)]
