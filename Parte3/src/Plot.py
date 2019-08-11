class Plot:
    def __init__(self, type, data):
        
        if type.lower() == "ac":
            self.freq = data[:,0]
            self.mag = data[:,1]
            self.phase = data[:,2]
        elif type.lower() == "transit":
            self.t = data[:,0]
            self.var = data[:,1]