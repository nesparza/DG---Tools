# -*- coding: utf-8 -*-
"""
Created on Mon Jul 26 11:03:57 2010
DG++ Numerical Base Calc

With this script I will be able to produce the parameters in the number base
of interest. This would scale the simulation correctly.

For example, I could calculate the material parameters in the base of
10 microns.

Input Paramters (M,N,J base):
length unit
LJ constants
Material constants

Output Parameters - scaled to length unit:
LJ constants
Lame material constants

@author: Noe
"""
debug = 1

# Import Library Section
import numpy as np			#this loads the numpy module as np
# End Import Section

# Define the SI base for the Sim parameters
baseLength    = 10e-6    # Meters
baseYoungsMod = 1.75e6   # N/M^2
nu            = 0.45     # poission ratio
baseLJsigma   = 1e-9     # M
baseLJepi     = 0.6e3     # J/mol - energy

# BEGIN main code

# Calculate scaled Lame Material Constants
if debug == 1:
    # SI base lame constants
    baseLameMu = baseYoungsMod/(2*(1+nu))
    baseLameLambda = (baseYoungsMod*nu)/((1+nu)*(1-2*nu))
    
    print "%s %0.2e\n"*2 % ("base Mu:", baseLameMu, "base Lambda:", 
    baseLameLambda)

# Scale Young's Modulus
scaledYoungsMod = baseYoungsMod * baseLength**2.0

# Scale Lame Constants
scaledLameMu = scaledYoungsMod/(2*(1+nu))
scaledLameLambda = (scaledYoungsMod*nu)/((1+nu)*(1-2*nu))

if debug == 1:
    print "%s %0.2e\n"*3 % ("Scaled E:", scaledYoungsMod,
    "Scaled Mu",scaledLameMu,"Scaled Lambda",scaledLameLambda)

# Scale LJ Constants
scaledLJsigma = baseLJsigma / baseLength
scaledLJepi = baseLJepi # energy doesnt need to be scaled?

if debug == 1:
    print "%s %0.2e\n"*2 % ("Scaled LJ Sigma:",scaledLJsigma,
    "Scaled LJ Epislon:",scaledLJepi)