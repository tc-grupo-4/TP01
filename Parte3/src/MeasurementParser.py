import csv
import xlrd

class MeasurementParser:
	# https://pythonprogramming.net/reading-csv-files-python-3/
	def parseCSV(self, filePath):
		data = []
		with open(filePath) as csvfile:
			readcsv = csv.reader(csvfile, delimiter = ';')
			next(readcsv)
			f = []
			mag = []
			phase = []
			for row in readcsv:
				f.append(row[0])
				mag.append(row[1])
				phase.append(row[2])
		
			f = [float(i) for i in f]
			mag = [float(i) for i in mag]
			phase = [float(i) for i in phase]
			data = [f, mag, phase]

		return data

	def parseSpreadsheet(self, filePath):
		# https://www.sitepoint.com/using-python-parse-spreadsheet-data/
		workbook = xlrd.open_workbook(filePath)
		sheet = workbook.sheet_by_index(0)
		i = 0
		j = 0
		row = []
		data = []
		f = []
		mag = []
		phase = []

		for i in range (0, sheet.nrows):
			f.append(sheet.cell_value(i,0))
			mag.append(sheet.cell_value(i,1))
			phase.append(sheet.cell_value(i,2))
			pass

		#f = [float(i) for i in f]
		#mag = [float(i) for i in mag]
		#phase = [float(i) for i in phase]

		data = [f, mag, phase]
		return data
