
class Comparison:
    """Comparison class.
This class implements a comparison object used in argument object.
attr: best_criterion_name: worst_criterion_name:
"""

    def __init__(self,best_criterion_name, worst_criterion_name) -> None:
        self.best_criterion_name = best_criterion_name
        self.worst_criterion_name = worst_criterion_name

    def __str__(self):
        return str(self.best_criterion_name) + " > " + str(self.worst_criterion_name)

    