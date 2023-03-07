"""
Prey-Predator Model
================================
Replication of the model found in NetLogo:
    Wilensky, U. (1997). NetLogo Wolf Sheep Predation model.
    http://ccl.northwestern.edu/netlogo/models/WolfSheepPredation.
    Center for Connected Learning and Computer-Based Modeling,
    Northwestern University, Evanston, IL.
"""
from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from prey_predator.agents import Sheep, Wolf, GrassPatch
from prey_predator.schedule import RandomActivationByBreed

class WolfSheep(Model):
    """
    Wolf-Sheep Predation Model
    """
    description = (
        "A model for simulating wolf and sheep (predator-prey) ecosystem modelling."
    )

    def __init__(
        self,
        height=20,
        width=20,
        initial_sheep=100,
        initial_wolves=50,
        sheep_reproduce=0.4,
        wolf_reproduce=0.2,
        grass=False,
        grass_regrowth_time=10,
        wolf_gain_from_food=1,
        sheep_gain_from_food=1,
        #
        sheep_energy = 1,
        wolf_energy = 2,
        sheep_age = 12,
        wolf_age = 14
    ):
        """
        Create a new Wolf-Sheep model with the given parameters.

        Args:
            initial_sheep: Number of sheep to start with
            initial_wolves: Number of wolves to start with
            sheep_reproduce: Probability of each sheep reproducing each step
            wolf_reproduce: Probability of each wolf reproducing each step
            wolf_gain_from_food: Energy a wolf gains from eating a sheep
            grass: Whether to have the sheep eat grass for energy
            grass_regrowth_time: How long it takes for a grass patch to regrow
                                 once it is eaten
            sheep_gain_from_food: Energy sheep gain from grass, if enabled.
        """
        super().__init__()
        # Set parameters
        self.height = height
        self.width = width
        self.initial_sheep = initial_sheep
        self.initial_wolves = initial_wolves
        self.sheep_reproduce = sheep_reproduce
        self.wolf_reproduce = wolf_reproduce
        self.wolf_gain_from_food = wolf_gain_from_food
        self.grass = grass
        self.grass_regrowth_time = grass_regrowth_time
        self.sheep_gain_from_food = sheep_gain_from_food

        # Other parameters we chose
        self.sheep_energy = sheep_energy
        self.wolf_energy = wolf_energy
        self.sheep_age = sheep_age
        self.wolf_age = wolf_age

        # Create schedule and grid
        self.schedule = RandomActivationByBreed(self)
        self.grid = MultiGrid(self.height, self.width, torus=True)
        self.datacollector = DataCollector(
            {
                "Wolves": lambda m: m.schedule.get_breed_count(Wolf),
                "Sheep": lambda m: m.schedule.get_breed_count(Sheep),
            }
        )

        # Create sheep:
        for _ in range(self.initial_sheep):
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            sheep = Sheep(self.next_id(), (x, y), self, True, energy=self.sheep_energy, age=self.sheep_age)
            self.grid.place_agent(sheep, (x, y))
            self.schedule.add(sheep)

        # Create wolves
        for _ in range(self.initial_wolves):
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            wolf = Wolf(self.next_id(), (x, y), self, True, energy=self.wolf_energy, age=self.wolf_age)
            self.grid.place_agent(wolf, (x, y))
            self.schedule.add(wolf)

        # Create grass patches
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                patch = GrassPatch(self.next_id(), (x, y), self, fully_grown=True, countdown=self.grass_regrowth_time)
                self.grid.place_agent(patch, (x, y))
                self.schedule.add(patch)

    def step(self):
        self.schedule.step()

        # Collect data
        self.datacollector.collect(self)

        # ... to be completed

    def run_model(self, step_count=200):
        for _ in range(step_count):
            self.step()

