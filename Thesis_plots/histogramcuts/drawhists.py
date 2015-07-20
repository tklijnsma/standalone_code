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

    c1 = ROOT.TCanvas("c1","c1",500,400)
    c1.SetGrid()

    outputdir = 'plots'

    if not os.path.isdir( outputdir ):
        os.makedirs( outputdir )

    part = 'b0'

    # Open hist bc
    pickle_f = open( 'histogramming_output/pt_hist_bc_{0}.pickle'.format(part) , 'rb' )
    pt_hist_bc = pickle.load( pickle_f )
    pickle_f.close()

    # Open hist ac
    pickle_f = open( 'histogramming_output/pt_hist_ac_{0}.pickle'.format(part) , 'rb' )
    pt_hist_ac = pickle.load( pickle_f )
    pickle_f.close()

    # Read bin boundaries
    f_in = open( 'histogramming_output/pt_bins_{0}.txt'.format(part), 'r' )






    lines = []
    while True:
        line = f_in.readline()
        if not line: break
        line = line.strip()
        lines.append( line )
    f_in.close()

    pt_axis = [ eval(i) for i in lines[3:] ]



    # BC
    # ==============================

    pt_hist_bc.SetTitle('')    
    pt_hist_bc.Draw()
    pt_hist_bc.SetMaximum( 500000.0 )

    fn_out = outputdir + '/pt_hist_bc'
    Make_images( fn_out, c1 )



    # AC
    # ==============================

    pt_hist_ac.SetTitle('')
    pt_hist_ac.Draw()
    pt_hist_ac.SetMaximum( 500000.0 )

    fn_out = outputdir + '/pt_hist_ac'
    Make_images( fn_out, c1 )



    # AC with vertical lines
    # ==============================

    v_lines = []
    for pt in pt_axis:

        # Get y-value of histogram at this pt
        bin_nr = pt_hist_ac.GetXaxis().FindBin(pt)
        y_max = pt_hist_ac.GetBinContent(bin_nr)

        l = ROOT.TLine( pt, 0.0, pt, y_max )
        l.SetLineStyle(1)
        #l.SetLineColor(13)
        l.SetLineColor(2)
        l.SetLineWidth(1)
        v_lines.append(l)

    for l in v_lines:
        l.Draw("SAME")
        c1.Update()

    fn_out = outputdir + '/pt_hist_ac_lines'
    Make_images( fn_out, c1 )







########################################
# End of Main
########################################
if __name__ == "__main__":
  main()
