class CoupleValue:
    """CoupleValue class.
    This class implements a couple value used in argument object.
    attr: criterion_name:
    value:
    """

    def __init__(self, criterion_name, value): 
        self.criterion_name = criterion_name
        self.value = value

    def __str__(self):
        if self.criterion_name is not None and self.value is not None:
            return str(self.criterion_name.name) + " = " + str(self.value.name)
        else:
            return ""