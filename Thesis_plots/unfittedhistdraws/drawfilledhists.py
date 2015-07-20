#!/usr/bin/env python
"""
Thomas:

Examples on how to use TFMatrix.dat

2 plots are created: 1 transfer function, and 1 cumulative distribution function

"""

########################################
# Imports
########################################

import pickle
import ROOT
import os


def Make_images( fn_out, c1 ):

    c1.Print( fn_out + '.pdf' ,'pdf')

    img = ROOT.TImage.Create()
    img.FromPad(c1)
    img.WriteImage( fn_out + '.png' )



########################################
# Main
########################################

def main():

    ROOT.gROOT.SetBatch(True)
    ROOT.gROOT.ProcessLine("gErrorIgnoreLevel = 1001;")
    ROOT.gStyle.SetOptFit(1011)
    ROOT.gStyle.SetOptStat(0)

    #ROOT.gStyle.SetTitleSize(0.3, "t")

    #ROOT.gStyle.SetTitleH(0.1)
    ROOT.gStyle.SetTitleW(0.44)
    ROOT.gStyle.SetTitleY(0.97)

    c1 = ROOT.TCanvas("c1","c1",500,400)
    c1.SetGrid()

    outputdir = 'plots'

    if not os.path.isdir( outputdir ):
        os.makedirs( outputdir )


    # Open hist matrix
    pickle_f = open( 'SBF_hists_pickle.dat' , 'rb' )
    histmat = pickle.load( pickle_f )
    pickle_f.close()


    particles = [ 'b' , 'l' ]
    etas = [ 0 , 1 ]
    pts = [ 0, 1, 2, 3, 4, 5, 54, 55, 56, 57 ]


    for particle in particles:
        for i_eta in etas:
            for i_pt in pts:

                hist = histmat[particle]['hist_mat'][i_eta][i_pt]

                pt_low = histmat[particle]['E_axis'][i_eta][i_pt]
                pt_high = histmat[particle]['E_axis'][i_eta][i_pt+1]

                if i_eta == 0: eta_low = 0.0; eta_high = 1.0
                else: eta_low = 1.0; eta_high = 2.5

                if particle == 'b': part_str = 'Bottom'
                else: part_str = 'Light'

                second_line = '{0} #leq #eta #leq {1}, {2} #leq p_{{T}} #leq {3}'.format(
                    eta_low, eta_high, pt_low, pt_high )

                hist.SetTitle( '#splitline{' + part_str + ' quark transfer function}{' + second_line + '}' )


                hist.GetXaxis().SetTitle("p_{T} (GeV)")

                hist.Draw() 





                fn_out = outputdir + '/cell_{0}_{1}_{2}'.format( particle, i_eta, i_pt )
                Make_images( fn_out, c1 )







########################################
# End of Main
########################################
if __name__ == "__main__":
  main()
