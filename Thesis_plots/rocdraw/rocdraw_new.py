#!/usr/bin/env python
"""
Thomas:

"""

########################################
# Imports
########################################

import pickle
import ROOT
import os

from Make_MEM_Table import MEM_Tablecell_Object
from MEM_Table_config import MEM_Table_configuration


########################################
# Functions
########################################

def Draw_PSB_Distr( MEM_Table, config, c1 ):

    # Set label specifics
    lbl = ROOT.TText()
    lbl.SetNDC()
    lbl.SetTextSize(0.04)

    # Draw base_hist with the axes; other hists will be 'HISTSAME'
    base_hist = ROOT.TH1F()
    base_hist.SetTitle('')
    base_hist.SetXTitle('P_{S/B}')
    base_hist.GetXaxis().SetTitleSize(0.05)
    base_hist.GetXaxis().SetTitleOffset(0.87)
    base_hist.SetYTitle('Fraction of events')
    base_hist.GetYaxis().SetTitleSize(0.05)
    base_hist.GetYaxis().SetTitleOffset(0.87)
    base_hist.Draw()

    # ==================================
    # Manual legend
    lx = 0.57
    ly = 0.85

    l = ROOT.TLine()
    l.SetNDC()
    l.SetLineWidth(2)
    l.SetLineColor(1)

    l.SetX1(lx)
    l.SetX2(lx+0.05)
    l.SetY1(ly)
    l.SetY2(ly)
    l.Draw('SAME')

    l2 = ROOT.TLine()
    l2.SetNDC()
    l2.SetLineWidth(2)
    l2.SetLineColor(1)
    l2.SetLineStyle(2)
    l2.SetX1(lx)
    l2.SetX2(lx+0.05)
    l2.SetY1(ly-0.05)
    l2.SetY2(ly-0.05)
    l2.Draw('SAME')

    lbl.DrawText( lx + 0.06, ly-0.01, ': sig' )
    lbl.DrawText( lx + 0.06, ly-0.06, ': bkg' )
    # ==================================

    histmins = [0.0]
    histmaxs = []

    # Starting coordinates and variables for labels
    anchorx  = 0.74
    anchory  = 0.88
    nl       = 0.05
    nc       = 0.14

    for ( ID, x_key, y_key, hypo ) in config.hypo_list:

        anchory -= 0.02
        lbl.SetTextColor( config.hypo_colors[ID] )
        lbl.DrawText( anchorx, anchory, config.hypo_prints[ID] )
        lbl.SetTextColor(1)
        anchory -= nl

        integral = {}

        for key in [ 'sig', 'bkg' ]:

            # Load hist
            hist = MEM_Table[x_key][y_key].mem_hist_dict[hypo][key]

            # Set style
            hist.SetLineWidth(2)
            if key=='bkg': hist.SetLineStyle(2)
            hist.SetLineColor( config.hypo_colors[ID] )

            integral[key] = float(hist.Integral())
            hist.Scale( 1.0 / integral[key] )

            # Draw
            hist.Draw('HISTSAME')

            # Save minimum and maximum for plot range
            histmaxs.append( hist.GetMaximum() )
            histmins.append( hist.GetMinimum() )

            # Add count label
            lbl.DrawText( anchorx, anchory , '{0} events'.format(key) )
            lbl.DrawText( anchorx+nc, anchory, '{0:.1f}'.format(integral[key]))
            anchory -= nl

        lbl.DrawText( anchorx, anchory , 'S/B'.format(key) )
        lbl.DrawText( anchorx+nc, anchory, '{0:.2f}'.format(
            integral['sig'] / integral['bkg'] ))
        anchory -= nl

    base_hist.SetMinimum( 0.01 )
    base_hist.SetMaximum( max(histmaxs) * 2 )

    c1.Update()

    fn_output = config.output_dir + '/hist_{0}.pdf'.format(config.name)
    c1.Print( fn_output , 'pdf' )



def Draw_ROC_Curve( MEM_Table, config, c1 ):

    # Set label specifics
    lbl = ROOT.TText()
    lbl.SetNDC()
    lbl.SetTextSize(0.04)
    #lbl.SetTextAlign(31)

    # Draw base_graph with the axes; other hists will be 'HISTSAME'
    base_graph = ROOT.TGraph(2)
    base_graph.SetPoint(0, 0.0, 1.0)
    base_graph.SetPoint(1, 1.0, 0.0)
    base_graph.SetLineColor(13)
    base_graph.SetLineWidth(2)
    base_graph.Draw('AL')
    base_graph.SetTitle('')
    base_graph.GetXaxis().SetTitle('#varepsilon_{sig}')
    base_graph.GetXaxis().SetTitleSize(0.05)
    base_graph.GetXaxis().SetTitleOffset(0.9)
    base_graph.GetXaxis().SetLimits(0.0,1.0)
    base_graph.GetYaxis().SetTitle('1-#varepsilon_{bkg}')
    base_graph.GetYaxis().SetTitleSize(0.05)
    base_graph.GetYaxis().SetTitleOffset(0.9)
    base_graph.SetMaximum(1.0)
    #base_graph.GetYaxis().SetLimits(0.0,1.0)

    anchorx  = 0.15
    anchory  = 0.25
    nl       = 0.05

    for ( ID, x_key, y_key, hypo ) in config.hypo_list:

        lbl.SetTextColor( config.hypo_colors[ID] )
        lbl.DrawText( anchorx, anchory, config.hypo_prints[ID] )
        anchory -= nl

        # Load roc TGraph
        roc = MEM_Table[x_key][y_key].ROC_TGraphs_dict[hypo]

        roc.SetLineColor( config.hypo_colors[ID] )
        roc.SetLineWidth(2)

        roc.Draw('L')

        """
        e_int = 0.6
        e_bkg = roc.Eval(e_int)
        print 'Hypothesis {0} eff. interpolation'.format(hypo_prints[hypo])
        print '    e_sig = {0}; e_bkg = {1}; surv. bkg = {2}'.format(
            e_int, e_bkg, 1-e_bkg )
        """

    c1.Update()

    fn_output = config.output_dir + '/roc_{0}.pdf'.format(config.name)
    c1.Print( fn_output , 'pdf' )


########################################
# Main
########################################

def roc_main( config ):

    # ==================================
    # Set up ROOT

    ROOT.gROOT.Reset()
    ROOT.gROOT.SetBatch(True)
    ROOT.gROOT.ProcessLine("gErrorIgnoreLevel = 1001;")

    ROOT.gStyle.SetOptFit(1011)
    ROOT.gStyle.SetOptStat(0)

    ROOT.TH1.SetDefaultSumw2(True)


    # ==================================

    # Specify output_dir; this is the location of MEM_Table.pickle
    output_dir = config.output_dir
    input_dir = config.input_dir


    #if not os.path.isdir( output_dir + '/plots' ):
    #    os.makedirs( output_dir + '/plots' )
    if not os.path.isdir( output_dir ):
        os.makedirs( output_dir )

    # Opening pickle file
    print 'Opening pickle file ' + input_dir + '/MEM_Table.pickle ...'
    f_pickle = open( input_dir + '/MEM_Table.pickle' )
    MEM_Table = pickle.load( f_pickle )
    f_pickle.close()
    print '    Opened successfully'


    """
    for x_key, y_key in xy_keys:

        # Get cell
        cell = MEM_Table[x_key][y_key]

        c1 = ROOT.TCanvas("c1","c1",600,400)
        c1.SetLogy()
        c1.SetRightMargin(0.28)
        Draw_PSB_Distr( cell, x_key, y_key, c1, output_dir, hypos )

        c2 = ROOT.TCanvas("c2","c2",400,400)
        c2.SetGrid()
        Draw_ROC_Curve( cell, x_key, y_key, c2, output_dir, hypos )
    """

    c1 = ROOT.TCanvas("c1","c1",600,400)
    c1.SetLogy()
    c1.SetRightMargin(0.28)
    Draw_PSB_Distr( MEM_Table, config, c1 )

    c2 = ROOT.TCanvas("c2","c2",400,400)
    c2.SetGrid()
    Draw_ROC_Curve( MEM_Table, config, c2 )








########################################
# End of Main
########################################
if __name__ == "__main__":
    roc_main()
