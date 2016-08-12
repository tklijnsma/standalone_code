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
import pickle

from MEM_Table_config import MEM_Table_configuration

hist_counter = 0

########################################
# Functions
########################################

def Get_hist_efficiency( hist ):

    n_bins = hist.GetSize() - 2 # Subtract for underflow and overflow bins
    n_entries = hist.Integral()

    #print n_entries

    if n_entries == 0:
        return [ 0.0, 1.0 ]

    # Create list of values between 0.0 and 1.0
    N = n_bins - 1 # -1 to be sure all points are in there
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

    for i_bin in range(n_bins-1,-1,-1):
        
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
        

def Get_sel_list( sel_key, sel_dict ):

    all_keys = sel_key.split('&&')

    sel_list = []
    for key in all_keys:
        sel_list.extend( sel_dict[key] )

    return sel_list



########################################
# Classes
########################################

class MEM_Tablecell_Object():

    def __init__( self, x_key, y_key, config ):

        self.x_key = x_key
        self.y_key = y_key
        self.config = config

        self.draw_dict      = {}
        self.mem_hist_dict  = {}
        self.histnames_dict = {}
        self.sel_strs       = {}

        self.ROC_TGraphs_dict = {}
        self.MEM_html_link_dict = {}


    def Set_draw_strs( self, hypo, i_hypo, bkg_constant ):

        global hist_counter

        self.histnames_dict[hypo] = {}
        self.draw_dict[hypo] = {}

        for key in [ 'sig', 'bkg' ]:

            """
            # Dictionary of histogram names
            self.histnames_dict[hypo][key] = \
                '{0}_{1}_{2}_{3}'.format(
                    hypo,
                    key,
                    self.x_key,
                    self.y_key,
                    )
            """
            # Dictionary of histogram names
            self.histnames_dict[hypo][key] = str(hist_counter)
            hist_counter += 1


            # Dictionary of draw strings per histogram
            self.draw_dict[hypo][key] = \
                'mem_tth_p[{0}]/(mem_tth_p[{0}]+{1}*mem_ttbb_p[{0}])' \
                '>>{2}({3},0.0,1.0)'.format(
                    i_hypo,
                    bkg_constant,
                    self.histnames_dict[hypo][key],
                    self.config.n_mem_hist_bins
                    )

        #self.sel_strs[hypo] = 'mem_tth_p[{0}]+{1}*mem_ttbb_p[{0}]>0'.format(
        #                            i_hypo, bkg_constant )


    def Set_sel_strs_per_hypo( self, config ):

        # Only select non-zero results
        # (This is the only selection that differs per hypothesis,
        # but it is still the same for sig and bkg)

        self.sel_strs = copy.deepcopy(config.sel_dict_per_hypo)




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


    def Create_MEM_ratio_hists( self, hypo, IO_dict ):

        # Convenient references
        input_dir   = IO_dict['input_dir']
        input_path  = IO_dict['input_path']
        output_dir  = IO_dict['output_dir']
        c1          = IO_dict['MEM_canvas']

        input_root_fns = { 'sig' : IO_dict['sig_input_root_fn'],
                           'bkg' : IO_dict['bkg_input_root_fn'] }

        # Open up spots to write histograms to
        self.mem_hist_dict[hypo] =  { 'sig' : 0, 'bkg' : 0 }
        self.MEM_html_link_dict[hypo] = { 'sig' : '', 'bkg' : '' }


        for key in [ 'sig', 'bkg' ]:

            input_root_file = ROOT.TFile(
                input_path + '/' + input_dir + '/' + input_root_fns[key] )
            input_tree = input_root_file.Get('tree')

            histname = self.histnames_dict[hypo][key]
            draw_str = self.draw_dict[hypo][key]
            sel_str = self.sel_strs[hypo]


            if hasattr(self.config, 'UseGenWeights') and self.config.UseGenWeights:
                sel_str = 'genWeight*(' + sel_str + ')'

            if ( hasattr(self.config, 'UsePhysical') and
                 self.config.UsePhysical ):


                # Get sum of weights of histogram

                if key == 'bkg':
                    n_weight_pos = input_tree.Draw( 'genWeight',
                                                     sel_str + '&&genWeight>0' )

                    n_weight_neg = input_tree.Draw( 'genWeight',
                                                     sel_str + '&&genWeight<0' )

                    sum_weights = ( n_weight_pos - n_weight_neg ) * 6384.0

                if key == 'sig':
                    sum_weights = input_tree.Draw( 'genWeight', sel_str )

                try:
                    weight_factor = ( ( self.config.sigma_p[key] *
                                        self.config.target_lumi ) /
                                      ( self.config.total_count[key] *
                                        self.config.genWeight_norm[key] )
                                    )

                except ZeroDivisionError:
                    weight_factor = 0.0


                #print '        sum_weights = {0}   weight_factor = {1}'.format(
                #    sum_weights, weight_factor )

                sel_str = 'genWeight*{0}*({1})'.format( weight_factor, sel_str )


            # Retrieve the histogram
            n_entries = input_tree.Draw( draw_str, sel_str )

            if n_entries > 0:
                mem_hist = getattr(ROOT, histname ).Clone()
            else:
                mem_hist = ROOT.TH1F()
            
            mem_hist.SetTitle( '{0}_{1}'.format( hypo, key ) )

            # Save the histogram to the cell object
            self.mem_hist_dict[hypo][key] = copy.deepcopy( mem_hist )

            # Avoid memory overload
            input_root_file.Close()

        
    def Create_ROC_TGraphs(self, hypo, IO_dict ):

        input_dir   = IO_dict['input_dir']
        input_path  = IO_dict['input_path']
        output_dir  = IO_dict['output_dir']
        c1          = IO_dict['ROC_canvas']

        # Initialize dicts
        eff_dict = { 'sig' : [] , 'bkg' : [] }
        self.ROC_TGraphs_dict[hypo] = {}

        # Get efficiency lists
        for key in [ 'sig', 'bkg' ]:
            eff_dict[key] = Get_hist_efficiency( self.mem_hist_dict[hypo][key] )

        # Get filled TGraph object
        ROC = Get_ROC_TGraph( eff_dict['sig'], eff_dict['bkg'] )

        plottitle = '{0}\nSelecting {1} AND {2}'.format( hypo,
                                                         self.y_key, self.x_key )

        ROC.SetTitle( plottitle )
        ROC.SetMarkerStyle(22);
        ROC.SetMarkerSize(0.6);

        # Store TGraph object in class
        self.ROC_TGraphs_dict[hypo] = ROC


    def Create_MEM_ratio_Image( self, hypo_list, IO_dict ):

        # Convenient references
        input_dir   = IO_dict['input_dir']
        input_path  = IO_dict['input_path']
        output_dir  = IO_dict['output_dir']
        c1          = IO_dict['MEM_canvas']
        c1.cd()

        empty_hist = ROOT.TH1F()

        # Set label specifics
        lbl = ROOT.TText()
        lbl.SetNDC()
        lbl.SetTextSize(0.04)

        for key in [ 'sig', 'bkg' ]:

            # Draw empty histogram (keeps axes and grid this way)
            empty_hist.Draw()
            c1.Update()
            LineColor_counter = 1

            # Starting coordinates and variabeles for labels
            anchorx  = 0.74
            anchory  = 0.85
            endl     = 0.05
            big_endl = 0.07
            anchorx_shift = 0.15

            # To be overridden by the maximum of the highest histogram
            y_axis_max = 0.0
            y_axis_min = 0.0

            for hypo in hypo_list:

                histname = self.histnames_dict[hypo][key]
                mem_hist = self.mem_hist_dict[hypo][key]

                # Find maximum in all histograms
                mem_hist_max = mem_hist.GetMaximum()
                if mem_hist_max > y_axis_max: y_axis_max = mem_hist_max

                mem_hist_min = mem_hist.GetMinimum()
                if mem_hist_min < y_axis_min: y_axis_min = mem_hist_min

                LineColor_counter += 1

                # I don't like colors 3 and 5
                if LineColor_counter == 3: LineColor_counter += 1
                if LineColor_counter == 5: LineColor_counter += 1

                mem_hist.SetLineColor(LineColor_counter)
                mem_hist.Draw('HISTSAME')


                # Adding labels to plot
                # ======================================

                lbl.SetTextColor(LineColor_counter)
                lbl.DrawText( anchorx, anchory, hypo )
                anchory -= endl

                lbl.SetTextColor(1)
                lbl.DrawText( anchorx, anchory , 'sig entries' )
                lbl.DrawText(
                    anchorx+anchorx_shift,
                    anchory,
                    '{0:.4f}'.format( self.mem_hist_dict[hypo]['sig'].Integral()) )
                anchory -= endl

                lbl.DrawText( anchorx, anchory , 'bkg entries' )
                lbl.DrawText(
                    anchorx+anchorx_shift,
                    anchory,
                    '{0:.4f}'.format( self.mem_hist_dict[hypo]['bkg'].Integral()) )
                anchory -= big_endl


            empty_hist.SetMinimum(y_axis_min)
            empty_hist.SetMaximum(y_axis_max*1.1)
            c1.Update()

            # IO operations
            # ======================================

            fn = 'MR_{0}_{1}_{2}'.format( key, self.x_key, self.y_key )
            fn_output = '{0}/plots/{1}'.format( output_dir, fn )

            self.MEM_html_link_dict[key] = 'plots/{0}'.format(fn)

            # Pdf
            c1.Print( fn_output , 'pdf' )

            # Png
            img = ROOT.TImage.Create()
            img.FromPad(c1)
            img.WriteImage('{0}.png'.format( fn_output ) )
    

    def Create_ROC_Image( self, hypo_list, IO_dict ):

        c1 = IO_dict['ROC_canvas']
        c1.cd()

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

        c1.Update()

        # Starting coordinates and variabeles for labels
        anchorx  = 0.7
        anchory  = 0.85
        endl     = 0.05
        big_endl = 0.07
        anchorx_shift = 0.19

        # Set label specifics
        lbl = ROOT.TText()
        lbl.SetNDC()
        lbl.SetTextSize(0.04)

        LineColor_counter = 1

        for hypo in hypo_list:

            LineColor_counter += 1

            if LineColor_counter == 3: LineColor_counter += 1
            if LineColor_counter == 5: LineColor_counter += 1

            ROC = self.ROC_TGraphs_dict[hypo]
            ROC.SetMarkerColor(LineColor_counter);
            ROC.SetMarkerSize(0.5);
            ROC.SetLineColor(LineColor_counter);

            if not ROC.GetN() == 2:
                ROC.Draw('LP')

            # Adding labels to plot
            # ======================================

            lbl.SetTextColor(LineColor_counter)
            lbl.DrawText( anchorx, anchory, hypo )
            anchory -= endl

            lbl.SetTextColor(1)
            lbl.DrawText( anchorx, anchory , 'sig entries' )
            lbl.DrawText(
                anchorx+anchorx_shift,
                anchory,
                '{0:.0f}'.format( self.mem_hist_dict[hypo]['sig'].GetEntries()) )
            anchory -= endl

            lbl.DrawText( anchorx, anchory , 'bkg entries' )
            lbl.DrawText(
                anchorx+anchorx_shift,
                anchory,
                '{0:.0f}'.format( self.mem_hist_dict[hypo]['bkg'].GetEntries()) )
            anchory -= big_endl

            c1.Update()

            # IO operations
            # ======================================

            fn = 'ROC_{0}_{1}'.format( self.x_key, self.y_key )
            fn_output = IO_dict['output_dir'] + '/plots/' + fn

            # Save html link filename also to class to create the actual table
            self.ROC_html_link   = 'plots/' + fn
            self.ROC_html_anchor = fn

            # Pdf
            c1.Print( fn_output , 'pdf' )

            # Png
            img = ROOT.TImage.Create()
            img.FromPad( c1 )
            img.WriteImage('{0}.png'.format( fn_output ) )



########################################
# Main
########################################

def main_MEM_Table( config = False ):

    ########################################
    # Read configuration
    ########################################

    if not config:
        config = MEM_Table_configuration()

    input_dir = config.input_dir
    output_dir = config.output_dir
    hypo_dict = config.hypo_dict
    bkg_constant = config.bkg_constant
    sel_list_for_all = config.sel_list_for_all
    x_key_list = config.x_key_list
    y_key_list = config.y_key_list

    sel_dict = config.sel_dict

    #compare_dict = config.compare_dict
    hypo_list = config.hypo_list

    ########################################
    # Set up for loop
    ########################################

    ROOT.gROOT.Reset()
    ROOT.gROOT.SetBatch(True)
    ROOT.gROOT.ProcessLine("gErrorIgnoreLevel = 1001;")

    ROOT.gStyle.SetOptFit(1011)
    ROOT.gStyle.SetOptStat(0)

    ROOT.TH1.SetDefaultSumw2(True)

    if not hasattr( config, 'input_path' ):
        input_path = '/shome/tklijnsm/Samples/MEMresults/'
    else:
        input_path = config.input_path

    # Actual root file names
    if hasattr( config, 'sig_input_root_fn' ):
        sig_input_root_fn = config.sig_input_root_fn
    else:
        sig_input_root_fn = 'tth_V11_13tev.root'
    if hasattr( config, 'bkg_input_root_fn' ):
        bkg_input_root_fn = config.bkg_input_root_fn
    else:
        bkg_input_root_fn = 'ttjets_V11_13tev.root'

    # Clean up output directory (only if plots will be drawn)
    if config.Draw_plots:
        if os.path.isdir( output_dir ):
            shutil.rmtree( output_dir )
        os.makedirs( output_dir + '/plots' )
        os.makedirs( output_dir + '/used_pys' )

    # Copy MEM_Table_config.py to the outputdir (easily repeatable that way)
    shutil.copyfile('MEM_Table_config.py',
                    output_dir + '/used_pys/MEM_Table_config.py' )
    shutil.copyfile('Make_MEM_Table.py',
                    output_dir + '/used_pys/Make_MEM_Table.py' )

    # Set up ROC canvas
    c2 = ROOT.TCanvas("c2","c2",600,400)
    c2.SetGrid()
    c2.SetRightMargin(0.32)

    # Set up MEM ratio canvas TODO: log scale
    c1 = ROOT.TCanvas("c1","c1",700,400)
    c1.SetGrid()
    c1.SetRightMargin(0.28)
    #c1.SetLogy()

    # All IO info contained
    IO_dict = { 'input_path'            : input_path,
                'input_dir'             : input_dir,
                'sig_input_root_fn'     : sig_input_root_fn,
                'bkg_input_root_fn'     : bkg_input_root_fn,
                'output_dir'            : output_dir,
                'MEM_canvas'            : c1,
                'ROC_canvas'            : c2,
              }

    # Initialize MEM_Table
    MEM_Table = {}
    for x_key in x_key_list:
        MEM_Table[x_key] = {}
        for y_key in y_key_list:
            # Initialize a cell
            MEM_Table[x_key][y_key] = MEM_Tablecell_Object(x_key,y_key,config)


    ########################################
    # Loop over the hypothesis-comparisons
    ########################################

    for hypo in hypo_list:

        # Get corresponding list index in ROOT MEM branch
        i_hypo = hypo_dict[hypo]

        print '\nRunning hypothesis {0}'.format(hypo)


        ########################################
        # Fill the mem table and create figures
        ########################################

        print '    Creating MEM Ratio histograms and ROC TGraphs'

        for x_key in x_key_list:
            for y_key in y_key_list:

                print '        x_key = {0:15s} y_key = {1:15s}'.format(
                    x_key, y_key )

                # Set 'cell' as the current cell for easy reference
                cell = MEM_Table[x_key][y_key]

                # Sets the draw strings and the unique selection strings
                cell.Set_draw_strs( hypo, i_hypo, bkg_constant )
                cell.Set_sel_strs_per_hypo( config )

                # Initialize list of selection strings
                sel_list = []

                # Load the selection strings from both axes into it
                sel_list.extend( Get_sel_list( x_key, sel_dict ) )
                sel_list.extend( Get_sel_list( y_key, sel_dict ) )
                sel_list.extend( sel_list_for_all )

                # Build the actual selection string
                full_sel_str = '&&'.join( sel_list )

                # Add the full selection string to the selection strings in the class
                if full_sel_str != '':
                    if cell.sel_strs[hypo] != '':
                        cell.sel_strs[hypo] += '&&'
                    cell.sel_strs[hypo] += full_sel_str

                cell.Create_MEM_ratio_hists( hypo, IO_dict )

                cell.Create_ROC_TGraphs( hypo, IO_dict )


    if config.Draw_plots:

        # Draw the ROC after the loop (includes all comparisons)

        print '\nDrawing all MEM ratio plots'
        for x_key in x_key_list:
            for y_key in y_key_list:
                MEM_Table[x_key][y_key].Create_MEM_ratio_Image( hypo_list, IO_dict )

        print 'Drawing all ROC plots'
        for x_key in x_key_list:
            for y_key in y_key_list:
                MEM_Table[x_key][y_key].Create_ROC_Image( hypo_list, IO_dict )


        ########################################
        # Creating the html-files
        ########################################

        print 'Creating html files'

        # Create the overview html-files
        hf_overview = open( output_dir + '/' + 'MEM_overview.html' , 'w' )
        hf_overview.write( '<html><body>\n<h1>MEM Ratio plots\n</h1>\n<br>\n<hr />' )
        hf_overview.write( '\n<h2>Signal ---------- Background ---------- ROC\n</h2>\n<br>\n' )

        # Create the table html file
        hf_table = open( '{0}/MEM_Table.html'.format( output_dir ) , 'w' )
        hf_table.write( '<html><body>\n<h1>MEM Table\n</h1>\n<br>\n<hr />' )

        # Fill the overview html files
        for x_key in x_key_list:
            for y_key in y_key_list:
                # Set 'cell' as the current cell for easy reference
                cell = MEM_Table[x_key][y_key]

                for key in [ 'sig', 'bkg' ]:
                    hf_overview.write(
                        '<a href="{0}"><img width="450" src="{0}.png"></a>\n'.format(
                            cell.MEM_html_link_dict[key]) )

                # Write the ROC curve plus html anchor to overview
                hf_overview.write('<a name="{0}"></a>\n'.format(cell.ROC_html_anchor) )
                hf_overview.write('<a href="{0}"><img width="400" src="{0}.png">' \
                                  '</a>\n'.format(cell.ROC_html_link) )
                hf_overview.write('<br>\n')


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

        if hasattr(config, 'Store_table_as_picke') and config.Store_table_as_picke:
            print 'Writing MEM Table to pickle file'
            f_pickle = open( output_dir + '/MEM_Table.pickle', 'wb' )
            pickle.dump( MEM_Table, f_pickle )
            f_pickle.close()

        
########################################
# End of Main
########################################
if __name__ == "__main__":
    main_MEM_Table()
