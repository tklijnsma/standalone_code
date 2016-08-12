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

from rocdraw_new import roc_main


########################################
# Class
########################################

class ROC_configuration:
    def __init__( self, name, input_dir, output_dir ):

        self.name = name
        self.input_dir = 'input_pickles/' + input_dir
        self.output_dir = 'output_plots/' + output_dir

        # Default configuration
        self.hypo_list = [
            ( '#1', 'All', 'All', 'SL_2qW_NewTF' ),
            ( '#2', 'All', 'All', 'SL_2qW_sj_NewTF' ),
            ( '#3', 'All', 'All', 'SL_2qW_sj_perm_NewTF' ),
            ]

        self.hypo_prints = {
            '#1'    : 'Default',
            '#2'    : 'Default (changed)',
            '#3'    : 'With subjets',
            '#4'    : 'With subjets (changed)',
            '#7'    : 'Perm. fixed (changed)',
            }

        self.hypo_colors = {
            '#1'    : 2,
            '#2'    : 28,
            '#3'    : 4,
            '#4'    : 8,
            '#7'    : 42,
            }






########################################
# Main
########################################

def main():

    ########################################
    # Approach 1
    ########################################

    #( '#7', 'All', 'All', 'SL_2qW_sj_perm_NewTF' ),

    # ======================================
    Unrestr_All = ROC_configuration( 'AP1_All', 'Unrestructured', 'AP1' )
    Unrestr_All.hypo_list = [
        ( '#1', 'All', 'All', 'SL_2qW_NewTF' ),
        ( '#2', 'pass_2qW_def', 'All', 'SL_2qW_NewTF' ),
        ( '#3', 'All', 'All', 'SL_2qW_sj_NewTF' ),
        ( '#4', 'pass_2qW_def', 'All', 'SL_2qW_sj_NewTF' ),
        ]

    # ======================================
    Unrestr_1b  = ROC_configuration( 'AP1_1b', 'Unrestructured', 'AP1' )
    Unrestr_1b.hypo_list = [
        ( '#1', 'All', 'ETN7', 'SL_2qW_NewTF' ),
        #( '#2', 'pass_2qW_def', 'ETN7', 'SL_2qW_NewTF' ),
        ( '#3', 'All', 'ETN7', 'SL_2qW_sj_NewTF' ),
        ( '#4', 'pass_2qW_def', 'ETN7', 'SL_2qW_sj_NewTF' ),
        ]

    # ======================================
    Unrestr_2b  = ROC_configuration( 'AP1_2b', 'Unrestructured', 'AP1' )
    Unrestr_2b.hypo_list = [
        ( '#1', 'All', 'ETN9', 'SL_2qW_NewTF' ),
        #( '#2', 'pass_2qW_def', 'ETN9', 'SL_2qW_NewTF' ),
        ( '#3', 'All', 'ETN9', 'SL_2qW_sj_NewTF' ),
        #( '#4', 'pass_2qW_def', 'ETN9', 'SL_2qW_sj_NewTF' ),
        ]
    
    # ======================================
    Unrestr_0b  = ROC_configuration( 'AP1_0b', 'Unrestructured', 'AP1' )
    Unrestr_0b.hypo_list = [
        #( '#1', 'nonpass_2qW_def', 'ETN16', 'SL_2qW_NewTF' ),
        #( '#1', 'nonpass_2qW_def', 'ETN16', 'SL_2qW_NewTF' ),
        ( '#3', 'nonpass_2qW_def', 'ETN16', 'SL_2qW_sj_NewTF' ),
        #( '#3', 'nonpass_2qW_def', 'ETN16', 'SL_2qW_sj_NewTF' ),
        ]
    Unrestr_0b.hypo_prints['#3'] = 'With subjets (added)'


    # ======================================
    Unrestr_perm  = ROC_configuration( 'AP1_perm', 'Unr_ETN17', 'AP1' )
    Unrestr_perm.hypo_list = [
        ( '#1', 'All', 'ETN17', 'SL_2qW_NewTF' ),
        #( '#2', 'pass_2qW_def', 'ETN9', 'SL_2qW_NewTF' ),
        ( '#4', 'pass_2qW_def', 'ETN17', 'SL_2qW_sj_NewTF' ),
        #( '#4', 'pass_2qW_def', 'ETN9', 'SL_2qW_sj_NewTF' ),
        ( '#7', 'pass_2qW_def', 'ETN17', 'SL_2qW_sj_perm_NewTF' ),
        ]



    ########################################
    # Approach 2
    ########################################

    ### No cuts

    # ======================================
    nocut_All = ROC_configuration( 'nocut_All', 'nocut', 'nocut' )
    nocut_All.hypo_list = [
        ( '#1', 'All', 'All', 'SL_2qW_NewTF' ),
        ( '#3', 'All', 'All', 'SL_2qW_sj_NewTF' ),
        ( '#4', 'pass_2qW_def', 'All', 'SL_2qW_sj_NewTF' ),
        ]

    # ======================================
    nocut_1b = ROC_configuration( 'nocut_1b', 'nocut', 'nocut' )
    nocut_1b.hypo_list = [
        ( '#1', 'All', '1excluded', 'SL_2qW_NewTF' ),
        ( '#3', 'All', '1excluded', 'SL_2qW_sj_NewTF' ),
        ( '#4', 'pass_2qW_def', '1excluded', 'SL_2qW_sj_NewTF' ),
        ]

    # ======================================
    nocut_2b = ROC_configuration( 'nocut_2b', 'nocut', 'nocut' )
    nocut_2b.hypo_list = [
        ( '#1', 'All', '23excluded', 'SL_2qW_NewTF' ),
        ( '#3', 'All', '23excluded', 'SL_2qW_sj_NewTF' ),
        ]

    # ======================================
    nocut_0b = ROC_configuration( 'nocut_0b', 'nocut', 'nocut' )
    nocut_0b.hypo_list = [
        ( '#3', 'nonpass_2qW_def', '0excluded', 'SL_2qW_sj_NewTF' ),
        ]
    nocut_0b.hypo_prints['#3'] = 'With subjets (added)'

    ### WP3

    # ======================================
    WP3_All = ROC_configuration( 'WP3_All', 'WP3', 'WP3' )
    WP3_All.hypo_list = [
        ( '#1', 'All', 'All', 'SL_2qW_NewTF' ),
        ( '#3', 'All', 'All', 'SL_2qW_sj_NewTF' ),
        ( '#4', 'pass_2qW_def', 'All', 'SL_2qW_sj_NewTF' ),
        ]

    # ======================================
    WP3_1b = ROC_configuration( 'WP3_1b', 'WP3', 'WP3' )
    WP3_1b.hypo_list = [
        ( '#1', 'All', '1excluded', 'SL_2qW_NewTF' ),
        ( '#3', 'All', '1excluded', 'SL_2qW_sj_NewTF' ),
        ( '#4', 'pass_2qW_def', '1excluded', 'SL_2qW_sj_NewTF' ),
        ]

    # ======================================
    WP3_2b = ROC_configuration( 'WP3_2b', 'WP3', 'WP3' )
    WP3_2b.hypo_list = [
        ( '#1', 'All', '23excluded', 'SL_2qW_NewTF' ),
        ( '#3', 'All', '23excluded', 'SL_2qW_sj_NewTF' ),
        ]

    # ======================================
    WP3_0b = ROC_configuration( 'WP3_0b', 'WP3', 'WP3' )
    WP3_0b.hypo_list = [
        ( '#3', 'nonpass_2qW_def', '0excluded', 'SL_2qW_sj_NewTF' ),
        ]
    WP3_0b.hypo_prints['#3'] = 'With subjets (added)'

    ### WP5

    # ======================================
    WP5_All = ROC_configuration( 'WP5_All', 'WP5', 'WP5' )
    WP5_All.hypo_list = [
        ( '#1', 'All', 'All', 'SL_2qW_NewTF' ),
        ( '#3', 'All', 'All', 'SL_2qW_sj_NewTF' ),
        ( '#4', 'pass_2qW_def', 'All', 'SL_2qW_sj_NewTF' ),
        ]

    # ======================================
    WP5_1b = ROC_configuration( 'WP5_1b', 'WP5', 'WP5' )
    WP5_1b.hypo_list = [
        ( '#1', 'All', '1excluded', 'SL_2qW_NewTF' ),
        ( '#3', 'All', '1excluded', 'SL_2qW_sj_NewTF' ),
        ( '#4', 'pass_2qW_def', '1excluded', 'SL_2qW_sj_NewTF' ),
        ]

    # ======================================
    WP5_2b = ROC_configuration( 'WP5_2b', 'WP5', 'WP5' )
    WP5_2b.hypo_list = [
        ( '#1', 'All', '23excluded', 'SL_2qW_NewTF' ),
        ( '#3', 'All', '23excluded', 'SL_2qW_sj_NewTF' ),
        ]

    # ======================================
    WP5_0b = ROC_configuration( 'WP5_0b', 'WP5', 'WP5' )
    WP5_0b.hypo_list = [
        ( '#3', 'nonpass_2qW_def', '0excluded', 'SL_2qW_sj_NewTF' ),
        ]
    WP5_0b.hypo_prints['#3'] = 'With subjets (added)'

    ### WP7

    # ======================================
    WP7_All = ROC_configuration( 'WP7_All', 'WP7', 'WP7' )
    WP7_All.hypo_list = [
        ( '#1', 'All', 'All', 'SL_2qW_NewTF' ),
        ( '#3', 'All', 'All', 'SL_2qW_sj_NewTF' ),
        ( '#4', 'pass_2qW_def', 'All', 'SL_2qW_sj_NewTF' ),
        ]

    # ======================================
    WP7_1b = ROC_configuration( 'WP7_1b', 'WP7', 'WP7' )
    WP7_1b.hypo_list = [
        ( '#1', 'All', '1excluded', 'SL_2qW_NewTF' ),
        ( '#3', 'All', '1excluded', 'SL_2qW_sj_NewTF' ),
        ( '#4', 'pass_2qW_def', '1excluded', 'SL_2qW_sj_NewTF' ),
        ]

    # ======================================
    WP7_2b = ROC_configuration( 'WP7_2b', 'WP7', 'WP7' )
    WP7_2b.hypo_list = [
        ( '#1', 'All', '23excluded', 'SL_2qW_NewTF' ),
        ( '#3', 'All', '23excluded', 'SL_2qW_sj_NewTF' ),
        ]

    # ======================================
    WP7_0b = ROC_configuration( 'WP7_0b', 'WP7', 'WP7' )
    WP7_0b.hypo_list = [
        ( '#3', 'nonpass_2qW_def', '0excluded', 'SL_2qW_sj_NewTF' ),
        ]
    WP7_0b.hypo_prints['#3'] = 'With subjets (added)'


    ########################################
    # Higgs presence
    ########################################

    # ======================================
    higgs_All_nocut = ROC_configuration( 'higgs_All_nocut', 'higgs_All', 'higgs_All' )
    higgs_All_nocut.hypo_list = [
        ( '#1', 'pass_2qW_def', 'All', 'SL_2qW_NewTF' ),
        ( '#3', 'All', 'All', 'SL_2qW_sj_NewTF' ),
        ( '#4', 'pass_2qW_def', 'All', 'SL_2qW_sj_NewTF' ),
        ]

    # ======================================
    higgs_All_ns = ROC_configuration( 'higgs_All_ns', 'higgs_All', 'higgs_All' )
    higgs_All_ns.hypo_list = [
        ( '#1', 'All', 'higgs_ns1', 'SL_2qW_NewTF' ),
        ( '#3', 'All', 'higgs_ns1', 'SL_2qW_sj_NewTF' ),
        ( '#4', 'pass_2qW_def', 'higgs_ns1', 'SL_2qW_sj_NewTF' ),
        ]

    # ======================================
    higgs_All_bb = ROC_configuration( 'higgs_All_bb', 'higgs_All', 'higgs_All' )
    higgs_All_bb.hypo_list = [
        ( '#1', 'All', 'higgs_bb1', 'SL_2qW_NewTF' ),
        ( '#3', 'All', 'higgs_bb1', 'SL_2qW_sj_NewTF' ),
        ( '#4', 'pass_2qW_def', 'higgs_bb1', 'SL_2qW_sj_NewTF' ),
        ]

    # ======================================
    higgs_All_nsbb = ROC_configuration( 'higgs_All_nsbb', 'higgs_All', 'higgs_All' )
    higgs_All_nsbb.hypo_list = [
        ( '#1', 'All', 'higgs_nsbb', 'SL_2qW_NewTF' ),
        ( '#3', 'All', 'higgs_nsbb', 'SL_2qW_sj_NewTF' ),
        ( '#4', 'pass_2qW_def', 'higgs_nsbb', 'SL_2qW_sj_NewTF' ),
        ]

    # 1 b case

    # ======================================
    higgs_1b_nocut = ROC_configuration( 'higgs_1b_nocut', 'higgs_1b', 'higgs_1b' )
    higgs_1b_nocut.hypo_list = [
        ( '#1', 'pass_2qW_def', 'All', 'SL_2qW_NewTF' ),
        ( '#3', 'All', 'All', 'SL_2qW_sj_NewTF' ),
        ( '#4', 'pass_2qW_def', 'All', 'SL_2qW_sj_NewTF' ),
        ]

    # ======================================
    higgs_1b_ns = ROC_configuration( 'higgs_1b_ns', 'higgs_1b', 'higgs_1b' )
    higgs_1b_ns.hypo_list = [
        ( '#1', 'All', 'higgs_ns1', 'SL_2qW_NewTF' ),
        ( '#3', 'All', 'higgs_ns1', 'SL_2qW_sj_NewTF' ),
        ( '#4', 'pass_2qW_def', 'higgs_ns1', 'SL_2qW_sj_NewTF' ),
        ]

    # ======================================
    higgs_1b_bb = ROC_configuration( 'higgs_1b_bb', 'higgs_1b', 'higgs_1b' )
    higgs_1b_bb.hypo_list = [
        ( '#1', 'All', 'higgs_bb1', 'SL_2qW_NewTF' ),
        ( '#3', 'All', 'higgs_bb1', 'SL_2qW_sj_NewTF' ),
        ( '#4', 'pass_2qW_def', 'higgs_bb1', 'SL_2qW_sj_NewTF' ),
        ]

    # ======================================
    higgs_1b_nsbb = ROC_configuration( 'higgs_1b_nsbb', 'higgs_1b', 'higgs_1b' )
    higgs_1b_nsbb.hypo_list = [
        ( '#1', 'All', 'higgs_nsbb', 'SL_2qW_NewTF' ),
        ( '#3', 'All', 'higgs_nsbb', 'SL_2qW_sj_NewTF' ),
        ( '#4', 'pass_2qW_def', 'higgs_nsbb', 'SL_2qW_sj_NewTF' ),
        ]


    ### Q1

    # ======================================
    Q1_All = ROC_configuration( 'Q1_All', 'Q1', 'Q1' )
    Q1_All.hypo_list = [
        ( '#1', 'pass_1qW_def', 'All', 'SL_1qW_NewTF' ),
        ( '#3', 'All', 'All', 'SL_1qW_sj_NewTF' ),
        ( '#4', 'pass_1qW_def', 'All', 'SL_1qW_sj_NewTF' ),
        ]

    # ======================================
    Q1_1b = ROC_configuration( 'Q1_1b', 'Q1', 'Q1' )
    Q1_1b.hypo_list = [
        ( '#1', 'All', '1excluded', 'SL_1qW_NewTF' ),
        ( '#3', 'All', '1excluded', 'SL_1qW_sj_NewTF' ),
        ( '#4', 'pass_1qW_def', '1excluded', 'SL_1qW_sj_NewTF' ),
        ]

    # ======================================
    Q1_2b = ROC_configuration( 'Q1_2b', 'Q1', 'Q1' )
    Q1_2b.hypo_list = [
        ( '#1', 'All', '23excluded', 'SL_1qW_NewTF' ),
        ( '#3', 'All', '23excluded', 'SL_1qW_sj_NewTF' ),
        ]

    # ======================================
    Q1_0b = ROC_configuration( 'Q1_0b', 'Q1', 'Q1' )
    Q1_0b.hypo_list = [
        ( '#3', 'nonpass_1qW_def', '0excluded', 'SL_1qW_sj_NewTF' ),
        ]
    Q1_0b.hypo_prints['#3'] = 'With subjets (added)'



    # ======================================
    Q1_WP3_All = ROC_configuration( 'Q1_WP3_All', 'Q1_WP3', 'Q1_WP3' )
    Q1_WP3_All.hypo_list = [
        ( '#1', 'pass_1qW_def', 'All', 'SL_1qW_NewTF' ),
        ( '#3', 'All', 'All', 'SL_1qW_sj_NewTF' ),
        ( '#4', 'pass_1qW_def', 'All', 'SL_1qW_sj_NewTF' ),
        ]

    # ======================================
    Q1_WP3_1b = ROC_configuration( 'Q1_WP3_1b', 'Q1_WP3', 'Q1_WP3' )
    Q1_WP3_1b.hypo_list = [
        ( '#1', 'All', '1excluded', 'SL_1qW_NewTF' ),
        ( '#3', 'All', '1excluded', 'SL_1qW_sj_NewTF' ),
        ( '#4', 'pass_1qW_def', '1excluded', 'SL_1qW_sj_NewTF' ),
        ]

    # ======================================
    Q1_WP3_2b = ROC_configuration( 'Q1_WP3_2b', 'Q1_WP3', 'Q1_WP3' )
    Q1_WP3_2b.hypo_list = [
        ( '#1', 'All', '23excluded', 'SL_1qW_NewTF' ),
        ( '#3', 'All', '23excluded', 'SL_1qW_sj_NewTF' ),
        ]

    # ======================================
    Q1_WP3_0b = ROC_configuration( 'Q1_WP3_0b', 'Q1_WP3', 'Q1_WP3' )
    Q1_WP3_0b.hypo_list = [
        ( '#3', 'nonpass_1qW_def', '0excluded', 'SL_1qW_sj_NewTF' ),
        ]
    Q1_WP3_0b.hypo_prints['#3'] = 'With subjets (added)'


    ########################################
    # Send to rocdraw
    ########################################

    config_list = [

        Unrestr_All,
        Unrestr_0b,
        Unrestr_1b,
        Unrestr_2b,

        Unrestr_perm,

        nocut_All,
        nocut_0b,
        nocut_1b,
        nocut_2b,

        WP3_All,
        WP3_0b,
        WP3_1b,
        WP3_2b,

        WP5_All,
        WP5_0b,
        WP5_1b,
        WP5_2b,

        WP7_All,
        WP7_0b,
        WP7_1b,
        WP7_2b,

        higgs_All_nocut,
        higgs_All_ns,
        higgs_All_bb,
        higgs_All_nsbb,

        higgs_1b_nocut,
        higgs_1b_ns,
        higgs_1b_bb,
        higgs_1b_nsbb,

        Q1_All,
        Q1_0b,
        Q1_1b,
        Q1_2b,

        Q1_WP3_All,
        Q1_WP3_0b,
        Q1_WP3_1b,
        Q1_WP3_2b,

        ]


    for config in config_list:
        roc_main( config )



########################################
# End of Main
########################################
if __name__ == "__main__":
    main()
