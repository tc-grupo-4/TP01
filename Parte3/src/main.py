import tkinter
from tkinter import simpledialog, messagebox, ttk
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
        self.transferBtnText = tkinter.StringVar()
        self.transferButton = tkinter.Button(self.controlsFrame, textvariable=self.transferBtnText, command=self.onTransferFunctionButtonClicked)
        self.transferButton.grid(columnspan=2, sticky="WE", padx=5, pady=5)
        # radioButton polos/ceros/mag o num/den
        self.MODES = ["(Poles, Zeros & Gain)", "(Num & Den)"]
        self.var = tkinter.IntVar()
        self.rb1 = tkinter.Radiobutton(self.controlsFrame, text=self.MODES[0], variable=self.var, value=0, command=self.selTransferMethod, bg = self.controlsFrame["bg"])
        self.rb1.grid(columnspan=2, sticky="WE", padx=5, pady=5)
        self.rb2 = tkinter.Radiobutton(self.controlsFrame, text=self.MODES[1], variable=self.var, value=1, command=self.selTransferMethod, bg = self.controlsFrame["bg"])
        self.rb2.grid(columnspan=2, sticky="WE", padx=5, pady=5)
        # llamo a selTransferMethod para setear el string del boton segun el radiobuttton por default
        self.selTransferMethod()

        # Boton medicion
        self.measurementButton = tkinter.Button(self.controlsFrame, text="Medición")
        self.measurementButton.grid(columnspan=2, sticky="W", padx=5, pady=5)

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
        filePath = tkinter.filedialog.askopenfilenames(title="Seleccionar archivo de Spice", filetypes=(("Archivos de Texto", "*.txt"),("Todos los archivos", "*.*")))
        if not filePath:
            return
        elif filePath[0] != '':
            type, data = self.parser.parseSpiceFile(filePath)
            if type.lower() == "ac":
                pass
                # Agregar Plot bode
            elif type.lower == "transit":
                # agregar plot tiempo
                pass
    
    def onTransferFunctionButtonClicked(self):
        mode = self.var.get()
        if mode == 0: # plos, ceros y gain
            print ("polos y ceros")
            # Prompt Polos
            self.polesZerosWindow()
        elif mode == 1: # num y den
            print ("num y den")
            self.numDenWindow()

    def polesZerosWindow(self):
        t = tkinter.Toplevel(self.controlsFrame)
        t.wm_title("Poles, Zeros & Gain Configuration")
        t.resizable(False, False)
        pLabel = tkinter.Label(t, text="Funtion Poles")
        pLabel.grid(row=0,column=0, padx=5, pady=5, sticky="WE")
        pEntry = tkinter.Entry(t)
        pEntry.grid(row=0, column=1, padx=5, pady=5, columnspan=3, sticky="WE")
        
        zLabel = tkinter.Label(t, text="Function Zeros")
        zLabel.grid(row=1,column=0, padx=5, pady=5, sticky="WE")
        zEntry = tkinter.Entry(t)
        zEntry.grid(row=1, column=1, padx=5, pady=5, columnspan=3, sticky="WE")

        gLabel = tkinter.Label(t, text="Function Gain")
        gLabel.grid(row=2,column=0, padx=5, pady=5, sticky="WE")
        gEntry = tkinter.Entry(t)
        gEntry.grid(row=2, column=1, padx=5, pady=5, columnspan=3, sticky="WE")

        acceptButton = tkinter.Button(t, text="Accept")
        acceptButton.grid(row=3,column=2, padx=5, pady=5, sticky="WE")

        cancelButton = tkinter.Button(t, text="Cancel")
        cancelButton.grid(row=3,column=3, padx=5, pady=5, sticky="WE")

    def numDenWindow(self):
        t = tkinter.Toplevel(self.controlsFrame)
        t.wm_title("Numerator & Denumerator")
        t.resizable(False, False)

        nLabel = tkinter.Label(t, text="Function Numerator")
        nLabel.grid(row=1,column=0, padx=5, pady=5, sticky="WE")
        nEntry = tkinter.Entry(t)
        nEntry.grid(row=1, column=1, padx=5, pady=5, columnspan=3, sticky="WE")

        dLabel = tkinter.Label(t, text="Function Denominator")
        dLabel.grid(row=2,column=0, padx=5, pady=5, sticky="WE")
        dEntry = tkinter.Entry(t)
        dEntry.grid(row=2, column=1, padx=5, pady=5, columnspan=3, sticky="WE")

        acceptButton = tkinter.Button(t, text="Accept")
        acceptButton.grid(row=3,column=2, padx=5, pady=5, sticky="WE")

        cancelButton = tkinter.Button(t, text="Cancel")
        cancelButton.grid(row=3,column=3, padx=5, pady=5, sticky="WE")

    def selTransferMethod(self):
        selection = str(self.MODES[self.var.get()])
        temp = "H(s)\n" + selection
        self.transferBtnText.set(temp)

    
def main():
    # Root window
    root = tkinter.Tk()
    PlotTool(root)
    root.mainloop()

if __name__ == "__main__": main()
