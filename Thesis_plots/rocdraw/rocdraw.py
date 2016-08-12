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

def Draw_PSB_Distr( cell, x_key, y_key, c1, output_dir, hypos ):

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

    hypo_prints = {
        'SL_2qW_NewTF'         : 'Default',
        'SL_2qW_sj_NewTF'      : 'With subjets',
        'SL_2qW_sj_perm_NewTF' : 'With subjets + perm.',
        }

    hypo_colors = {
        'SL_2qW_NewTF'         : 2,
        'SL_2qW_sj_NewTF'      : 4,
        'SL_2qW_sj_perm_NewTF' : 8,
        }

    Q1 = True
    if Q1:
        hypo_prints = {
            'SL_1qW_NewTF'         : 'Default',
            'SL_1qW_sj_NewTF'      : 'With subjets',
            'SL_1qW_sj_perm_NewTF' : 'With subjets + perm.',
            }

        hypo_colors = {
            'SL_1qW_NewTF'         : 2,
            'SL_1qW_sj_NewTF'      : 4,
            'SL_1qW_sj_perm_NewTF' : 8,
            }

    # Starting coordinates and variables for labels
    anchorx  = 0.74
    anchory  = 0.88
    nl       = 0.05
    nc       = 0.14

    for hypo in hypos:

        anchory -= 0.02
        lbl.SetTextColor(hypo_colors[hypo])
        lbl.DrawText( anchorx, anchory, hypo_prints[hypo] )
        lbl.SetTextColor(1)
        anchory -= nl

        for key in [ 'sig', 'bkg' ]:

            # Load hist
            hist = cell.mem_hist_dict[hypo][key]

            # Set style
            hist.SetLineWidth(2)
            if key=='bkg': hist.SetLineStyle(2)
            hist.SetLineColor(hypo_colors[hypo])

            #hist.Scale( 1, "width" )
            hist.Scale( 1.0 / hist.Integral() )

            # Draw
            hist.Draw('HISTSAME')

            # Save minimum and maximum for plot range
            histmaxs.append( hist.GetMaximum() )
            histmins.append( hist.GetMinimum() )

            # Add count label
            lbl.DrawText( anchorx, anchory , '{0} entries'.format(key) )
            lbl.DrawText( anchorx+nc, anchory, '{0:.0f}'.format(hist.GetEntries()))
            anchory -= nl

    #base_hist.SetMinimum( min(histmins) )
    base_hist.SetMinimum( 0.01 )
    base_hist.SetMaximum( max(histmaxs) * 2 )

    c1.Update()

    fn_output = output_dir + '/plots/hist_{0}_{1}.pdf'.format(x_key,y_key)
    c1.Print( fn_output , 'pdf' )



def Draw_ROC_Curve( cell, x_key, y_key, c1, output_dir, hypos ):

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


    hypo_prints = {
        'SL_2qW_NewTF'         : 'Default',
        'SL_2qW_sj_NewTF'      : 'With subjets',
        'SL_2qW_sj_perm_NewTF' : 'With subjets + perm.',
        }

    hypo_colors = {
        'SL_2qW_NewTF'         : 2,
        'SL_2qW_sj_NewTF'      : 4,
        'SL_2qW_sj_perm_NewTF' : 8,
        }

    Q1 = True
    if Q1:
        hypo_prints = {
            'SL_1qW_NewTF'         : 'Default',
            'SL_1qW_sj_NewTF'      : 'With subjets',
            'SL_1qW_sj_perm_NewTF' : 'With subjets + perm.',
            }

        hypo_colors = {
            'SL_1qW_NewTF'         : 2,
            'SL_1qW_sj_NewTF'      : 4,
            'SL_1qW_sj_perm_NewTF' : 8,
            }



    anchorx  = 0.15
    anchory  = 0.25
    nl       = 0.05

    for hypo in hypos:

        lbl.SetTextColor(hypo_colors[hypo])
        lbl.DrawText( anchorx, anchory, hypo_prints[hypo] )
        anchory -= nl

        # Load roc TGraph
        roc = cell.ROC_TGraphs_dict[hypo]

        roc.SetLineColor(hypo_colors[hypo])
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

    fn_output = output_dir + '/plots/roc_{0}_{1}.pdf'.format(x_key,y_key)
    c1.Print( fn_output , 'pdf' )


########################################
# Main
########################################

def main():

    # ==================================
    # Set up ROOT

    ROOT.gROOT.Reset()
    ROOT.gROOT.SetBatch(True)
    ROOT.gROOT.ProcessLine("gErrorIgnoreLevel = 1001;")

    ROOT.gStyle.SetOptFit(1011)
    ROOT.gStyle.SetOptStat(0)

    ROOT.TH1.SetDefaultSumw2(True)


    # ==================================

    # Specify output_dir

    #output_dir = 'V12_v3_nocut'
    #output_dir = 'V12_v3_ETN16'
    #output_dir = 'V12RESTRUCT_v5_nocut'
    #output_dir = 'V12R_v5_WP5'
    #output_dir = 'V12R_v5_HC_1b'
    output_dir = 'V12_1Q/nocut'

    xy_keys = [
        #( 'All', 'All' ),
        #( 'All', 'ETN7' ),
        #( 'All', 'ETN9' ),
        #( 'nonpass_2qW_def', 'ETN16' ),

        #( 'All', 'All' ),
        #( 'All', '1excluded'),
        #( 'nonpass_2qW_def', '0excluded'),
        #( 'All', '23excluded'),

        #( 'All', 'All' ),
        #( 'All', 'higgs_bb1' ),
        #( 'All', 'higgs_ns1' ),
        #( 'All', 'higgs_nsbb' ),

        ( 'All', 'All' ),
        ( 'All', '1excluded'),

        ]

    hypos = [
        #'SL_2qW_NewTF',
        #'SL_2qW_sj_NewTF',
        #'SL_2qW_sj_perm_NewTF',

        'SL_1qW_NewTF',
        'SL_1qW_sj_NewTF',
        'SL_1qW_sj_perm_NewTF',
        ]



    if not os.path.isdir( output_dir + '/plots' ):
        os.makedirs( output_dir + '/plots' )

    # Opening pickle file
    print 'Opening pickle file ' + output_dir + '/MEM_Table.pickle ...'
    f_pickle = open( output_dir + '/MEM_Table.pickle' )
    MEM_Table = pickle.load( f_pickle )
    f_pickle.close()
    print '    Opened successfully'


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








########################################
# End of Main
########################################
if __name__ == "__main__":
    main()
