#!/usr/bin/env python
"""
Short program to count entries in a root file and skip too small files
"""

########################################
# Imports
########################################

import ROOT
import os
import sys

########################################
# Functions
########################################

def lfn_to_pfn(fn):
    return "dcap://t3se01.psi.ch:22125/pnfs/psi.ch/cms/trivcat" + fn


########################################
# Main
########################################

def main():

    # ==================
    # Input

    input_dir = 'V12_test2'

    if len( sys.argv ) == 2:
        SB = sys.argv[1]
    else:
        SB = 'sig'
        #SB = 'bkg'

    # ==================


    if SB == 'sig':
        f_in = open( '{0}/tth_V12_13tev.txt'.format(input_dir), 'r' )
        #f_count = open( '{0}/COUNT_tth_V12_13tev.txt'.format(input_dir), 'r' )
    if SB == 'bkg':
        f_in = open( '{0}/ttjets_V12_13tev.txt'.format(input_dir), 'r' )
        #f_count = open( '{0}/COUNT_ttjets_V12_13tev.txt'.format(input_dir), 'r' )

    # Create list of all filenames
    all_filenames = []
    while True:
        filename = f_in.readline()
        if not filename: break
        filename = filename.strip()
        all_filenames.append( filename )
    f_in.close()
    n_all_filenames = len(all_filenames)

    # Initialize list to store filesizes (in # of events)
    all_filesizes = []

    n_total_count = 0

    # Loop over files, count entries
    for i_f, filename in enumerate(all_filenames):
        #if i_f > 400: break

        print '\n========== {0}/{1}, counting entries of:'.format( i_f+1, n_all_filenames )
        print filename

        root_file = ROOT.TFile.Open(lfn_to_pfn(filename))

        root_tree = root_file.Get("tree")
        n_entries = root_tree.GetEntries()

        all_filesizes.append( n_entries )

        TH1F_count = root_file.Get("Count")
        n_count = TH1F_count.Integral()

        if SB == 'sig' and n_entries >= 30000:
            n_total_count += n_count
        if SB == 'bkg' and n_entries >= 30000:
            n_total_count += n_count

        print 'Found entries: {0}  Found count: {1}'.format( n_entries, n_count )

        root_file.Close()

    output_dir = '{0}/output'.format(input_dir)
    if not os.path.isdir( output_dir ):
        os.makedirs( output_dir )

    f_dat = open( '{0}/all_{1}.dat'.format( output_dir, SB ), 'w' )

    for filename, filesize in zip( all_filenames, all_filesizes ):
        f_dat.write( '{0} = {1}\n'.format(filename, filesize) )

    print '\nEntries stored in {0}/all_{1}.dat'.format( output_dir, SB )
    print 'Run Format_filenames.py to cut on entries and to get well formatted files'


    print 'Total found count = {0}'.format( n_total_count )

########################################
# End of Main
########################################
if __name__ == "__main__":
    main()
