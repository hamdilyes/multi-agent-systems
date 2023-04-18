from communication.arguments.Comparison import Comparison
from communication.arguments.CoupleValue import CoupleValue


class Argument :
    """ Argument class .
    This class implements an argument used during the interaction .
    attr :
    decision :
    item :
    comparison_list :
    couple_values_list :
    """
    def __init__( self , boolean_decision , item ) :
        """ Creates a new Argument .
        """
        # To be completed
        self.decision = boolean_decision
        self.item = item
        self.comparison = None
        self.couple_values = None
    def add_premiss_comparison( self , criterion_name_1 , criterion_name_2 ) :
        """ Adds a premiss comparison in the comparison list .
        """
        self.comparison = Comparison(criterion_name_1, criterion_name_2)
        
    def add_premiss_couple_values( self , criterion_name , value ) :
        """ Add a premiss couple values in the couple values list .
        """
        self.couple_values = CoupleValue(criterion_name, value)

    def __str__(self):
        if self.decision:
            return self.item.get_name()+' <= '+ self.couple_values.__str__() + " , " + self.comparison.__str__()
        else:
            return 'not ' + self.item.get_name()+' > '+ self.couple_values.__str__() + " , " + self.comparison.__str__()