#!/usr/bin/env python
"""
Thomas:

"""

########################################
# Imports
########################################



########################################
# Main
########################################

def main():

    input_branch_name_list = [
        'QMatching_n_hadr_bquark_matched_to_bjet',
        'QMatching_n_lept_bquark_matched_to_bjet',
        'QMatching_n_lquarks_matched_to_bjet',
        'QMatching_n_hadr_bquark_matched_to_ljet',
        'QMatching_n_lept_bquark_matched_to_ljet',
        'QMatching_n_lquarks_matched_to_ljet',
        'QMatching_n_hadr_bquark_matched_to_top_subjet',
        'QMatching_n_lept_bquark_matched_to_top_subjet',
        'QMatching_n_lquarks_matched_to_top_subjet',
        'QMatching_n_hadr_bquark_matched_to_otop_subjet',
        'QMatching_n_lept_bquark_matched_to_otop_subjet',
        'QMatching_n_lquarks_matched_to_otop_subjet',
        'QMatching_n_higgs_bquarks_matched_to_bjet',
        'QMatching_n_higgs_bquarks_matched_to_ljet',
        'QMatching_n_higgs_bquarks_matched_to_top_subjet',
        'QMatching_n_higgs_bquarks_matched_to_otop_subjet',
        ]

    # Fill defaults (comment out if needed specifically)
    input_attribute_name_list = []
    input_help_str_list = []
    input_add_hasattr_else_list = []
    for branch_name in input_branch_name_list:
        input_attribute_name_list.append( branch_name )
        input_help_str_list.append( '' )
        input_add_hasattr_else_list.append( True )

    # Create branch codes
    output_str = ''    
    for i in range( len( input_branch_name_list )):

        if input_add_hasattr_else_list[i]:
            thisbranch_str = """
                    NTupleVariable(
                        "{0}",
                        lambda ev: ev.{1} if hasattr(ev,'{1}') else -1,
                        help="{2}"
                    ),""".format(
                        input_branch_name_list[i],
                        input_attribute_name_list[i],
                        input_help_str_list[i],
                        )
        else:
            thisbranch_str = """
                    NTupleVariable(
                        "{0}",
                        lambda ev: ev.{1},
                        help="{2}"
                    ),""".format(
                        input_branch_name_list[i],
                        input_attribute_name_list[i],
                        input_help_str_list[i],
                        )

        output_str += thisbranch_str

    # Write to file
    out_f = open('Create_branches_output.txt', 'w')
    out_f.write( output_str )
    out_f.close()



########################################
# End of Main
########################################
if __name__ == "__main__":
    main()
