class Instrument:
    # Constructor method to initialize an instance of the Instrument class
    def __init__(self, name, ins_type, displayName, pipLocation, tradeUnitsPrecision, marginRate):
        self.name = name  # The unique identifier for the instrument
        self.ins_type = ins_type  # Instrument type, using ins_type to avoid conflict with the keyword 'type'
        self.displayName = displayName  # Human-readable name of the instrument
        self.pipLocation = pow(10, pipLocation)  # The pip location, calculated as 10 to the power of pipLocation
        self.tradeUnitsPrecision = tradeUnitsPrecision  # Precision of trade units, dictates how the instrument is traded
        self.marginRate = float(marginRate)  # The margin rate, converted to float for calculations

    # Representation method to provide a string representation of the instrument object
    def __repr__(self):
        return str(vars(self))  # Returns a string representation of the instance variables

    # Class method to create an instance of the Instrument class from an API response object
    @classmethod
    def FromApiObject(cls, ob):
        # Calls the constructor of the Instrument class with parameters extracted from the API response object
        return cls(
            ob['name'],
            ob['type'],
            ob['displayName'],
            ob['pipLocation'],
            ob['tradeUnitsPrecision'],
            ob['marginRate']
        )
