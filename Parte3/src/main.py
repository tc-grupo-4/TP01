import tkinter
from tkinter import simpledialog, messagebox, ttk
from tkinter.filedialog import asksaveasfile
import SpiceParser as sp
import TransferParser as tp
import MeasurementParser as mp
import os.path
from matplotlib import rc


from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import numpy as np

class PlotTool:
    def __init__(self, master):
        self.spiceParser = sp.SpiceParser()
        self.transferParser = tp.TransferParser()
        self.measurementParser = mp.MeasurementParser()
        self.root = master
        self.legends = []
        self.markers = []
        self.root.geometry("1000x600")
        self.root.title("Plot Tool")
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
        self.freqLabel.set("Frequency [Hz]")
        self.magLabel.set("Mag [dB]")
        self.phaseLabel.set("Phase [grad]")

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
        self.measurementButton = tkinter.Button(self.controlsFrame, text="Measurement", command=self.onMeasurementButton)
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

        # Boton exportar como pdf
        self.pdfExportButton = tkinter.Button(self.controlsFrame, text="Export as PDF", command=self.pdfExport)
        self.pdfExportButton.grid(columnspan=2, sticky="WE", padx=5, pady=5)

        # Boton exportar como PNG
        self.pngExport = tkinter.Button(self.controlsFrame, text="Export as PNG", command=self.pngExport)
        self.pngExport.grid(columnspan=2, sticky="WE", padx=5, pady=5)

        # Seteo canvas de graficos
        self.fig1 = Figure(figsize=(6,4))
        plt.rc('text', usetex=True)
        plt.rc('font', family='serif')
        self.axis1 = self.fig1.add_subplot(111)
        self.axis2 = self.axis1.twinx()
        self.figCanvas = FigureCanvasTkAgg(self.fig1, master=self.figuresFrame)
        self.figCanvas.draw()
        self.figCanvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH)

    def onSelect(self):
        selection = self.plotListBox.curselection()
        if len(selection) > 0:
            self.deleteButton.config(state=tkinter.NORMAL)
        else:
            self.deleteButton.config(state=tkinter.DISABLED)

    def onSpiceBtnClicked(self):
        self.markers.append('')
        filePath = tkinter.filedialog.askopenfilenames(title="Seleccionar archivo de Spice", filetypes=(("Archivos de Texto", "*.txt"),("Todos los archivos", "*.*")))
        if not filePath:
            return
        elif filePath[0] != '':
            data = self.spiceParser.parseSpiceFile(filePath[0])
            # agrego a la lista de plots
            self.plotList.append(data)
            self.legend = simpledialog.askstring("Input", "Plot Legend", parent=self.root)
            self.legends.append(self.legend)
            f=data[:][0]
            mag=data[:][1]
            phase=data[:][2]
            self.updatePlots()

    def onTransferFunctionButtonClicked(self):
        self.markers.append('')
        mode = self.var.get()
        if mode == 0: # plos, ceros y gain
            print ("polos y ceros")
            # Prompt Polos
            self.polesZerosWindow()
        elif mode == 1: # num y den
            print ("num y den")
            self.numDenWindow()
        

    def polesZerosWindow(self):
        self.transferType = 'poles'
        self.poles = tkinter.StringVar()
        self.zeros = tkinter.StringVar()
        self.gain = tkinter.StringVar()

        self.poles.set('')
        self.zeros.set('')
        self.gain.set('')

        self.prompt = tkinter.Toplevel(self.controlsFrame)
        self.prompt.wm_title("Poles, Zeros & Gain Configuration")
        self.prompt.resizable(False, False)

        self.pLabel = tkinter.Label(self.prompt, text="Funtion Poles")
        self.pLabel.grid(row=0,column=0, padx=5, pady=5, sticky="WE")
        self.pEntry = tkinter.Entry(self.prompt, textvariable=self.poles)
        self.pEntry.grid(row=0, column=1, padx=5, pady=5, columnspan=3, sticky="WE")
        
        self.zLabel = tkinter.Label(self.prompt, text="Function Zeros")
        self.zLabel.grid(row=1,column=0, padx=5, pady=5, sticky="WE")
        self.zEntry = tkinter.Entry(self.prompt, textvariable=self.zeros)
        self.zEntry.grid(row=1, column=1, padx=5, pady=5, columnspan=3, sticky="WE")

        self.gLabel = tkinter.Label(self.prompt, text="Function Gain")
        self.gLabel.grid(row=2,column=0, padx=5, pady=5, sticky="WE")
        self.gEntry = tkinter.Entry(self.prompt, textvariable=self.gain)
        self.gEntry.grid(row=2, column=1, padx=5, pady=5, columnspan=3, sticky="WE")

        acceptButton = tkinter.Button(self.prompt, text="Accept", command=self.submitTransferData)
        acceptButton.grid(row=3,column=2, padx=5, pady=5, sticky="WE")

        cancelButton = tkinter.Button(self.prompt, text="Cancel", command=self.closePrompt)
        cancelButton.grid(row=3,column=3, padx=5, pady=5, sticky="WE")

    def submitTransferData(self):
        self.legend = simpledialog.askstring("Input", "Plot Legend", parent=self.root)
        self.legends.append(self.legend)
        if self.transferType == 'poles':
            # parseo la data:
            valid, data = self.transferParser.parsePZG([self.poles.get(), self.zeros.get(), self.gain.get()])
        elif self.transferType == 'numden':
            valid, data = self.transferParser.parseNumDen([self.num.get(), self.den.get()])
        if valid:
            # agregar a lista de plots y actualizar
            self.closePrompt()
            self.plotList.append(data)
            self.updatePlots()

    def closePrompt(self):
        self.prompt.destroy()

    def numDenWindow(self):
        self.transferType='numden'
        self.prompt = tkinter.Toplevel(self.controlsFrame)
        self.prompt.wm_title("Numerator & Denumerator")
        self.prompt.resizable(False, False)

        self.num = tkinter.StringVar()
        self.den = tkinter.StringVar()

        self.nLabel = tkinter.Label(self.prompt, text="Function Numerator")
        self.nLabel.grid(row=1,column=0, padx=5, pady=5, sticky="WE")
        self.nEntry = tkinter.Entry(self.prompt, textvariable=self.num)
        self.nEntry.grid(row=1, column=1, padx=5, pady=5, columnspan=3, sticky="WE")

        self.dLabel = tkinter.Label(self.prompt, text="Function Denominator")
        self.dLabel.grid(row=2,column=0, padx=5, pady=5, sticky="WE")
        self.dEntry = tkinter.Entry(self.prompt, textvariable=self.den)
        self.dEntry.grid(row=2, column=1, padx=5, pady=5, columnspan=3, sticky="WE")

        acceptButton = tkinter.Button(self.prompt, text="Accept", command=self.submitTransferData)
        acceptButton.grid(row=3,column=2, padx=5, pady=5, sticky="WE")

        cancelButton = tkinter.Button(self.prompt, text="Cancel", command=self.closePrompt)
        cancelButton.grid(row=3,column=3, padx=5, pady=5, sticky="WE")

    def selTransferMethod(self):
        selection = str(self.MODES[self.var.get()])
        temp = "H(s)\n" + selection
        self.transferBtnText.set(temp)

    def onMeasurementButton(self):
        self.markers.append('.')
        filePath = tkinter.filedialog.askopenfilenames(title="Seleccionar archivo de Spice", filetypes=(("Coma Separated Values", "*.csv"),("Excel Spreadsheet", "*.xlsx"),("Todos los archivos", "*.*")))
        if not filePath:
            return
        elif filePath[0] != '':
            data = []
            fn, ext = os.path.splitext(filePath[0])
            if ext == '.csv':
                data = self.measurementParser.parseCSV(filePath[0])
            elif ext == '.xls' or ext == '.xlsx':
                data = self.measurementParser.parseSpreadsheet(filePath[0]) 
            
            # agrego a la lista de plots
            self.legend = simpledialog.askstring("Input", "Plot Legend", parent=self.root)
            self.legends.append(self.legend)
            self.plotList.append(data)
            f=data[:][0]
            mag=data[:][1]
            phase=data[:][2]
            self.updatePlots()

    def updatePlots(self):
        self.index = 0
        if self.bodeModeFlag == 0:
            self.redrawCondensated()
        elif self.bodeModeFlag == 1:
            self.redrawExpanded()

    def selBodeMode(self):
        option = self.bodeMode.get()
        if option == 0 and self.bodeModeFlag == 1:
            self.index = 0
            # condensar los bodes:
            # reacomodar la figura
            self.redrawCondensated()
        elif option == 1 and self.bodeModeFlag == 0:
            self.index = 0
            # reacomodar figura
            
            self.redrawExpanded()
            # tomar todas las mag y phase de los bodes y graficarlas todas en un solo plot

        self.bodeModeFlag = option

    def redrawCondensated(self):

        self.figCanvas._tkcanvas.destroy()
        self.fig1 = Figure(figsize=(6,4))
        self.axis1 = self.fig1.add_subplot(111)
        self.axis2 = self.axis1.twinx()
        self.figCanvas = FigureCanvasTkAgg(self.fig1, master=self.figuresFrame)
        self.figCanvas.draw()
        self.figCanvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH)

        for data in self.plotList:
            f = data[:][0]
            mag = data[:][1]
            phase = data[:][2]
            self.drawCondensated(f, mag, phase)
            self.index = self.index + 1

    def drawCondensated(self, f, mag, phase):
        self.axis1.semilogx(f, mag, linewidth=1, linestyle='-', marker=self.markers[self.index])
        self.axis1.tick_params(axis='y')
        self.axis1.grid(True, which="major", ls='-')
        self.axis1.set_xlabel(r'{}'.format(self.freqLabel.get()))
        self.axis1.set_ylabel(r'{}'.format(self.magLabel.get()))
        self.axis1.legend(self.legends)
        self.axis2.semilogx(f, phase, linewidth=1, linestyle='-.', marker=self.markers[self.index])
        self.axis2.tick_params(axis='y')
        self.axis2.grid(True, which="major", ls="-")
        self.axis2.set_ylabel(r'{}'.format(self.phaseLabel.get()))
        self.figCanvas.draw()

    def redrawExpanded(self):

        self.figCanvas._tkcanvas.destroy()
        self.fig1 = Figure(figsize=(6,4))
        self.figCanvas = FigureCanvasTkAgg(self.fig1, master=self.figuresFrame)
        self.figCanvas.draw()
        self.figCanvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH,expand=1)
        self.axis1 = self.fig1.add_subplot(211)
        self.axis2 = self.fig1.add_subplot(212)
        for data in self.plotList:
            f = data[:][0]
            mag = data[:][1]
            phase = data[:][2]
            self.drawExpanded(f, mag, phase)
            self.index = self.index+1

    def drawExpanded(self, f, mag, phase):
        self.axis1.semilogx(f, mag, linewidth=1, marker=self.markers[self.index])
        self.axis1.set_xlabel(r'{}'.format(self.freqLabel.get()))
        self.axis1.set_ylabel(r'{}'.format(self.magLabel.get()))
        self.axis1.grid(True, which="major", ls='-')
        self.axis1.legend(self.legends)
        self.axis2.semilogx(f, phase, linewidth=1, marker=self.markers[self.index])
        self.axis2.set_xlabel(r'{}'.format(self.freqLabel.get()))
        self.axis2.set_ylabel(r'{}'.format(self.phaseLabel.get()))
        self.axis2.grid(True, which="major", ls='-')
        self.axis2.legend(self.legends)
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
        self.legends = []

    def pdfExport(self):
        file = asksaveasfile(filetypes=[('PDF Files', '*.pdf')], defaultextension=[('PDF Files', '*.pdf')])
        if not file:
            return
        elif file.name != '':
            self.fig1.savefig(file.name, bbox_inches='tight')
        pass

    def pngExport(self):
        file = asksaveasfile(filetypes=[('PNG Files', '*.png')], defaultextension=[('PNG Files', '*.png')])
        if not file:
            return
        elif file.name != '':
            self.fig1.savefig(file.name, bbox_inches='tight')
        pass
        pass

def main():
    # Root window
    root = tkinter.Tk()
    PlotTool(root)
    root.mainloop()

if __name__ == "__main__": main()
