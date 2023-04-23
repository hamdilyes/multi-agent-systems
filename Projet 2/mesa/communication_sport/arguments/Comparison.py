
class Comparison:
    """Comparison class.
    This class implements a comparison object used in argument object.
    attr: best_criterion_name: worst_criterion_name:
    """

    def __init__(self,best_criterion_name, worst_criterion_name):
        self.best_criterion_name = best_criterion_name
        self.worst_criterion_name = worst_criterion_name

    def __str__(self):
        if self.best_criterion_name is not None and self.worst_criterion_name is not None:
            return ", " + str(self.best_criterion_name.name) + " > " + str(self.worst_criterion_name.name)
        else:
            return ""

    