

from execution_time import timeit


class ReagentManager():
    def __init__(self):
        self.reagents = {}
        self.tier_map = {}
        self.current_requirements = {}

    def read_input(self, input_data):
        input_data = input_data.split("\n")
        for row in input_data:
            new_reagent = Reagent(row)
            self.add_reagent(new_reagent)
        self.add_reagent(Reagent("ORE"))
    
    def add_reagent(self, reagent):
        self.reagents[reagent.name] = reagent
    
    def fetch_reagent(self, reagent_name):
        return self.reagents[reagent_name]
    
    def calculate_tiers(self, reagent_name, tier):
        # Go through each reagent, and determine it's tier
        selected = self.fetch_reagent(reagent_name)
        children = selected.get_child_ingredients(self)
        for i in children:
            if tier > i.tier:
                i.tier = tier
            self.calculate_tiers(i.name, tier+1)
    
    def print_tiers(self):
        for i in self.reagents:
            print(f"{i} - Tier {self.reagents[i].tier}")

    def calculate_tier_prerequisites(self, to_process_tier):
        self.build_tier_map()
        reagents = self.tier_map[to_process_tier]
        for reagent in reagents:
            if reagent.name not in self.current_requirements:
                raise Exception("WHOOPS")
            # Batches required
            output_units_needed = self.current_requirements[reagent.name]
            recipe_outputs = reagent.batch_volume
            if output_units_needed % recipe_outputs != 0:
                batches = int(output_units_needed / recipe_outputs)+1
            else:
                batches = int(output_units_needed / recipe_outputs)
            recipe = reagent.recipe
            for reagent_name in recipe:
                amount = recipe[reagent_name]*batches
                if reagent_name in self.current_requirements:
                    self.current_requirements[reagent_name] += amount
                else:
                    self.current_requirements[reagent_name] = amount
    
    def build_tier_map(self):
        if self.tier_map == {}: # Build map so we can call this faster
            for i in self.reagents:
                if self.reagents[i].tier not in self.tier_map:
                    self.tier_map[self.reagents[i].tier] = [self.reagents[i]]
                else:
                    self.tier_map[self.reagents[i].tier].append(self.reagents[i])


    def calculate_fuel_cost(self, fuel_units):
        self.current_requirements = {}
        fuel = self.fetch_reagent("FUEL")
        self.build_tier_map()
        for ingredient in fuel.recipe:
            self.current_requirements[ingredient] = fuel.recipe[ingredient] * fuel_units
        tiers = list(self.tier_map.keys())
        tiers.sort()
        # Skipe first tier - which is just FUEL
        for tier in tiers[1:]:
            self.calculate_tier_prerequisites(tier)
        return self.current_requirements["ORE"]



        
class Reagent():
    def __init__(self, instruction):    
        self.recipe = {}
        self.child_ingredients = []
        self.tier = -1

        if instruction == "ORE":
            self.tier = 999999
            self.name = "ORE"
            self.batch_volume = 1
            return
        
        [ingredients, outp] = instruction.split("=>")
        outp = outp.strip()
        [self.batch_volume, self.name] = outp.split(" ")
        self.batch_volume = int(self.batch_volume)
        for ingredient in ingredients.split(","):
            [vol, ingredient] = ingredient.strip().split(" ")
            self.recipe[ingredient] = int(vol)
    
    def get_child_ingredients(self, manager):
        if self.name == "ORE":
            return []
        if self.child_ingredients == []:
            for ingredient in self.recipe:
                new_reagent = manager.fetch_reagent(ingredient)
                self.child_ingredients.append(new_reagent)
        return self.child_ingredients


@timeit
def question_14():
    with open("data\\q14input.txt") as f:
        input_data = f.read()
    manager = ReagentManager()
    manager.read_input(input_data)
    manager.calculate_tiers("FUEL", 1)
    manager.print_tiers()
    print(f"Question 14a: {manager.calculate_fuel_cost(1)}")
    ORE_reserves = 1000000000000
    
    fuel_units = 1000
    current_fuel_cost = 0
    current_fuel_step = 1000
    
    while current_fuel_step > 1:
        previous_fuel_cost = current_fuel_cost
        current_fuel_cost = manager.calculate_fuel_cost(fuel_units)
        # Step Distance
        distance = (current_fuel_cost - previous_fuel_cost)/ current_fuel_step
        current_fuel_step = int((ORE_reserves - current_fuel_cost) / distance)
        fuel_units += current_fuel_step
    print(f"Question 14b: Can produce {fuel_units} costing {manager.calculate_fuel_cost(fuel_units)}")
    print(f"Question 14b: Cannot produce {fuel_units+1} costing {manager.calculate_fuel_cost(fuel_units+1)}")





if __name__ == "__main__":
    question_14()
