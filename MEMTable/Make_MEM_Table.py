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


########################################
# Functions
########################################

def Get_hist_efficiency( hist ):

    n_bins = hist.GetSize() - 2 # Subtract for underflow and overflow bins
    n_entries = hist.GetEntries()

    if n_entries == 0:
        return ( [ 0.0, 1.0 ] , 0 )

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

    return ( eff, N )


def Get_ROC_TGraph( sig_eff, bkg_eff ):

    if len(sig_eff) != len(bkg_eff):
        print 'Warning: efficiency lists are not equally sized. Ignoring some points'

    n_points = max( len(sig_eff), len(bkg_eff) )

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

        self.draw_dict = {}
        self.histnames_dict = {}
        self.sel_strs = []

        # Initialize efficiency dict; accessible via eff_dict['sig'/'bkg'][1/0]
        self.eff_dict = { 'sig' : [ [], [] ] , 'bkg' : [ [], [] ] }
        self.mem_hist_dict = { 'sig' : [ 0, 0 ] , 'bkg' : [ 0, 0 ] }


    def Set_draw_strs( self, i_hypo, i_hypo_sj, bkg_constant ):

        sig_histnames = [
            'H_sig_{0}_{1}'.format( self.x_key, self.y_key ),
            'Hsj_sig_{0}_{1}'.format( self.x_key, self.y_key ) ]

        sig_draw_strs = [
            'mem_tth_p[{0}]/(mem_tth_p[{0}]+{1}*mem_ttbb_p[{0}])'\
            '>>{2}(100,0.0,1.0)'.format(
                i_hypo, bkg_constant, sig_histnames[0] ),
            'mem_tth_p[{0}]/(mem_tth_p[{0}]+{1}*mem_ttbb_p[{0}])'\
            '>>{2}(100,0.0,1.0)'.format(
                i_hypo_sj, bkg_constant, sig_histnames[1] ) ]

        bkg_histnames = [
            'H_bkg_{0}_{1}'.format( self.x_key, self.y_key ),
            'Hsj_bkg_{0}_{1}'.format( self.x_key, self.y_key ) ]

        bkg_draw_strs = [
            'mem_tth_p[{0}]/(mem_tth_p[{0}]+{1}*mem_ttbb_p[{0}])'\
            '>>{2}(100,0.0,1.0)'.format(
                i_hypo, bkg_constant, bkg_histnames[0] ),
            'mem_tth_p[{0}]/(mem_tth_p[{0}]+{1}*mem_ttbb_p[{0}])'\
            '>>{2}(100,0.0,1.0)'.format(
                i_hypo_sj, bkg_constant, bkg_histnames[1] ) ]

        # Final storing of draw strings and histnames
        # Accessible via self.draw_dict['sig' or 'bkg'][0 or 1]
        self.draw_dict = { 'sig' : sig_draw_strs, 'bkg' : bkg_draw_strs }
        self.histnames_dict = { 'sig' : sig_histnames, 'bkg' : bkg_histnames }

        # Only select non-zero results
        # (This is the only selection that differs for non-subjet and subjet results,
        # but it is still the same for sig and bkg)
        self.sel_strs = [
            'mem_tth_p[{0}]+{1}*mem_ttbb_p[{0}]>0'.format(
                i_hypo, bkg_constant ),
            'mem_tth_p[{0}]+{1}*mem_ttbb_p[{0}]>0'.format(
                i_hypo_sj, bkg_constant ),
            ]


    def Print_Object(self):
        print '\n============================='
        print 'Class MEM_Tablecell_Object: '\
              'x_key = {0:10s}, y_key = {1:10s}'.format( self.x_key, self.y_key )

        for key in self.draw_dict:
            print '---------------\nDraw strings: {0}'.format(key)
            for draw_str in self.draw_dict[key]:
                print draw_str

        print '---------------\nSel strings:'
        for i in self.sel_strs: print i


    def Create_MEM_ratio_plots( self, IO_dict ):

        print 'Making mem ratio plots     x_key = {0:10s} y_key = {1:10s}'.format(
            self.x_key, self.y_key )

        input_dir   = IO_dict['input_dir']
        input_path  = IO_dict['input_path']
        output_dir  = IO_dict['output_dir']
        hf          = IO_dict['html_overview_file']
        c1          = IO_dict['root_canvas']

        input_root_fns = { 'sig' : IO_dict['sig_input_root_fn'],
                           'bkg' : IO_dict['bkg_input_root_fn'] }

        for key in input_root_fns:

            input_root_fn = input_root_fns[key]
            input_tree_name = 'tree'

            input_root_file = ROOT.TFile(
                input_path + '/' + input_dir + '/' + input_root_fn )

            input_tree = input_root_file.Get(input_tree_name)

            for sj in [0,1]:

                histname = self.histnames_dict[key][sj]
                draw_str = self.draw_dict[key][sj]
                sel_str = self.sel_strs[sj]

                # Retrieve the histogram
                n_entries = input_tree.Draw( draw_str, sel_str )

                if n_entries > 0:
                    mem_hist = getattr(ROOT, histname ).Clone()
                else:
                    mem_hist = ROOT.TH1F()
                
                mem_hist.SetTitle( '{0}, {3} (def: {1}, sj: {2})'.format(
                    key, self.y_key, self.x_key,
                    'Default' if sj==0 else 'With subjets' ) )

                # Draw again to display title <-- This should be moved to a 
                #                                 separate function at some point
                mem_hist.Draw()

                # Save the histogram to the cell object
                self.mem_hist_dict[key][sj] = copy.deepcopy( mem_hist )

                # Output filename
                im_fn = '{0}/plots/MR_{1}'.format( output_dir, histname )
                html_link_fn = 'plots/MR_{0}'.format(histname)

                # Pdf
                c1.Print( im_fn , 'pdf' )

                # Png
                #print 'Writing {0}.png'.format( im_fn )
                img = ROOT.TImage.Create()
                img.FromPad(c1)
                img.WriteImage('{0}.png'.format( im_fn ) )

                hf.write('<a href="{0}"><img width="300" src="{0}.png"></a>\n'.format(html_link_fn) )

        
    def Create_ROC_Curves(self, IO_dict):

        print 'Making ROC curves          x_key = {0:10s} y_key = {1:10s}'.format(
            self.x_key, self.y_key )

        input_dir   = IO_dict['input_dir']
        input_path  = IO_dict['input_path']
        output_dir  = IO_dict['output_dir']
        hf          = IO_dict['html_overview_file']
        c1          = IO_dict['root_canvas']

        # Get all efficiency lists
        for key in [ 'sig', 'bkg' ]:
            for sj in [ 0 , 1 ]:
                ( self.eff_dict[key][sj], n_points ) = \
                    Get_hist_efficiency( self.mem_hist_dict[key][sj] )

        plottitle = 'Default category:   {0:10s} '\
                    'Subjet category:   {1:10s}'.format( self.y_key, self.x_key )

        # Get filled TGraph object
        ROC = Get_ROC_TGraph( self.eff_dict['sig'][0], self.eff_dict['bkg'][0] )
        ROC.SetTitle( plottitle )
        ROC.SetLineColor(4);
        ROC.SetMarkerColor(4);
        ROC.SetMarkerStyle(22);
        ROC.SetMarkerSize(0.6);
        ROC.GetXaxis().SetTitle( 'sig efficiency' );
        ROC.GetYaxis().SetTitle( '1 - bkg efficiency' );
        ROC.Draw('ALP')

        # Get filled TGraph object
        ROC_sj = Get_ROC_TGraph( self.eff_dict['sig'][1], self.eff_dict['bkg'][1] )
        ROC_sj.SetLineColor(2);
        ROC_sj.SetMarkerColor(2);
        ROC_sj.SetMarkerStyle(23);
        ROC_sj.SetMarkerSize(0.6);
        ROC_sj.Draw('LP')

        # Also draw a straight line
        gr_straight = ROOT.TGraph( 2 )
        gr_straight.SetPoint ( 0, 0.0, 1.0 )
        gr_straight.SetPoint ( 1, 1.0, 0.0 )
        gr_straight.SetLineColor(15)
        gr_straight.Draw('L')

        c1.Update()

        # Adding labels to plot
        # ======================================

        # Set label specifics
        lbl = ROOT.TText()
        lbl.SetNDC()
        lbl.SetTextSize(0.04)
        lbl.SetTextColor(1)

        # Coordinates for the histogram specifics
        anchorx = 0.63
        anchory = 0.85
        nl = 0.05

        # Default, without subjets
        lbl.SetTextColor(4)
        lbl.DrawText( anchorx, anchory, 'Default')
        lbl.SetTextColor(1)
        anchory-=nl

        lbl.DrawText( anchorx, anchory , 'sig entries' )
        lbl.DrawText( anchorx+0.19, anchory , '{0:.0f}'.format(
            self.mem_hist_dict['sig'][0].GetEntries()) )
        anchory-=nl

        lbl.DrawText( anchorx, anchory , 'bkg entries' )
        lbl.DrawText( anchorx+0.19, anchory , '{0:.0f}'.format(
            self.mem_hist_dict['bkg'][0].GetEntries()) )
        anchory-=nl+0.02

        # With subjets
        lbl.SetTextColor(2)
        lbl.DrawText( anchorx, anchory, 'With subjets')
        lbl.SetTextColor(1)
        anchory-=nl

        lbl.DrawText( anchorx, anchory , 'sig entries' )
        lbl.DrawText( anchorx+0.19, anchory , '{0:.0f}'.format(
            self.mem_hist_dict['sig'][1].GetEntries()) )
        anchory-=nl

        lbl.DrawText( anchorx, anchory , 'bkg entries' )
        lbl.DrawText( anchorx+0.19, anchory , '{0:.0f}'.format(
            self.mem_hist_dict['bkg'][1].GetEntries()) )
        anchory-=nl

        c1.Update()

        # IO operations <-- Requires work, code should be streamlined
        # ======================================

        # Output filename

        fn_nopath = 'ROC_{0}_{1}'.format( self.x_key, self.y_key )

        im_fn = output_dir + '/plots/' + fn_nopath
        html_link_fn = 'plots/' + fn_nopath

        # Save html link filename also to class to create the actual table
        self.ROC_html_link = html_link_fn
        self.ROC_tag = fn_nopath

        # Pdf
        c1.Print( im_fn , 'pdf' )

        # Png
        #print 'Writing {0}.png'.format( im_fn )
        img = ROOT.TImage.Create()
        img.FromPad(c1)
        img.WriteImage('{0}.png'.format( im_fn ) )

        # Write html anchor to link to
        hf.write('<a name="{0}"></a>\n'.format(fn_nopath) )
        hf.write('<a href="{0}"><img width="300" src="{0}.png"></a>\n'.format(html_link_fn) )



########################################
# Main
########################################

def main():

    ROOT.gROOT.SetBatch(True)
    ROOT.gROOT.ProcessLine("gErrorIgnoreLevel = 1001;")
    ROOT.gStyle.SetOptFit(1011)

    input_path = '/shome/tklijnsm/Samples/MEMresults/'
    input_dir = 'BMEM_V11_SB_FULL'

    sig_input_root_fn = 'tth_V11_13tev.root'
    bkg_input_root_fn = 'ttjets_V11_13tev.root'

    output_dir = input_dir + '_output'

    # Clean up output directory
    if os.path.isdir( output_dir ):
        shutil.rmtree( output_dir )
    os.makedirs( output_dir + '/plots' )    

    html_overview_fn = 'MEM_overview.html'
    hf = open( output_dir + '/' + html_overview_fn , 'w' )
    hf.write( '<html><body>\n<h1>MEM Ratio plots\n</h1>\n<br>\n<hr />' )

    c1 = ROOT.TCanvas("c1","c1",500,400)
    c1.SetGrid()


    # All IO info contained
    IO_dict = { 'input_path'        : input_path,
                'input_dir'         : input_dir,
                'sig_input_root_fn' : sig_input_root_fn,
                'bkg_input_root_fn' : bkg_input_root_fn,
                'output_dir'        : output_dir,
                'html_overview_file': hf,
                'root_canvas'       : c1,
              }


    ########################################
    # Build matrix of draw strings and selection string
    ########################################

    bkg_constant = 0.12

    hypo = 'testhypo' # Rename this properly
    i_hypo = 0

    hypo_sj = 'testhypo' # Rename this properly
    i_hypo_sj = 2


    # Selection string lists for the horizontal axis
    # ======================================

    sel_dict_x = {}

    sel_dict_x['All'] = [
        ]

    sel_dict_x['No_htt'] = [
        'nhttCandidate_aftercuts<=0',
        ]

    sel_dict_x['htt'] = [
        'nhttCandidate_aftercuts>0',
        ]

    sel_dict_x['0b_matched'] = [
        'nhttCandidate_aftercuts>0',
        'Matching_event_type_number>=1',
        'Matching_event_type_number<=5',
        ]

    sel_dict_x['1b_matched'] = [
        'nhttCandidate_aftercuts>0',
        'Matching_event_type_number>=6',
        'Matching_event_type_number<=8',
        ]

    sel_dict_x['2or3b_matched'] = [
        'nhttCandidate_aftercuts>0',
        'Matching_event_type_number>=9',
        'Matching_event_type_number<=11',
        ]

    # Selection string lists for the vertical axis
    # ======================================

    sel_dict_y = {}

    sel_dict_y['NA'] = [
        'mem_tth_p[{0}]+{2}*mem_ttbb_p[{0}]>0&&'\
            'mem_tth_p[{1}]+{2}*mem_ttbb_p[{1}]==0'.format(
            i_hypo_sj, i_hypo, bkg_constant ),
        ]

    sel_dict_y['Cat1'] = [
        'cat==1',
        ]

    sel_dict_y['Cat2'] = [
        'cat==2',
        ]

    sel_dict_y['Cat3'] = [
        'cat==3',
        ]

    sel_dict_y['Cat123'] = [
        'cat>=1',
        'cat<=3',
        ]

    sel_dict_y['AllCat'] = [
        ]

    # To keep order consistent and easily turn categories on or off

    x_key_list = [ 'All', 'No_htt', 'htt',
                   '0b_matched', '1b_matched', '2or3b_matched' ]
    y_key_list = [ 'NA', 'Cat1', 'Cat2', 'Cat3', 'Cat123', 'AllCat' ]

    #x_key_list = [ 'No_htt', 'htt' ]
    #y_key_list = [ 'Cat1', 'AllCat' ]


    ########################################
    # Fill the mem table and create figures
    ########################################

    # Initialize MEM_Table
    MEM_Table = {}
    for x_key in x_key_list:
        MEM_Table[x_key] = {}
        for y_key in y_key_list:
            # Initialize a cell
            MEM_Table[x_key][y_key] = MEM_Tablecell_Object(x_key,y_key)
            # Set 'cell' as the current cell for easy reference
            cell = MEM_Table[x_key][y_key]

            # Sets the draw strings and the unique selection strings
            cell.Set_draw_strs( i_hypo, i_hypo_sj, bkg_constant )

            # Initialize list of selection strings
            sel_list = []

            # Load the selection strings from both axes into it
            sel_list.extend( sel_dict_x[x_key] )
            sel_list.extend( sel_dict_y[y_key] )

            # Build the actual selection string
            full_sel_str = ''
            for sel_str in sel_list:
                full_sel_str += sel_str
                # If not the last element, add '&&'
                if sel_str != sel_list[-1]:
                    full_sel_str += '&&'

            # Add the full selection string to the selection strings in the class
            if full_sel_str != '':
                cell.sel_strs[0] += '&&' + full_sel_str
                cell.sel_strs[1] += '&&' + full_sel_str

            cell.Create_MEM_ratio_plots( IO_dict )
            cell.Create_ROC_Curves( IO_dict )

            hf.write('<br>\n')
    hf.close()
    
    # Create the actual table html file
    hf = open( '{0}/MEM_Table.html'.format( output_dir ) , 'w' )
    hf.write( '<html><body>\n<h1>MEM Table\n</h1>\n<br>\n<hr />' )
    
    for y_key in y_key_list:
        for x_key in x_key_list:
            # Set 'cell' as the current cell for easy reference
            cell = MEM_Table[x_key][y_key]

            hf.write('<a href="{0}"><img width="250" src="{1}.png"></a>\n'.format(
                html_overview_fn + '#' + cell.ROC_tag,
                cell.ROC_html_link ) )
        hf.write('<br>\n')


########################################
# End of Main
########################################
if __name__ == "__main__":
    main()
