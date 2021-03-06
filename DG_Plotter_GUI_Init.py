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
import time

devPath = 'C:\\Users\\Noe\\Documents\\BDML\\CodeDev\\PythonScratch\\'
#devPath ='/Users/noe/Documents/BDML/CodeDev/PythonScratch/'
os.chdir(devPath)

import noe
import Tkinter				#import dialog box stuff
from tkFileDialog import askdirectory

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
#myPath = 'C:\\Users\\Noe\\Documents\\BDML\\CodeDev\\PythonScratch\\wedge3umTipFillet\\'
root = Tkinter.Tk()	# initiliases the window system
root.withdraw()
myPath = askdirectory(parent = root, title ='Select Data Directory')
root.destroy()	# window cleanup

fileFormatStr = 'preload00in00out_%05d.dat'
fileRefMesh = 'RefMesh.dat'



#change the current directory
os.chdir(myPath)
dirListing = os.listdir('.')
lastNum = 0
for tmp in dirListing:
    if tmp.startswith('preload'):
        lastNum += 1

#### Load up the RefMesh to determine base lines
filename = os.path.join(myPath,fileRefMesh)

# Load file and read in lines
fHandle = open(filename)
rawTxt = fHandle.readlines()
# Parse out the data from txt file
nodeData = vstack(importDataLines(rawTxt))
elementList = vstack(importElementLines(rawTxt))
fHandle.close()

# This produces the base outline and nodes that represent it
mp.ioff() #this forces interactive mode to not plot during running

outlinePts = noe.findOutline(nodeData,noe.createConnectionMat(elementList-1))
x = nodeData[:,0]
y = nodeData[:,1]
mp.figure()
mp.plot(x[outlinePts],y[outlinePts])
xmin,xmax = mp.xlim()
mp.hlines([-8.5],xmin,xmax,colors='k')
mp.axis('equal')
ymin,ymax = mp.ylim()
xmin,xmax = mp.xlim()
mp.clf()

start = time.time()
for i in range(lastNum):
    filename = os.path.join(myPath,(fileFormatStr % i))
    fHandle = open(filename)
    rawTxt = fHandle.readlines()
    # Parse out the data from txt file
    nodeData = vstack(importDataLines(rawTxt))
    fHandle.close()
    x = nodeData[:,0]
    y = nodeData[:,1]
    
    mp.plot(x[outlinePts],y[outlinePts])
    mp.hlines([-8.5],xmin,xmax,colors='k')
    mp.axis([xmin,xmax,ymin,ymax])
    outFile = str('fileOut_%05d.png' % i)
    mp.savefig(outFile,dpi=100)
    print 'Wrote File', outFile
    mp.clf()

end = time.time()

print str('Elapsed %f secs' % (end-start))

mp.ion()