import numpy as np

class SpiceParser:
    def __init__(self):
        pass
    
    def parseSpiceFile(self, filePath):
        # Me pasn un archivo .txt
        # primera columna: frecuencia
        # segunda columna (magnitud,fase)
        # magnitud viene con dB y fase con º

        # abrir archivo en modo lectura
        file = open(filePath, "r")
        lines = file.readlines()
        file.close()

        # tengo todas las lineas de alchivo en lines
        
        # La primera linea me indica si es un AC analysis
        # o un transit
        # leo hasta el primer \t
        headers = lines[0].split("\t")
        [freq,mag,phase] = self.parseACFile(lines[1:])
        # devuelvo los datos:
        return [freq, mag, phase]

    def parseTransitFile(self, lines):
        pass

    def parseACFile(self, lines):
        # freq contiene la lista de frecuencias
        freq = []
        mag = []
        phase = []
        for line in lines:
            #data es un string
            # freq es una lista de strings con todas las frecuencias
            # del archivo. solo resta convertirlas a float
            freq.append(line.split("\t")[0])
            data = line.split("\t")[1]
            # tengo que parsear el data
            temp = self.parseACData(data)
            mag.append(temp[0])
            phase.append(temp[1])
        
        #convierto todos los elemntos a float
        freq = [float(i) for i in freq]
        mag = [float(i) for i in mag]
        phase = [float(i) for i in phase]

        return [freq,mag,phase]

    def parseTransferFunction(self, type, data):
        
        pass

    def parseACData(self, data):
        mag = data[data.find("(")+1:data.find("d")]
        phase = data[data.find(",")+1:data.find(")")-1]

        return [mag,phase]

        

