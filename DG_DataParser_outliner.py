################################################################################
# DG_DataParser.py
#
# This file is designed to read in data outputted by DG++. In particular the
# load step files with the displacement data.
#
# Created: 11 Feb 2010 NE
#
################################################################################
# import modules
import os as os				#import OS funcitons for directory stuff
from numpy import *			#this loads the numpy module
import matplotlib.pyplot as mp		#import of plotting module
import time as time

devPath = 'C:\\Users\\Noe\\Documents\\BDML\\CodeDev\\PythonScratch\\'
os.chdir(devPath)

import noe as noe
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

# This produces the base outline and nodes that represent it
outlinePts = noe.findOutline(nodeData,noe.createConnectionMat(elementList-1))


mp.figure()
start = time.time()
for i in range(lastNum+1):
    filename = myPath+(fileFormatStr % i)
    fHandle = open(filename)
    rawTxt = fHandle.readlines()
    # Parse out the data from txt file
    nodeData = vstack(importDataLines(rawTxt))
    x = nodeData[:,0]
    y = nodeData[:,1]
    
    mp.plot(x[outlinePts],y[outlinePts])
    mp.axis([-4.25,4.25,-8.5,0])
    outFile = str('fileOut_%05d.png' % i)
    mp.savefig(outFile,dpi=100)
    print 'Wrote File', outFile
    mp.clf()

end = time.time()

print str('Elapsed %f secs' % (end-start))