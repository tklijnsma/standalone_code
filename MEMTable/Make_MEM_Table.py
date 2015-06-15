#!/usr/bin/env python
"""
Thomas: Creates mem plot
"""


########################################
# Imports
########################################

import os
import shutil
import copy
import ROOT
import TTH.TTHNtupleAnalyzer.AccessHelpers as AH
from itertools import cycle

from MEM_Table_config import MEM_Table_configuration


########################################
# Functions
########################################

def Get_hist_efficiency( hist ):

    n_bins = hist.GetSize() - 2 # Subtract for underflow and overflow bins
    n_entries = hist.GetEntries()

    if n_entries == 0:
        return [ 0.0, 1.0 ]

    # Create list of values between 0.0 and 1.0
    N = 100
    Dcuts = [ float(x)/N for x in range(N-1,-1,-1) ]

    # Create iterable object and call the first element
    iter_Dcuts = cycle( Dcuts )
    Dcut = iter_Dcuts.next()

    bin_width = hist.GetBinWidth(0)

    # Initialize sum of bin contents
    n = 0

    # Initialize efficiency list
    eff = []

    # By definition zero integral
    eff.append( 0.0 )

    # Loop: Start with the last bin, and continuously sum up bins. As soon as a cut
    # value of sig/(sig+const(bkg) is reached, save the efficiency

    for i_bin in range(99,-1,-1):
        
        n += hist.GetBinContent(i_bin)

        # sig/(sig+const(bkg) = i_bin * bin_width; if a cut is reached, save 
        # efficiency
        if i_bin * bin_width < Dcut:
            Dcut = iter_Dcuts.next()
            eff.append( n / float( n_entries ) )

    # By definition the full integral
    eff.append( 1.0 )

    return eff


def Get_ROC_TGraph( sig_eff, bkg_eff ):

    if len(sig_eff) != len(bkg_eff):
        print 'Warning: efficiency lists are not equally sized. Ignoring some points'
        print '    len(sig_eff) = {0}, len(bkg_eff) = {1}'.format(
            len(sig_eff), len(bkg_eff) )

    n_points = min( len(sig_eff), len(bkg_eff) )

    ROC = ROOT.TGraph( n_points )

    for i in range(n_points):
        ROC.SetPoint( i, sig_eff[i], 1.0-bkg_eff[i] )

    return ROC
        



########################################
# Classes
########################################

class MEM_Tablecell_Object():

    def __init__( self, x_key, y_key ):

        self.x_key = x_key
        self.y_key = y_key

        self.draw_dict      = {}
        self.mem_hist_dict  = {}
        self.histnames_dict = {}
        self.sel_strs       = {}

        self.ROC_TGraphs_dict = {}
        self.MEM_html_link_dict = {}


    def Set_draw_strs( self, comparison_key,
                             hypo_ver,   hypo_hor,
                             i_hypo_ver, i_hypo_hor,
                             bkg_constant ):

        self.histnames_dict[comparison_key] = {}
        self.draw_dict[comparison_key] = {}

        for ( i_hypo, hypo ) in [ ( i_hypo_ver, hypo_ver ),
                                  ( i_hypo_hor, hypo_hor ) ] :

            self.histnames_dict[comparison_key][hypo] = {}
            self.draw_dict[comparison_key][hypo] = {}

            for key in [ 'sig', 'bkg' ]:

                # Dictionary of histogram names
                self.histnames_dict[comparison_key][hypo][key] = \
                    '{0}_{1}_{2}_{3}_{4}'.format(
                        comparison_key,
                        hypo,
                        key,
                        self.x_key,
                        self.y_key,
                        )

                # Dictionary of draw strings per histogram
                self.draw_dict[comparison_key][hypo][key] = \
                    'mem_tth_p[{0}]/(mem_tth_p[{0}]+{1}*mem_ttbb_p[{0}])' \
                    '>>{2}(100,0.0,1.0)'.format(
                        i_hypo,
                        bkg_constant,
                        self.histnames_dict[comparison_key][hypo][key],
                        )

        # Only select non-zero results
        # (This is the only selection that differs for hypo_hor and hypo_ver,
        # but it is still the same for sig and bkg)
        self.sel_strs[comparison_key] = {
            hypo_ver : 'mem_tth_p[{0}]+{1}*mem_ttbb_p[{0}]>0'.format(
                        i_hypo_ver, bkg_constant ),
            hypo_hor : 'mem_tth_p[{0}]+{1}*mem_ttbb_p[{0}]>0'.format(
                        i_hypo_hor, bkg_constant ),
            }


    def Print_Object(self): # OUTDATED
        print '\n============================='
        print 'Class MEM_Tablecell_Object: '\
              'x_key = {0:10s}, y_key = {1:10s}'.format( self.x_key, self.y_key )

        for key in self.draw_dict:
            print '---------------\nDraw strings: {0}'.format(key)
            for draw_str in self.draw_dict[key]:
                print draw_str

        print '---------------\nSel strings:'
        for i in self.sel_strs: print i


    def Create_MEM_ratio_plots( self, comparison_key, hypo_ver, hypo_hor, IO_dict ):

        # Convenient references
        input_dir   = IO_dict['input_dir']
        input_path  = IO_dict['input_path']
        output_dir  = IO_dict['output_dir']
        c1          = IO_dict['root_canvas']

        input_root_fns = { 'sig' : IO_dict['sig_input_root_fn'],
                           'bkg' : IO_dict['bkg_input_root_fn'] }

        # Open up spots to write histograms to
        self.mem_hist_dict[comparison_key] = { 
            hypo_ver : { 'sig' : [ 0, 0 ], 'bkg' : [ 0, 0 ] },
            hypo_hor : { 'sig' : [ 0, 0 ], 'bkg' : [ 0, 0 ] }
            }

        self.MEM_html_link_dict[comparison_key] = {
            hypo_ver : { 'sig' : [ '', '' ], 'bkg' : [ '', '' ] },
            hypo_hor : { 'sig' : [ '', '' ], 'bkg' : [ '', '' ] }
            }

        for key in [ 'sig', 'bkg' ]:

            input_root_file = ROOT.TFile(
                input_path + '/' + input_dir + '/' + input_root_fns[key] )
            input_tree = input_root_file.Get('tree')

            for hypo in [ hypo_ver, hypo_hor ]:

                histname = self.histnames_dict[comparison_key][hypo][key]
                draw_str = self.draw_dict[comparison_key][hypo][key]
                sel_str = self.sel_strs[comparison_key][hypo]

                # Retrieve the histogram
                n_entries = input_tree.Draw( draw_str, sel_str )

                if n_entries > 0:
                    mem_hist = getattr(ROOT, histname ).Clone()
                else:
                    mem_hist = ROOT.TH1F()
                
                mem_hist.SetTitle( '{0}::{1}::{2} ({3} vs. {4})'.format(
                    comparison_key,
                    hypo,
                    key,
                    hypo_ver,
                    hypo_hor,
                    ) )

                # Draw again to display title <-- This should be moved to a 
                #                                 separate function at some point
                mem_hist.Draw()

                # Save the histogram to the cell object
                self.mem_hist_dict[comparison_key][hypo][key] = copy.deepcopy(
                                                                    mem_hist )

                # IO operations
                # ======================================

                fn = 'MR_{0}'.format(histname)
                fn_output = '{0}/plots/{1}'.format( output_dir, fn )

                self.MEM_html_link_dict[comparison_key][hypo][key] = \
                    'plots/{0}'.format(fn)

                # Pdf
                c1.Print( fn_output , 'pdf' )

                # Png
                img = ROOT.TImage.Create()
                img.FromPad(c1)
                img.WriteImage('{0}.png'.format( fn_output ) )


        
    def Create_ROC_TGraphs(self, comparison_key, hypo_ver, hypo_hor, IO_dict ):

        input_dir   = IO_dict['input_dir']
        input_path  = IO_dict['input_path']
        output_dir  = IO_dict['output_dir']
        c1          = IO_dict['root_canvas']

        # Initialize dicts
        eff_dict = { 'sig' : [] , 'bkg' : [] }
        self.ROC_TGraphs_dict[comparison_key] = {}

        for hypo in [ hypo_ver, hypo_hor ]:

            # Get efficiency lists
            for key in [ 'sig', 'bkg' ]:
                eff_dict[key] = Get_hist_efficiency(
                    self.mem_hist_dict[comparison_key][hypo][key] )

            # Get filled TGraph object
            ROC = Get_ROC_TGraph( eff_dict['sig'], eff_dict['bkg'] )

            plottitle = '{0}: {1} vs. {2}\n' \
                        'hor. cat: {3:10s} ver. cat: {4:10s}'.format(
                            comparison_key,
                            hypo_ver, hypo_hor,
                            self.y_key, self.x_key )

            ROC.SetTitle( plottitle )
            ROC.SetMarkerStyle(22);
            ROC.SetMarkerSize(0.6);

            # Store TGraph object in class
            self.ROC_TGraphs_dict[comparison_key][hypo] = ROC


    def Create_ROC_Image( self, compare_dict, IO_dict ):

        # Draw a straight line
        gr_straight = ROOT.TGraph( 2 )
        gr_straight.SetPoint ( 0, 0.0, 1.0 )
        gr_straight.SetPoint ( 1, 1.0, 0.0 )
        gr_straight.SetLineColor(15)
        gr_straight.GetXaxis().SetTitle( 'sig efficiency' );
        gr_straight.GetYaxis().SetTitle( '1 - bkg efficiency' );
        gr_straight.SetTitle( 'vert. cat = {0:15s} hor. cat = {1:15s}'.format(
            self.y_key, self.x_key ) )
        gr_straight.Draw('AL')

        IO_dict['root_canvas'].Update()

        # Starting coordinates and variabeles for labels
        anchorx  = 0.7
        anchory  = 0.85
        endl     = 0.05
        big_endl = 0.07

        # Set label specifics
        lbl = ROOT.TText()
        lbl.SetNDC()
        lbl.SetTextSize(0.04)

        LineColor_counter = 1

        for comparison_key in self.ROC_TGraphs_dict:

            ( hypo_ver, hypo_hor ) = compare_dict[comparison_key]

            for hypo in [ hypo_ver, hypo_hor ]:

                LineColor_counter += 1

                if LineColor_counter == 3: LineColor_counter += 1
                if LineColor_counter == 5: LineColor_counter += 1

                ROC = self.ROC_TGraphs_dict[comparison_key][hypo]
                ROC.SetMarkerColor(LineColor_counter);
                ROC.SetMarkerSize(0.5);
                ROC.SetLineColor(LineColor_counter);

                if not ROC.GetN() == 2:
                    ROC.Draw('LP')

                # Adding labels to plot
                # ======================================

                lbl.SetTextColor(LineColor_counter)
                lbl.DrawText( anchorx,
                              anchory,
                              '{0}::{1}'.format(comparison_key,hypo) )
                anchory -= endl

                lbl.SetTextColor(1)
                lbl.DrawText( anchorx, anchory , 'sig entries' )
                lbl.DrawText(
                    anchorx+0.19,
                    anchory,
                    '{0:.0f}'.format(
                    self.mem_hist_dict[comparison_key][hypo]['sig'].GetEntries()) )
                anchory -= endl

                lbl.DrawText( anchorx, anchory , 'bkg entries' )
                lbl.DrawText(
                    anchorx+0.19,
                    anchory,
                    '{0:.0f}'.format(
                    self.mem_hist_dict[comparison_key][hypo]['bkg'].GetEntries()) )
                anchory -= big_endl

                IO_dict['root_canvas'].Update()

                # IO operations
                # ======================================

                fn = 'ROC_{0}_{1}_{2}'.format( comparison_key,
                                               self.x_key, self.y_key )
                fn_output = IO_dict['output_dir'] + '/plots/' + fn

                # Save html link filename also to class to create the actual table
                self.ROC_html_link   = 'plots/' + fn
                self.ROC_html_anchor = fn

                # Pdf
                IO_dict['root_canvas'].Print( fn_output , 'pdf' )

                # Png
                img = ROOT.TImage.Create()
                img.FromPad( IO_dict['root_canvas'] )
                img.WriteImage('{0}.png'.format( fn_output ) )



########################################
# Main
########################################

def main():

    ########################################
    # Configuration
    ########################################

    config = MEM_Table_configuration()

    input_dir = config.input_dir
    output_dir = config.output_dir
    hypo_dict = config.hypo_dict
    bkg_constant = config.bkg_constant
    compare_dict = config.compare_dict
    sel_list_for_all = config.sel_list_for_all
    x_key_list = config.x_key_list
    y_key_list = config.y_key_list


    ########################################
    # Set up for loop
    ########################################

    ROOT.gROOT.SetBatch(True)
    ROOT.gROOT.ProcessLine("gErrorIgnoreLevel = 1001;")
    ROOT.gStyle.SetOptFit(1011)

    input_path = '/shome/tklijnsm/Samples/MEMresults/'

    sig_input_root_fn = 'tth_V11_13tev.root'
    bkg_input_root_fn = 'ttjets_V11_13tev.root'

    # Clean up output directory
    if os.path.isdir( output_dir ):
        shutil.rmtree( output_dir )
    os.makedirs( output_dir + '/plots' )    

    c1 = ROOT.TCanvas("c1","c1",500,400)
    c1.SetGrid()

    # All IO info contained
    IO_dict = { 'input_path'            : input_path,
                'input_dir'             : input_dir,
                'sig_input_root_fn'     : sig_input_root_fn,
                'bkg_input_root_fn'     : bkg_input_root_fn,
                'output_dir'            : output_dir,
                'root_canvas'           : c1,
              }

    # Initialize MEM_Table
    MEM_Table = {}
    for x_key in x_key_list:
        MEM_Table[x_key] = {}
        for y_key in y_key_list:
            # Initialize a cell
            MEM_Table[x_key][y_key] = MEM_Tablecell_Object(x_key,y_key)


    ########################################
    # Loop over the hypothesis-comparisons
    ########################################

    for comparison_key in compare_dict:

        # Retrieve the hypothesis names
        ( hypo_ver, hypo_hor ) = compare_dict[comparison_key]

        # Get corresponding list index in ROOT MEM branch
        i_hypo_ver = hypo_dict[hypo_ver]
        i_hypo_hor = hypo_dict[hypo_hor]

        print '\nRunning comparison {0}   ( {1} vs. {2} )'.format(
            comparison_key, hypo_ver, hypo_hor )

        # Define selection string dict
        # ======================================

        # Selection may depend on hypothesis, so include it in the loop

        sel_dict = {

            # Horizonal axis

            'All' : [
                ],

            'No_htt' : [
                'nhttCandidate_aftercuts<=0',
                ],

            'htt' : [
                'nhttCandidate_aftercuts>0',
                ],

            '0b_matched' : [
                'nhttCandidate_aftercuts>0',
                'Matching_event_type_number>=1',
                'Matching_event_type_number<=5',
                ],

            '1b_matched' : [
                'nhttCandidate_aftercuts>0',
                'Matching_event_type_number>=6',
                'Matching_event_type_number<=8',
                ],

            '2or3b_matched' : [
                'nhttCandidate_aftercuts>0',
                'Matching_event_type_number>=9',
                'Matching_event_type_number<=11',
                ],

            'NA' : [
                'mem_tth_p[{0}]+{2}*mem_ttbb_p[{0}]>0&&'\
                    'mem_tth_p[{1}]+{2}*mem_ttbb_p[{1}]==0'.format(
                    i_hypo_hor, i_hypo_ver, bkg_constant ),
                ],

            # Vertical axis

            'Cat1' : [
                'cat==1',
                ],

            'Cat2' : [
                'cat==2',
                ],

            'Cat3' : [
                'cat==3',
                ],

            'Cat12' : [
                'cat==1',
                'cat==2',
                ],

            'Cat123' : [
                'cat>=1',
                'cat<=3',
                ],

            'AllCat' : [
                ],

            }


        ########################################
        # Fill the mem table and create figures
        ########################################

        print '    Drawing MEM Ratio plots'

        for x_key in x_key_list:
            for y_key in y_key_list:

                print '        x_key = {0:15s} y_key = {1:15s}'.format(
                    x_key, y_key )

                # Set 'cell' as the current cell for easy reference
                cell = MEM_Table[x_key][y_key]

                # Sets the draw strings and the unique selection strings
                cell.Set_draw_strs( comparison_key,
                                    hypo_ver,   hypo_hor,
                                    i_hypo_ver, i_hypo_hor,
                                    bkg_constant )

                # Initialize list of selection strings
                sel_list = []

                # Load the selection strings from both axes into it
                sel_list.extend( sel_dict[x_key] )
                sel_list.extend( sel_dict[y_key] )
                sel_list.extend( sel_list_for_all )

                # Build the actual selection string
                full_sel_str = '&&'.join( sel_list )

                # Add the full selection string to the selection strings in the class
                if full_sel_str != '':
                    cell.sel_strs[comparison_key][hypo_ver] += '&&' + full_sel_str
                    cell.sel_strs[comparison_key][hypo_hor] += '&&' + full_sel_str

                cell.Create_MEM_ratio_plots( comparison_key,
                                             hypo_ver, hypo_hor,
                                             IO_dict )

                cell.Create_ROC_TGraphs(     comparison_key,
                                             hypo_ver, hypo_hor,
                                             IO_dict )


    print '\nDrawing ROC plots'

    # Draw the ROC after the loop (includes all comparisons)

    c2 = ROOT.TCanvas("c2","c2",600,400)
    c2.SetGrid()
    c2.SetRightMargin(0.32)
    IO_dict['root_canvas'] = c2

    for x_key in x_key_list:
        for y_key in y_key_list:
            MEM_Table[x_key][y_key].Create_ROC_Image(  compare_dict, IO_dict )


    ########################################
    # Creating the html-files
    ########################################

    print 'Creating html files'

    # Create the overview html-files
    hf_overview = open( output_dir + '/' + 'MEM_overview.html' , 'w' )
    hf_overview.write( '<html><body>\n<h1>MEM Ratio plots\n</h1>\n<br>\n<hr />' )

    # Create the table html file
    hf_table = open( '{0}/MEM_Table.html'.format( output_dir ) , 'w' )
    hf_table.write( '<html><body>\n<h1>MEM Table\n</h1>\n<br>\n<hr />' )

    # Fill the overview html files
    for x_key in x_key_list:
        for y_key in y_key_list:
            # Set 'cell' as the current cell for easy reference
            cell = MEM_Table[x_key][y_key]

            for comparison_key in compare_dict:
                hf = hf_overview

                # Write the four MEM Ratio histograms to the overview
                for hypo in compare_dict[comparison_key]:
                    for key in [ 'sig', 'bkg' ]:
                        hf.write(
                            '<a href="{0}"><img width="300" src="{0}.png">' \
                            '</a>\n'.format(
                                cell.MEM_html_link_dict[comparison_key][hypo][key]) )

                # Write the ROC curve plus html anchor to overview
                hf.write('<a name="{0}"></a>\n'.format(cell.ROC_html_anchor) )
                hf.write('<a href="{0}"><img width="300" src="{0}.png">' \
                         '</a>\n'.format(cell.ROC_html_link) )
                hf.write('<br>\n')

    # Fill the table html file
    for y_key in y_key_list:
        for x_key in x_key_list:
            # Set 'cell' as the current cell for easy reference
            cell = MEM_Table[x_key][y_key]

            hf_table.write('<a href="{0}"><img width="250" src="{1}.png">' \
                '</a>\n'.format(
                    'MEM_overview.html#' + cell.ROC_html_anchor,
                    cell.ROC_html_link ) )

        hf_table.write('<br>\n')

    hf_overview.close()
    hf_table.close()

        
########################################
# End of Main
########################################
if __name__ == "__main__":
    main()
