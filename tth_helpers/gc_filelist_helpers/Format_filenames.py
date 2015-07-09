#!/usr/bin/env python
"""
Thomas:

"""

########################################
# Imports
########################################

import imp
import sys


########################################
# Functions
########################################

def Read_dat( dat_filename ):

    f_in = open( dat_filename, 'r' )

    filenames = []
    filesizes = []

    while True:
        line = f_in.readline()
        if not line: break
        line = line.strip()
        line_list = line.split(' = ')
        filenames.append( line_list[0] )
        filesizes.append( int(line_list[1]) )

    f_in.close()

    return ( filenames, filesizes )


def Write_gc_dataset( filenames, filesizes, output_dir, SB ):

    out_f = open( '{0}/{1}.dat'.format(output_dir,SB), 'w' )

    if SB == 'sig':
        out_f.write( '[tth_V12_13tev]\n' )
    if SB == 'bkg':
        out_f.write( '[ttjets_V12_13tev]\n' )

    for ( filename, filesize ) in zip( filenames, filesizes ):
        out_f.write( '{0} = {1}\n'.format( filename, filesize ) )

    out_f.close()


def Write_samples_vhbb_list( filenames, filesizes, output_dir, SB ):

    out_f = open( '{0}/samples_vhbb_{1}_copypaste.txt'.format(output_dir,SB), 'w' )

    for ( filename, filesize ) in zip( filenames, filesizes ):
        out_f.write( '            "{0}",\n'.format( filename ) )

    out_f.close()

def Write_plain_list( filenames, filesizes, output_dir, SB ):

    out_f = open( '{0}/plain_{1}.txt'.format(output_dir,SB), 'w' )

    for filename in filenames:
        out_f.write( filename + '\n' )

    out_f.close()


########################################
# Main
########################################

def main():

    # ==================
    # Input

    input_dir = 'V12'

    if len( sys.argv ) == 2:
        SB = sys.argv[1]
    else:
        #SB = 'sig'
        SB = 'bkg'

    n_entries_cutoff = 30000

    # ==================


    output_dir = input_dir + '/output'
    ( all_filenames, all_filesizes ) = \
        Read_dat( '{0}/all_{1}.dat'.format(output_dir, SB) )

    filenames = []
    filesizes = []
    skipped_filenames = []
    skipped_filesizes = []

    for filename, filesize in zip( all_filenames, all_filesizes ):

        if filesize < n_entries_cutoff:
            skipped_filenames.append( filename )
            skipped_filesizes.append( filesize )
        else:
            filenames.append( filename )
            filesizes.append( filesize )


    # Write file with some statistics
    total_entries = sum( all_filesizes )
    used_entries = sum( filesizes )
    percentage = float( used_entries ) / float( total_entries ) * 100.0

    f_stat = open( '{0}/report_{1}.txt'.format(output_dir,SB) , 'w' )

    f_stat.write( '=== Report on {0} ===\n\n'.format(SB) )

    f_stat.write( 'Input_dir        : {0}\n'.format( input_dir ) )
    f_stat.write( 'SB               : {0}\n'.format( SB ) )
    f_stat.write( 'n_entries_cutoff : {0}\n\n'.format( n_entries_cutoff ) )

    f_stat.write( 'Used entries     : {0}\n'.format( used_entries ) )
    f_stat.write( 'Total entries    : {0}\n'.format( total_entries ) )
    f_stat.write( 'Percentage used  : {0:.4f} %\n\n'.format( percentage ) )

    f_stat.write( 'Total files      : {0}\n'.format( len( all_filenames ) ) )
    f_stat.write( 'Kept files       : {0}\n'.format( len( filenames ) ) )
    f_stat.write( 'Skipped files    : {0}\n\n'.format( len( skipped_filenames ) ) )

    f_stat.write( 'Skipped filenames:\n\n' )

    for filename, filesize in zip( skipped_filenames, skipped_filesizes ):
        f_stat.write( '{0} = {1}\n'.format( filename, filesize ) )

    f_stat.close()


    # Create the several formats

    Write_gc_dataset( filenames, filesizes, output_dir, SB )
    Write_samples_vhbb_list( filenames, filesizes, output_dir, SB )
    Write_plain_list( filenames, filesizes, output_dir, SB )


########################################
# End of Main
########################################
if __name__ == "__main__":
    main()
