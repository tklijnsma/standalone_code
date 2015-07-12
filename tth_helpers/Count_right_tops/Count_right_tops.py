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
# Main
########################################

def main():


    ROOT.gROOT.SetBatch(True)
    ROOT.gROOT.ProcessLine("gErrorIgnoreLevel = 1001;")
    ROOT.gStyle.SetOptFit(1011)

    IO_dict = {

        'input_path' : '/shome/tklijnsm/Samples/NoMEM/V12_righttoptest',
        #'input_dir' : 'highest_delR_lepton',

        'sig' : 'tth_V12_13tev.root',
        'bkg' : 'ttjets_V12_13tev.root',

        }        

    sel_str_dict = {

        'right_top_h'  : 'QMatching_sj_hadr_bquark==1&&QMatching_sj_ot_hadr_bquark==0',
        'wrong_top_h'  : 'QMatching_sj_hadr_bquark==0&&QMatching_sj_ot_hadr_bquark==1',
        'both_wrong_h' : 'QMatching_sj_hadr_bquark==0&&QMatching_sj_ot_hadr_bquark==0',
        'both_right_h' : 'QMatching_sj_hadr_bquark==1&&QMatching_sj_ot_hadr_bquark==1',

        #'right_top_l'  : 'QMatching_sj_lept_bquark==1&&QMatching_sj_ot_lept_bquark==0',
        #'wrong_top_l'  : 'QMatching_sj_lept_bquark==0&&QMatching_sj_ot_lept_bquark==1',
        #'both_wrong_l' : 'QMatching_sj_lept_bquark==0&&QMatching_sj_ot_lept_bquark==0',
        #'both_right_l' : 'QMatching_sj_lept_bquark==1&&QMatching_sj_ot_lept_bquark==1',

        }

    sel_keys = [ 
        'right_top_h',
        'wrong_top_h',
        'both_wrong_h',
        'both_right_h',
        #'right_top_l',
        #'wrong_top_l',
        #'both_wrong_l',
        #'both_right_l',
        ]


    input_dirs = [
        'highest_delR_lepton',
        'lowest_fRec',
        'lowest_n_subjetiness',
        ]

    count_dict = {}


    for input_dir in input_dirs:

        count_dict[input_dir] = {}

        for key in [ 'sig', 'bkg' ]:

            count_dict[input_dir][key] = {}

            input_root_file = ROOT.TFile(
                IO_dict['input_path'] + '/' + 
                input_dir + '/' +
                IO_dict[key] )
            input_tree = input_root_file.Get('tree')

            for sel_key in sel_str_dict:
                sel_str = sel_str_dict[sel_key]
                count_dict[input_dir][key][sel_key] = input_tree.Draw( 'run', 
                                                                       sel_str )

            # Calculate percentages

            total_count = 0.0
            for sel_key in sel_str_dict:
                total_count += count_dict[input_dir][key][sel_key]

            for sel_key in sel_str_dict:
                count_dict[input_dir][key][sel_key + '_perc'] = \
                    float(count_dict[input_dir][key][sel_key]) / total_count * 100


    f_out = open( 'Output_counted_files', 'w' )
    f_out.write( 'Matching counts for subjet to hadronic b-quark\n\n' )

    for input_dir in input_dirs:

        f_out.write( input_dir + ':\n' )

        for key in [ 'sig', 'bkg' ]:
            f_out.write( '  {0}:\n'.format(key) )
            for sel_key in sel_keys:
                f_out.write( '    {0:11s}: {1:6s} ({2:.2f}%)\n'.format(
                    sel_key,
                    str(count_dict[input_dir][key][sel_key]),
                    count_dict[input_dir][key][sel_key + '_perc'],
                    ))

        f_out.write('===========================\n')
            
            





########################################
# End of Main
########################################
if __name__ == "__main__":
    main()
