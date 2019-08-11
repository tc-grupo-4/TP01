import tkinter
import FileParser as fp
import os.path

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

import numpy as np

WIDTH = 800
HEIGHT = 600

class PlotTool:
    def __init__(self, master):
        self.parser = fp.FileParser()
        self.root = master
        # Frames
        # Creo dos frames que de distribuyen la ventana en un grid de 2 col y una fila
        # En controlsFrame van los controles del programa (a la izquierda)
        # En figuresFrame van las figuras de los graficos
        self.controlsFrame = tkinter.Frame(self.root, bg = 'lightblue')
        self.figuresFrame = tkinter.Frame(self.root, bg = 'lightgrey')

        self.controlsFrame.grid(row=0, column=0, sticky= "nsew")
        self.figuresFrame.grid(row=0, column=1, sticky= "nsew")

        self.root.grid_columnconfigure(0)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # Controles para etiquetas de ejes.
        tkinter.Label(self.controlsFrame, text="x label:", bg=self.controlsFrame["bg"]).grid(row=0,padx=5)
        tkinter.Label(self.controlsFrame, text="y label:",bg=self.controlsFrame["bg"]).grid(row=1,padx=5)

        self.xLabelEntry = tkinter.Entry(self.controlsFrame)
        self.yLabelEntry = tkinter.Entry(self.controlsFrame)

        self.xLabelEntry.grid(row=0, column=1, pady=5, padx=5)
        self.yLabelEntry.grid(row=1, column=1, pady=5, padx=5)

        # Controles para cargar archivos
        # Boton Spice
        self.spiceButton = tkinter.Button(self.controlsFrame, text= "Spice", command=self.onSpiceBtnClicked)
        self.spiceButton.grid(columnspan=2, sticky="WE", padx=5, pady=5)

        # Boton transferencia
        self.transferButton = tkinter.Button(self.controlsFrame, text="H(s)")
        self.transferButton.grid(columnspan=2, sticky="WE", padx=5, pady=5)


        # Boton medicion
        self.measurementButton = tkinter.Button(self.controlsFrame, text="Medición")
        self.measurementButton.grid(columnspan=2, sticky="WE", padx=5, pady=5)

        # Boton borrar plots
        # lista de prueba:
        self.testList = ["plot 1", "plot 2", "plot 3"]
        self.plotListBox = tkinter.Listbox(self.controlsFrame, exportselection=0, selectmode=tkinter.MULTIPLE)
        for entry in self.testList:
            self.plotListBox.insert(tkinter.END, entry)
        self.plotListBox.grid(columnspan=2, sticky="WE", padx=5, pady=5)
        self.deleteButton = tkinter.Button(self.controlsFrame, text="Eliminar", state=tkinter.DISABLED)
        self.deleteButton.grid(columnspan=2, sticky="WE", padx=5, pady=5)
        self.plotListBox.bind('<<ListboxSelect>>', lambda event: self.onSelect())


    def onSelect(self):
        selection = self.plotListBox.curselection()
        if len(selection) > 0:
            self.deleteButton.config(state=tkinter.NORMAL)
        else:
            self.deleteButton.config(state=tkinter.DISABLED)

    def onSpiceBtnClicked(self):
        #type, data = self.parser.parseSpiceFile("resources/ac.txt")
        #print(type)
        #print(len(data[0]))
        # Abrir selector de archivos
        filePath = tkinter.filedialog.askopenfilenames(title="Seleccionar archivo de Spice", filetypes=(("Archivos de Texto", "*.txt"),("Todos los archivos", "*.*")))[0]
        if filePath != '':
            type, data = self.parser.parseSpiceFile(filePath)
            if type.lower() == "ac":
                pass
                # Agregar Plot bode
            elif type.lower == "transit":
                # agregar plot tiempo
                pass

def main():
    # Root window
    root = tkinter.Tk()
    PlotTool(root)
    root.mainloop()

if __name__ == "__main__": main()
