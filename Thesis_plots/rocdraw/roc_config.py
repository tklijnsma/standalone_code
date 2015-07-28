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
            '#2'    : 'With subjets',
            '#3'    : 'With subjets + perm.',
            '#4'    : 'Default (+htt)',
            }

        self.hypo_colors = {
            '#1'    : 2,
            '#2'    : 4,
            '#3'    : 8,
            '#4'    : 42,
            }






########################################
# Main
########################################

def main():

    ########################################
    # Approach 1
    ########################################


    # ======================================
    Unrestr_All = ROC_configuration( 'AP1_All', 'Unrestructured', 'AP1' )
    Unrestr_All.hypo_list = [
        ( '#1', 'All', 'All', 'SL_2qW_NewTF' ),
        ( '#4', 'pass_2qW_def', 'All', 'SL_2qW_NewTF' ),
        ( '#2', 'All', 'All', 'SL_2qW_sj_NewTF' ),
        ( '#3', 'All', 'All', 'SL_2qW_sj_perm_NewTF' ),
        ]

    # ======================================
    Unrestr_1b  = ROC_configuration( 'AP1_1b', 'Unrestructured', 'AP1' )
    Unrestr_1b.hypo_list = [
        ( '#1', 'All', 'ETN7', 'SL_2qW_NewTF' ),
        ( '#2', 'All', 'ETN7', 'SL_2qW_sj_NewTF' ),
        ( '#3', 'All', 'ETN7', 'SL_2qW_sj_perm_NewTF' ),
        ]

    # ======================================
    Unrestr_2b  = ROC_configuration( 'AP1_2b', 'Unrestructured', 'AP1' )
    Unrestr_2b.hypo_list = [
        ( '#1', 'All', 'ETN9', 'SL_2qW_NewTF' ),
        ( '#2', 'All', 'ETN9', 'SL_2qW_sj_NewTF' ),
        ]
    
    # ======================================
    Unrestr_0b  = ROC_configuration( 'AP1_0b', 'Unrestructured', 'AP1' )
    Unrestr_0b.hypo_list = [
        ( '#2', 'nonpass_2qW_def', 'ETN16', 'SL_2qW_sj_NewTF' ),
        ( '#3', 'nonpass_2qW_def', 'ETN16', 'SL_2qW_sj_perm_NewTF' ),
        ]


    ########################################
    # Approach 2
    ########################################

    ### No cuts

    # ======================================
    nocut_All = ROC_configuration( 'nocut_All', 'nocut', 'nocut' )

    # ======================================
    nocut_1b = ROC_configuration( 'nocut_1b', 'nocut', 'nocut' )
    nocut_1b.hypo_list = [
        ( '#1', 'All', '1excluded', 'SL_2qW_NewTF' ),
        ( '#2', 'All', '1excluded', 'SL_2qW_sj_NewTF' ),
        ( '#3', 'All', '1excluded', 'SL_2qW_sj_perm_NewTF' ),
        ]

    # ======================================
    nocut_2b = ROC_configuration( 'nocut_2b', 'nocut', 'nocut' )
    nocut_2b.hypo_list = [
        ( '#1', 'All', '23excluded', 'SL_2qW_NewTF' ),
        ( '#2', 'All', '23excluded', 'SL_2qW_sj_NewTF' ),
        ]

    # ======================================
    nocut_0b = ROC_configuration( 'nocut_0b', 'nocut', 'nocut' )
    nocut_0b.hypo_list = [
        ( '#2', 'nonpass_2qW_def', '0excluded', 'SL_2qW_sj_NewTF' ),
        ( '#3', 'nonpass_2qW_def', '0excluded', 'SL_2qW_sj_perm_NewTF' ),
        ]

    ### WP3

    # ======================================
    WP3_All = ROC_configuration( 'WP3_All', 'WP3', 'WP3' )

    # ======================================
    WP3_1b = ROC_configuration( 'WP3_1b', 'WP3', 'WP3' )
    WP3_1b.hypo_list = [
        ( '#1', 'All', '1excluded', 'SL_2qW_NewTF' ),
        ( '#2', 'All', '1excluded', 'SL_2qW_sj_NewTF' ),
        ( '#3', 'All', '1excluded', 'SL_2qW_sj_perm_NewTF' ),
        ]

    # ======================================
    WP3_2b = ROC_configuration( 'WP3_2b', 'WP3', 'WP3' )
    WP3_2b.hypo_list = [
        ( '#1', 'All', '23excluded', 'SL_2qW_NewTF' ),
        ( '#2', 'All', '23excluded', 'SL_2qW_sj_NewTF' ),
        ]

    # ======================================
    WP3_0b = ROC_configuration( 'WP3_0b', 'WP3', 'WP3' )
    WP3_0b.hypo_list = [
        ( '#2', 'nonpass_2qW_def', '0excluded', 'SL_2qW_sj_NewTF' ),
        ( '#3', 'nonpass_2qW_def', '0excluded', 'SL_2qW_sj_perm_NewTF' ),
        ]

    ### WP5

    # ======================================
    WP5_All = ROC_configuration( 'WP5_All', 'WP5', 'WP5' )

    # ======================================
    WP5_1b = ROC_configuration( 'WP5_1b', 'WP5', 'WP5' )
    WP5_1b.hypo_list = [
        ( '#1', 'All', '1excluded', 'SL_2qW_NewTF' ),
        ( '#2', 'All', '1excluded', 'SL_2qW_sj_NewTF' ),
        ( '#3', 'All', '1excluded', 'SL_2qW_sj_perm_NewTF' ),
        ]

    # ======================================
    WP5_2b = ROC_configuration( 'WP5_2b', 'WP5', 'WP5' )
    WP5_2b.hypo_list = [
        ( '#1', 'All', '23excluded', 'SL_2qW_NewTF' ),
        ( '#2', 'All', '23excluded', 'SL_2qW_sj_NewTF' ),
        ]

    # ======================================
    WP5_0b = ROC_configuration( 'WP5_0b', 'WP5', 'WP5' )
    WP5_0b.hypo_list = [
        ( '#2', 'nonpass_2qW_def', '0excluded', 'SL_2qW_sj_NewTF' ),
        ( '#3', 'nonpass_2qW_def', '0excluded', 'SL_2qW_sj_perm_NewTF' ),
        ]

    ### WP7

    # ======================================
    WP7_All = ROC_configuration( 'WP7_All', 'WP7', 'WP7' )

    # ======================================
    WP7_1b = ROC_configuration( 'WP7_1b', 'WP7', 'WP7' )
    WP7_1b.hypo_list = [
        ( '#1', 'All', '1excluded', 'SL_2qW_NewTF' ),
        ( '#2', 'All', '1excluded', 'SL_2qW_sj_NewTF' ),
        ( '#3', 'All', '1excluded', 'SL_2qW_sj_perm_NewTF' ),
        ]

    # ======================================
    WP7_2b = ROC_configuration( 'WP7_2b', 'WP7', 'WP7' )
    WP7_2b.hypo_list = [
        ( '#1', 'All', '23excluded', 'SL_2qW_NewTF' ),
        ( '#2', 'All', '23excluded', 'SL_2qW_sj_NewTF' ),
        ]

    # ======================================
    WP7_0b = ROC_configuration( 'WP7_0b', 'WP7', 'WP7' )
    WP7_0b.hypo_list = [
        ( '#2', 'nonpass_2qW_def', '0excluded', 'SL_2qW_sj_NewTF' ),
        ( '#3', 'nonpass_2qW_def', '0excluded', 'SL_2qW_sj_perm_NewTF' ),
        ]

    ########################################
    # Send to rocdraw
    ########################################

    config_list = [

        Unrestr_All,
        Unrestr_0b,
        Unrestr_1b,
        Unrestr_2b,

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

        ]


    for config in config_list:
        roc_main( config )



########################################
# End of Main
########################################
if __name__ == "__main__":
    main()
