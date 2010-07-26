################################################################################
# DG_DataParser.py
#
# This file is designed to read in data outputted by DG++. In particular the
# load step files with the displacement data.
#
# Created: 8 Feb 2010 NE
#
################################################################################
# import modules
import os as os				#import OS funcitons for directory stuff
from numpy import *			#this loads the numpy module
import matplotlib.pyplot as mp		#import of plotting module
#import scipy.stats as stats
import time as time

# import Tkinter				#import dialog box stuff
# from tkFileDialog import askopenfilename

# FUNCTION DEFINITIONS
def importDataLines(inTxt):	
	for l in inTxt:
		try:
			if len(l.split()) == 4 or len(l.split()) == 2:
				tempArr = array(l.split(), dtype = float)
				if len(tempArr) == 4:
					output = array([tempArr[0]+tempArr[2], tempArr[1]+tempArr[3]])
				else:
					output = tempArr
				yield output
		except:
			pass
			
def importElementLines(inTxt):	
	for l in inTxt:
		try:
			if len(l.split()) == 3:
				yield array(l.split(), dtype = int)
		except:
			pass
# END FUNCTIONS

# # BEGIN SCRIPT

#filename = 'C:\Users\Noe\Documents\BDML\CodeDev\PythonScratch\wedge3umTipFillet\preload45in00out_00101.dat'
#filename = 'C:\Users\Noe\Documents\BDML\CodeDev\PythonScratch\wedge3umTipFillet\RefMesh.dat'
#filename = '/Users/noe/Documents/BDML/CodeDev/PythonScratch/wedge3umTipFillet/RefMesh.dat'

#myPath = '/Users/noe/Documents/BDML/CodeDev/PythonScratch/wedge3umTipFillet/'
myPath = 'C:\\Users\\Noe\\Documents\\BDML\\CodeDev\\PythonScratch\\wedge3umTipFillet\\'
fileFormatStr = 'preload45in00out_%05d.dat'
fileRefMesh = 'RefMesh.dat'
lastNum = 101


#change the current directory
os.chdir(myPath)

#### Load up the RefMesh to determine base lines
filename = myPath+fileRefMesh

# Load file and read in lines
fHandle = open(filename)
rawTxt = fHandle.readlines()
# Parse out the data from txt file
nodeData = vstack(importDataLines(rawTxt))
elementList = vstack(importElementLines(rawTxt))

# Work with the Element lines
# lets try to find all the unique lines
linePtsArray = vstack((elementList[::,(0,1)],
                       elementList[::,(1,2)],
                       elementList[::,(0,2)]))
# sort so we can more easily identify dups
linePtsArray.sort()

# loop through and remove dups
uniqueLines = []
for pts in linePtsArray:
    if pts.tolist() not in uniqueLines:
        uniqueLines.append(pts.tolist())
arrLines = array(uniqueLines)	#These are the unique lines to plot



# # # Lets loop and save all the figs
mp.figure()
start = time.time()
for i in range(lastNum+1):
	filename = myPath+(fileFormatStr % i)
	fHandle = open(filename)
	rawTxt = fHandle.readlines()
	# Parse out the data from txt file
	nodeData = vstack(importDataLines(rawTxt))
	for pt in arrLines:
	    ptLine = array([[nodeData[pt[0]-1,0],nodeData[pt[0]-1,1]],
	    [nodeData[pt[1]-1,0],nodeData[pt[1]-1,1]]])
	    mp.plot(ptLine[::,0],ptLine[::,1],'b')  
	mp.axis([-4.25,4.25,-8.5,0])
	
	outFile = str('fileOut_%05d.png' % i)
	mp.savefig(outFile,dpi=100)
	mp.clf()

	print 'Wrote File', outFile 
#mp.show()
end = time.time()

print str('Elapsed %f secs' % (end-start))

# plot the nodes
#mp.figure()
#axH = mp.scatter(nodeData[::,0],nodeData[::,1])
#mp.axis([-4.25,4.25,-8.5,0])
#axH.axes.set_aspect('equal')
#mp.draw()


## THIS APPROACH DOESNT WORK
# This will provide the number of times a node is used in a line
# tmpA = stats.itemfreq(arrLines[:,0]) #result is 2D array - COL 0 value COL 1 count
# tmpB = stats.itemfreq(arrLines[:,1])

# indSetA = array(where(tmpA[:,1]<=3))
# indSetB = array(where(tmpB[:,1]<=3))

# setA = arrLines[indSetA,0]
# setB = arrLines[indSetB,1]

# outlineList = []
# for lines in arrLines:
# 	temp1 = array(where(lines[0]==setA))
# 	temp2 = array(where(lines[1]==setB))
# 	if size(temp1) > 0 and size(temp2) > 0:
# 		outlineList.append(lines.tolist())
# arrOutlineLines = array(outlineList)
## END BAD APPROACH