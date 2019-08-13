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
		while sheet.cell(i,j).value is not xlrd.empty_cell.value:
			row = []
			while sheet.cell(i,j).value is not xlrd.empty_cell.value:
				row.append(sheet.cell(i,j).value)
				j = j + 1
				pass
			data.append(row)
			i = i+1
			pass
		f = data[:][0]
		mag = data[:][1]
		phase = data[:][2]

		f = [float(i) for i in f]
		mag = [float(i) for i in mag]
		phase = [float(i) for i in phase]

		data = [f, mag, phase]
		return data
