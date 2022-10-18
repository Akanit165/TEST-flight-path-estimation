- This "orbit" directory is a prototype of satellite orbit prediction which contains of two python modules

	1. astro.py for julian date and sidereal time calculation.
	2. test_position.py is the "main" module to compute the satellite position which receive data from "data.csv" (like GNSS) 

- When test_position is executed, there are 2 required input which are the current and future time index.
	Time index is the line of csv file that will be imported to test_position.py : Time index = 1 is the line 2 of csv
	*** For accuracy and result error in tolerance, the future time index should not more than current time index + 10
	For example using current index = 5 for calculate position, then future index should not more than 15 (3 minutes approximately) because the acceleration in 3 axes are not "constant"

- First check your laptop/computer that python is installed
- Install the library

	pip install -r requirements.txt

- Execute test_position.py

	python test_position.py
	
	or
	
	python3 test_position.py
	
	============the result will be shown as below=============
	
	Enter time index (more than 0): 1
	Enter time index to predict (shouldn't more than previous index + 10 for accuracy): 5
	Current date:   01 Jan 2000 12:00:00.034
	Predicted date:   01 Jan 2000 12:01:34.277
	Satellite position in next 1.57 min : {'ECI_X': 7863.814589666271, 'ECI_Y': 962.2945216440564, 'ECI_Z': -242.52678140372112}

 
 
