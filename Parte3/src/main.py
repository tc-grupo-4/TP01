import tkinter
from tkinter import simpledialog, messagebox, ttk
import FileParser as fp
import os.path
from matplotlib import rc


from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import numpy as np

WIDTH = 800
HEIGHT = 600

class PlotTool:
    def __init__(self, master):
        self.parser = fp.FileParser()
        self.root = master
        self.plotList = []
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
        tkinter.Label(self.controlsFrame, text="Freq Label:", bg=self.controlsFrame["bg"]).grid(row=0,padx=5)
        tkinter.Label(self.controlsFrame, text="Mag Label:",bg=self.controlsFrame["bg"]).grid(row=1,padx=5)
        tkinter.Label(self.controlsFrame, text="Phase Label:",bg=self.controlsFrame["bg"]).grid(row=2,padx=5)

        self.freqLabel = tkinter.StringVar()
        self.magLabel = tkinter.StringVar()
        self.phaseLabel = tkinter.StringVar()

        self.freqLabelEntry = tkinter.Entry(self.controlsFrame, textvariable=self.freqLabel)
        self.magLabelEntry = tkinter.Entry(self.controlsFrame, textvariable=self.magLabel)
        self.phaseLabelEntry = tkinter.Entry(self.controlsFrame, textvariable=self.phaseLabel)

        self.freqLabelEntry.grid(row=0, column=1, pady=5, padx=5, sticky="W")
        self.magLabelEntry.grid(row=1, column=1, pady=5, padx=5, sticky="W")
        self.phaseLabelEntry.grid(row=2, column=1, pady=5, padx=5, sticky="W")

        self.labelsButton = tkinter.Button(self.controlsFrame, text ="Set Labels", command=self.setLabels)
        self.labelsButton.grid(columnspan=2, sticky="WE", padx=5, pady=5)

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
        self.rb1.grid(columnspan=2, sticky="W", padx=5, pady=5)
        self.rb2 = tkinter.Radiobutton(self.controlsFrame, text=self.MODES[1], variable=self.var, value=1, command=self.selTransferMethod, bg = self.controlsFrame["bg"])
        self.rb2.grid(columnspan=2, sticky="W", padx=5, pady=5)
        # llamo a selTransferMethod para setear el string del boton segun el radiobuttton por default
        self.selTransferMethod()

        # Boton medicion
        self.measurementButton = tkinter.Button(self.controlsFrame, text="Medición")
        self.measurementButton.grid(columnspan=2, sticky="WE", padx=5, pady=5)

        # Distribucion Bode
        tkinter.Label(self.controlsFrame, text="Bode Distribution:", bg=self.controlsFrame["bg"]).grid(columnspan=2,padx=5, sticky="W")
        self.DIST = ["Condensed", "Expanded"]
        self.bodeMode = tkinter.IntVar()
        self.bodeMode.set(0)
        self.bodeModeFlag = self.bodeMode.get()
        self.rb1 = tkinter.Radiobutton(self.controlsFrame, text=self.DIST[0], variable=self.bodeMode, value=0, command=self.selBodeMode, bg = self.controlsFrame["bg"])
        self.rb1.grid(columnspan=2, sticky="W", padx=5, pady=5)
        self.rb2 = tkinter.Radiobutton(self.controlsFrame, text=self.DIST[1], variable=self.bodeMode, value=1, command=self.selBodeMode, bg = self.controlsFrame["bg"])
        self.rb2.grid(columnspan=2, sticky="W", padx=5, pady=5)

        # Boton borrar plots
        self.deleteButton = tkinter.Button(self.controlsFrame, text="Eliminar", command=self.deletePlots)
        self.deleteButton.grid(columnspan=2, sticky="WE", padx=5, pady=5)


        # TEST!!! pongo un grafico de prueba
        self.fig1 = Figure(figsize=(6,4))
        plt.rc('text', usetex=True)
        plt.rc('font', family='serif')
        self.axis1 = self.fig1.add_subplot(111)
        self.axis2 = self.axis1.twinx()
        self.figCanvas = FigureCanvasTkAgg(self.fig1, master=self.figuresFrame)
        self.figCanvas.draw()
        self.figCanvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

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
            type, data = self.parser.parseSpiceFile(filePath[0])
            # agrego a la lista de plots
            self.plotList.append(data)
            if type.lower() == "ac":
                # Agregar Plot bode
                f=data[:][0]
                mag=data[:][1]
                phase=data[:][2]
                if self.bodeModeFlag == 0: # condensado
                    # los dos en uno
                    self.drawCondensated(f, mag, phase)
                    
                elif self.bodeModeFlag == 1: # extendido
                    self.drawExpanded(f, mag, phase)

    
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

    def selBodeMode(self):
        option = self.bodeMode.get()
        if option == 0 and self.bodeModeFlag == 1:
            # condensar los bodes:
            # reacomodar la figura
            self.redrawCondensated()
        elif option == 1 and self.bodeModeFlag == 0:
            # reacomodar figura
            
            self.redrawExpanded()
            # tomar todas las mag y phase de los bodes y graficarlas todas en un solo plot

        self.bodeModeFlag = option

    def redrawCondensated(self):
        self.fig1.clf()
        self.axis1 = self.fig1.add_subplot(111)
        self.axis2 = self.axis1.twinx()
        for data in self.plotList:
            f = data[:][0]
            mag = data[:][1]
            phase = data[:][2]
            self.drawCondensated(f, mag, phase)
    
    def drawCondensated(self, f, mag, phase):
        self.axis1.semilogx(f, mag, linewidth=0.5, linestyle='-')
        self.axis1.tick_params(axis='y')
        self.axis1.grid(True, which="both", ls="-")
        self.axis1.set_xlabel(r'Frequency [Hz]')
        self.axis1.set_ylabel(r'Mag [dB]')
        self.axis2.semilogx(f, phase, linewidth=0.5, linestyle='-.')
        self.axis2.tick_params(axis='y')
        self.axis2.grid(True, which="both", ls="-")
        self.axis2.set_ylabel(r'Phase [grad]')

        self.figCanvas.draw()

    def redrawExpanded(self):
        self.fig1.clf()
        self.axis1 = self.fig1.add_subplot(211)
        self.axis2 = self.fig1.add_subplot(212)
        for data in self.plotList:
            f = data[:][0]
            mag = data[:][1]
            phase = data[:][2]
            self.drawExpanded(f, mag, phase)

    def drawExpanded(self, f, mag, phase):
        self.axis1.semilogx(f, mag, linewidth=0.5)
        self.axis1.set_xlabel(r'{}'.format(self.freqLabel.get()))
        self.axis1.set_ylabel(r'{}'.format(self.magLabel.get()))
        self.axis1.grid(True, which="both", ls="-")
        self.axis2.semilogx(f, phase, linewidth=0.5)
        self.axis2.set_xlabel(r'{}'.format(self.freqLabel.get()))
        self.axis2.set_ylabel(r'{}'.format(self.phaseLabel.get()))
        self.axis2.grid(True, which="both", ls="-")
        self.fig1.tight_layout()
        self.figCanvas.draw()

    def setLabels(self):
        if self.freqLabel.get():
            self.axis1.set_xlabel(r'{}'.format(self.freqLabel.get()))
            self.axis2.set_xlabel(r'{}'.format(self.freqLabel.get()))  
        
        if self.magLabel.get():
            self.axis1.set_ylabel(r'{}'.format(self.magLabel.get()))
        
        if self.phaseLabel.get():
            self.axis2.set_ylabel(r'{}'.format(self.phaseLabel.get()))

        self.axis1.relim()
        self.axis2.relim()
        self.figCanvas.draw()


    def deletePlots(self):
        self.axis1.cla()
        self.axis2.cla()
        self.figCanvas.draw()
        self.plotList = []

def main():
    # Root window
    root = tkinter.Tk()
    PlotTool(root)
    root.mainloop()

if __name__ == "__main__": main()
