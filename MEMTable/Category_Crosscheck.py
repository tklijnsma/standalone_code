#!/usr/bin/env python
"""
Thomas:

"""

########################################
# Imports
########################################

import os
import shutil
import copy
import sys
import ROOT



########################################
# Classes
########################################

class Cat_Tablecell_Object():

    def __init__( self, x_key, y_key ):

        self.x_key = x_key
        self.y_key = y_key

        self.sel_str = ''

        self.N = { 'sig' : 0 , 'bkg' : 0 }


    def Count_for_selstr( self, IO_dict ):

        for key in [ 'sig', 'bkg' ]:
            input_root_file = ROOT.TFile(
                IO_dict['input_path'] + '/' + 
                IO_dict['input_dir'] + '/' +
                IO_dict['input_root_fns'][key] )

            input_tree = input_root_file.Get('tree')

            self.N[key] = input_tree.Draw( 'run>>h', self.sel_str )

        


########################################
# Main
########################################

def main():


    ROOT.gROOT.SetBatch(True)
    ROOT.gROOT.ProcessLine("gErrorIgnoreLevel = 1001;")
    ROOT.gStyle.SetOptFit(1011)

    IO_dict = {

        'input_path' : '/shome/tklijnsm/Samples/MEMresults/',
        'input_dir' : 'BMEM_V11_SB_FULL_njetsbranches_S5changed',

        'sig_input_root_fn' : 'tth_V11_13tev.root',
        'bkg_input_root_fn' : 'ttjets_V11_13tev.root',

        'input_root_fns' : { 'sig' : 'tth_V11_13tev.root',
                             'bkg' : 'ttjets_V11_13tev.root' },

        }        


    ########################################
    # Build matrix of draw strings and selection string
    ########################################

    # Selection string lists for the horizontal axis
    # ======================================

    sel_dict_x = {}

    sel_dict_x['1lep_4b_>=2l'] = [
        'nleps==1',
        'n_bjets>=4',
        'n_ljets>=2',
        'cat_btag==1',
        ]

    sel_dict_x['1lep_4b_>=1l'] = [
        'nleps==1',
        'n_bjets>=4',
        'n_ljets>=1',
        'cat_btag==1',
        ]

    sel_dict_x['1lep_4b_>=2l_sj'] = [
        'nleps==1',
        'n_bjets_sj>=4',
        'n_ljets_sj>=2',
        ]

    sel_dict_x['1lep_4b_>=1l_sj'] = [
        'nleps==1',
        'n_bjets_sj>=4',
        'n_ljets_sj>=1',
        ]

    sel_dict_x['All'] = [
        'nhttCandidate_aftercuts>0',
        ]


    # Selection string lists for the vertical axis
    # ======================================

    sel_dict_y = {}

    sel_dict_y['NOCAT'] = [
        'nhttCandidate_aftercuts>0',
        'cat==-1',
        ]

    sel_dict_y['Cat1'] = [
        'nhttCandidate_aftercuts>0',
        'cat==1',
        ]

    sel_dict_y['Cat2'] = [
        'nhttCandidate_aftercuts>0',
        'cat==2',
        ]

    sel_dict_y['Cat3'] = [
        'nhttCandidate_aftercuts>0',
        'cat==3',
        ]

    sel_dict_y['Cat123'] = [
        'nhttCandidate_aftercuts>0',
        'cat>=1',
        'cat<=3',
        ]

    sel_dict_y['All'] = [
        'nhttCandidate_aftercuts>0',
        #'cat_btag==1',
        ]

    # To keep order consistent and easily turn categories on or off

    #x_key_list = [ '1lep_4b_>=2l', '1lep_4b_>=1l' ]
    #x_key_list = [ '1lep_4b_>=2l_sj', '1lep_4b_>=1l_sj' ]
    x_key_list = [ '1lep_4b_>=2l', '1lep_4b_>=1l', '1lep_4b_>=2l_sj', '1lep_4b_>=1l_sj' ]
    y_key_list = [ 'Cat1', 'Cat2', 'Cat3', 'All', 'NOCAT' ]


    
    ########################################
    # Fill category table
    ########################################

    # Initialize Cat_Table
    Cat_Table = {}
    for x_key in x_key_list:
        Cat_Table[x_key] = {}
        for y_key in y_key_list:
            # Initialize a cell
            Cat_Table[x_key][y_key] = Cat_Tablecell_Object(x_key,y_key)
            # Set 'cell' as the current cell for easy reference
            cell = Cat_Table[x_key][y_key]
            
            # Initialize list of selection strings
            sel_list = []

            # Load the selection strings from both axes into it
            sel_list.extend( sel_dict_x[x_key] )
            sel_list.extend( sel_dict_y[y_key] )

            # Build the actual selection string
            full_sel_str = "&&".join( sel_list )

            # Add the full selection string to the selection strings in the class
            if full_sel_str != '':
                cell.sel_str += full_sel_str

            #print 'x_key = {0:10s} y_key = {1:10s}'.format( x_key, y_key )
            #print '    cell.sel_str = {0}'.format( cell.sel_str )


    for x_key in x_key_list:
        for y_key in y_key_list:
            Cat_Table[x_key][y_key].Count_for_selstr( IO_dict )


    for key in ['sig', 'bkg']:

        print '\nCategory crosscheck for {0}'.format(key)

        # Print line with all x_keys:
        sys.stdout.write( '\n          |' )
        for x_key in x_key_list:
            x_key_str = '{0:16s}|'.format(x_key)
            sys.stdout.write(x_key_str)

        for y_key in y_key_list:
            sys.stdout.write( '\n{0:10s}|'.format(y_key) )
            for x_key in x_key_list:

                n = Cat_Table[x_key][y_key].N[key]

                n_str = '{0:16s}|'.format( str(n) )
                sys.stdout.write(n_str)

        print ''




########################################
# End of Main
########################################
if __name__ == "__main__":
    main()
