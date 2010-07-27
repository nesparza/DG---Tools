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
# Import Library Section
# End Import Section

class DGParams:
    scaledEMod = 1.0
    scaledLJsigma = 1.0
    scaledLJepi = 1.0
    scaledLameMu = 1.0
    scaledLameLambda = 1.0
    
    def __init__(self,baseLength = 10e-6,baseEMod = 1.75e6,baseLJsigma = 1e-9,
    baseLJepi = 0.6e3, nu = 0.45):
        self.baseLength = baseLength
        self.baseEMod = baseEMod
        self.baseLJsigma = baseLJsigma
        self.baseLJepi = baseLJepi
        self.nu = nu
    
    def scaleParams(self):
        self.scaledEMod = self.baseEMod * self.baseLength**2.0
        self.scaledLameMu = self.scaledEMod/(2*(1+self.nu))
        self.scaledLameLambda = (self.scaledEMod*self.nu)/((1+self.nu)*(1-2*self.nu))
        self.scaledLJsigma = self.baseLJsigma / self.baseLength
        self.scaledLJepi = self.baseLJepi # energy doesnt need to be scaled?
    
    def _Print(self):
        string_base = "Base - Length: %.2e EMod: %.2e LJSigma: %.2e LJEpi: %2e"\
        % (self.baseLength, self.baseEMod, self.baseLJsigma, self.baseLJepi)
        string_scaled = "Scaled - Emod: %.2e LameMu: %.2e LameLambda: %.2e LJSigma: %.2e LJEpi: %.2e" \
        % (self.scaledEMod, self.scaledLameMu, self.scaledLameLambda, self.scaledLJsigma, self.scaledLJepi)
        
        return "%s \n%s" % (string_base, string_scaled)

    def Print(self):
        print self._Print()
        


# BEGIN main code
def main():
    debug = 1
    simNewBase= DGParams()
    simNewBase.scaleParams()

    if debug == 1:
        simNewBase.Print()

if __name__ == '__main__':
    main()

# END main code
