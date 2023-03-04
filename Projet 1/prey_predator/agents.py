from mesa import Agent
from prey_predator.random_walk import RandomWalker


class Sheep(RandomWalker):
    """
    A sheep that walks around, reproduces (asexually) and gets eaten.

    The init is the same as the RandomWalker.
    """

    def __init__(self, unique_id, pos, model, moore, energy=3,age = 10):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy
        self.age = age

    def step(self):
        """
        A model step. Move, then eat grass and reproduce.
        """
        self.age -=1
        self.random_move()
        # If grass available, eat it
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        # Type of agent in cellmates
        if len(cellmates) > 0 and any( type(mate) is GrassPatch for mate in cellmates) :
            for mate in cellmates:
                if type(mate) is GrassPatch:
                    if mate.fully_grown:
                        mate.fully_grown = False
                        self.energy += 1
        # reproduce if enough energy
        if self.energy > 4 :
            sheep = Sheep(self.model.next_id(),self.pos,self.model,True)
            self.model.schedule.add(sheep)
            self.model.grid.place_agent(sheep,self.pos)

        if self.age < 0:
            self.model.schedule.remove(self)
            self.model.grid.remove_agent(self)
            #del self
        

class Wolf(RandomWalker):
    """
    A wolf that walks around, reproduces (asexually) and eats sheep.
    """

    

    def __init__(self, unique_id, pos, model, moore, energy=3, age=10):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy
        self.age = age

    def step(self):
        self.random_move()
        # ... to be completed
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        # Type of agent in cellmates
        if len(cellmates) > 0 and any( type(mate) is Sheep for mate in cellmates) :
            for mate in cellmates:
                if type(mate) is Sheep:
                    self.model.schedule.remove(mate)
                    self.model.grid.remove_agent(mate)
                    #del mate
                    self.energy += 1
        # reproduce if enough energy
        if self.energy > 4 :
            wolf = Wolf(self.model.next_id,self.pos,self.model,True)
            self.model.schedule.add(wolf)
            self.model.grid.place_agent(wolf,self.pos)
        
        if self.age < 0:
            self.model.schedule.remove(self)
            self.model.grid.remove_agent(self)
            #del self


class GrassPatch(Agent):
    """
    A patch of grass that grows at a fixed rate and it is eaten by sheep
    """

    def __init__(self, unique_id, pos, model, fully_grown, countdown):
        """
        Creates a new patch of grass

        Args:
            grown: (boolean) Whether the patch of grass is fully grown or not
            countdown: Time for the patch of grass to be fully grown again
        """
        super().__init__(unique_id, model)
        # ... to be completed
        self.pos = pos
        self.fully_grown = fully_grown
        self.countdown = countdown

    def step(self):
        # ... to be completed
        if self.fully_grown == False and self.countdown > 0:
            self.countdown -= 1
        elif self.fully_grown == False and self.countdown == 0:
            self.fully_grown = True
            self.countdown = 10
        
