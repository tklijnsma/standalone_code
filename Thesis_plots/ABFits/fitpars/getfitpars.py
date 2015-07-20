#!/usr/bin/env python
"""
Dictionay and pickle test

"""

########################################
# Imports
########################################

import pickle
import ROOT

from TFClasses import function
from TFClasses import TF

########################################
# Main
########################################

def Draw_Hists_and_Fits():

    # Load the found transfer functions
    pickle_f = open( 'TFMatrix.dat', 'rb' )
    TFMat = pickle.load( pickle_f )
    pickle_f.close()

    for particle in [ 'b', 'l' ]:
        for i_eta in [ 0, 1 ]:

            f_out = open( 'fitpars_{0}{1}.txt'.format(particle,i_eta), 'w' )

            for (ABFnr, func) in enumerate(
                TFMat[particle][i_eta].AcrossBinFuncs ):

                if ABFnr==0: continue

                for val in func.par_values:
                    f_out.write( str(val) + ',' )

                f_out.write('\n')

            f_out.close()

                



########################################
# End of Main
########################################
def main():
    Draw_Hists_and_Fits()

if __name__ == "__main__":
  main()
