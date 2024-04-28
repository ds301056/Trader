class Instrument:

    def __init__(self, name, ins_type, displayName, pipLocation, tradeUnitsPrecision, marginRate, displayPrecision ):
        self.name = name # Set the name attribute to the value of the name parameter
        self.ins_type = ins_type # Set the ins_type attribute to the value of the ins_type parameter
        self.displayName = displayName # Set the displayName attribute to the value of the displayName parameter
        self.pipLocation = pow(10, pipLocation) # Set the pipLocation attribute to 10 raised to the power of the pipLocation parameter
        self.tradeUnitsPrecision = tradeUnitsPrecision # Set the tradeUnitsPrecision attribute to the value of the tradeUnitsPrecision parameter
        self.marginRate = float(marginRate) # Set the marginRate attribute to the float value of the marginRate parameter
        self.displayPrecision = int(displayPrecision) # Set the displayPrecision attribute to the integer value of the displayPrecision parameter

    def __repr__(self):
        return str(vars(self))

    @classmethod
    def FromApiObject(cls, ob): # Define the FromApiObject class method with the cls and ob parameters
        return Instrument(
            ob['name'],
            ob['type'],
            ob['displayName'],
            ob['pipLocation'],
            ob['tradeUnitsPrecision'],
            ob['marginRate'],
            ob['displayPrecision']
            #ob.get('displayPrecision', 0)
        )