from idleiss.fleet import FleetManager

class Location_Already_Exists(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Location_Does_Not_Exist(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class ResourceManager(object):
    def __init__(self):
        self.basic_materials = 0
        self.advanced_materials = 0
        self.money = 0
        #income is per second
        self.basic_materials_income = 0
        self.advanced_materials_income = 0
        self.money_income = 0
        self.income_sources = {}
        self.owned_systems = []
        self.owned_system_count = 0
        #income sources are a nested dict of
        # {starsystem:{
        #       location:
        #           [type (moon, station, belt, or other),
        #           basic_income,
        #           adv_income,
        #           money income
        #       ]
        #   }
        #}
        #example:
        #{"START SYSTEM": {
        #   "ISS": ["station", 2, 1, 1]
        #   }
        #}

    def pay_resources(self, seconds):
        self.basic_materials += self.basic_materials_income*seconds
        self.advanced_materials += self.advanced_materials_income*seconds
        self.money += self.money_income*seconds

    def add_income_source(self, system, location, source_type, basic_income,
                          adv_income, money_income):
        if basic_income < 0 or adv_income < 0 or money_income < 0:
            raise ValueError("Income for an income source cannot be negative")

        self.basic_materials_income += basic_income
        self.advanced_materials_income += adv_income
        self.money_income += money_income
        if system in self.income_sources:
            if location in self.income_sources[system]:
                raise Location_Already_Exists(str(location) + "@" + str(system) + " already exists.")
            else:
                self.income_sources[system].update({location: [source_type, basic_income, adv_income, money_income]})
        else:
            self.income_sources.update({system: {location: [source_type, basic_income, adv_income, money_income]}})

    def remove_income_source(self, system, location):
        if system in self.income_sources:
            if location in self.income_sources[system]:
                type, b_i, a_i, m_i = self.income_sources[system][location]
                self.basic_materials_income -= b_i
                self.advanced_materials_income -= a_i
                self.money_income -= m_i
                if self.basic_materials_income < 0 or self.advanced_materials_income < 0 or self.money_income < 0:
                    raise ValueError("Income is negative after removing income source "+str(location)+"@"+str(system)+": " + str(self.basic_materials_income) + " " + str(self.advanced_materials_income) + " " + str(self.money_income))
                self.income_sources[system].pop(location)
                if len(self.income_sources[system]) == 0:
                    self.income_sources.pop(system)
            else:
                raise Location_Does_Not_Exist(str(location)+"@"+str(system)+" does not exist.")
        else:
            raise Location_Does_Not_Exist(str(location)+"@"+str(system)+" does not exist.")

    def update_income_source(self, system, location, basic_income, adv_income, money_income):
        if basic_income < 0 or adv_income < 0 or money_income < 0:
            raise ValueError("Income for an income source cannot be negative")

        if system in self.income_sources:
            if location in self.income_sources[system]:
                type, b_i, a_i, m_i = self.income_sources[system][location]
                self.basic_materials_income += basic_income - b_i
                self.advanced_materials_income += adv_income - a_i
                self.money_income += money_income - m_i
            else:
                raise Location_Does_Not_Exist(str(location)+"@"+str(system)+" does not exist.")
        else:
            raise Location_Does_Not_Exist(str(location)+"@"+str(system)+" does not exist.")

    def conquer_new_system_check(self, system):
        """
        Using a Large Structure Gantry a TCU can be onlined in an unclaimed system
        Need:
            Large Structure Gantry
            Resources to upgrade Gantry
            Unclaimed system
        """
        if not system.fleets[self.player_name].contains_ship("Large Structure Gantry"):
            return False
        if system.owner is not None:
            return False
        if self.calculate_TCU_cost() > self.money:
            return False
        if self.calculate_TCU_minerals() > self.basic_materials:
            return False
        return True

    def init_conquer_new_system(self, system):
        """
        Using a Large Structure Gantry a TCU can be onlined in an unclaimed system
        """
        if conquer_new_system_check():
            if not system.fleets[self.player_name].remove_ship("Large Structure Gantry", 1):
                return False
            self.owned_system_count += 1
            system.owner = self.player_name
            self.owned_systems.append(system)

    def construct_citadel(self, system):
        """
        Citadels will function as money generators (mission hubs), consumes Small Structure Gantry
        """
        pass

    def construct_drilling_platform(self, system):
        """
        Drilling Platforms will function as basic material generators, consumes Small Structure Gantry
        """
        pass

    def construct_industrial_array(self, system):
        """
        Industrial Arrays will produce ships and structures, consumes Small Structure Gantry
        """
        pass
