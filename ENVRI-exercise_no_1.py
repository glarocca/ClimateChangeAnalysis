#!/usr/bin/env python3

# 1. Connect to the Climate Change Knowledge Portal at: sdwebx.worldbank.org/climateportal/index.cfm
# 2. Click on the area of the map of interest to get start
# 3. Click on the region to view regional data
# 4. Click to download historical data
# 5. Select Temperature, Country and Time Period and click on Download Data to Excel
# 6. Use the below script to analyse the regional data and plot results
# 7. TODO: Adjust the script to plot the rainfall in the region of interest 

import matplotlib.pyplot as plt
import datetime as dt
import urllib.request
import xlrd


def get_datasets(url, prefix):
	#with urllib.request.urlopen(url) as filedata:
	#	datatowrite = filedata.read()
	filedata = urllib.request.urlopen(url)
	datatowrite = filedata.read()

	# Saving file
	filename = 'datasets_%s.xls' %prefix
	with open(filename, 'wb') as f:  
		f.write(datatowrite)


def read_datasets(file):
	book = xlrd.open_workbook(file)
	sheet = book.sheets()[0]

	raws = []
	x = []
	y = []

	for i in range(sheet.nrows):
		raws.append(sheet.row_values(i))

	# Removing header from the sheet
	raws.pop(0)

	return raws


def calculate_average_temperature(raws):

	total=average=0.0
	index=1
	x = []
	y = []

	for item in raws:
		print(item)
		temp=item[0]
		year=item[1]
		country=item[3]

		index=index+1
		total=total+temp

		if (index==13):
			# Calculate the average temp. for each year
			average=total/12
			print("Year [ %d ], average temperature = %f year" %(int(year), average))
			print("")

			x.append(year)
			y.append(average)
		
			index=1
			total=average=0.0

	return (x,y)


def do_plot (x, y, title, xlabel, ylabel, filename):
        # Plotting
        plt.plot(x,y, label=title, linewidth=3)
        plt.gcf().autofmt_xdate()
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)

        plt.title(title)
        plt.legend()
        plt.rcParams["figure.figsize"]=[15,10]
        plt.show()
        plt.savefig(filename, dpi=300)


def main():
	
	# Fetching datasets to be processed
	datatowrite = get_datasets('http://sdwebx.worldbank.org/climateportal/DownloadData/tas_1991_2015.xls', 'amt')

	# Reading the excel file for processing
	raws = read_datasets('datasets_amt.xls')

	# Calculate the average monthly temperature
	x1,y1 = calculate_average_temperature(raws)

	# Plotting datasets
	do_plot(x1,y1, 'Average Monthly Temperature', 'Year', 'Temperature (°C)', 'AMT.png')
	


if __name__ == "__main__":
        main()

