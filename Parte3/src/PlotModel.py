class Plot:
    def __init__(self, data):    
        if type.lower() == "ac":
            self.freq = data[:][0]
            self.mag = data[:][1]
            self.phase = data[:][2]

