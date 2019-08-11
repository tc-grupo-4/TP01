import numpy as np

class PlotManager:
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
        if headers[0] == "time":
            self.parseTransitFile(lines[1,:])
        elif headers[0] == "Freq.":
            self.parseACFlie(lines)

        def parseTransitFile(self, lines):
            pass

        def parseACFlie(self, lines):
            # freq contiene la lista de frecuencias
            freq = []
            # data contiene (magdB,phaseº)
            data = []
            for line in lines:
                freq.append(line.split("\t")[0])
                data.append(line.split("\t")[1])

            print(freq)
            print(data)
                

        

