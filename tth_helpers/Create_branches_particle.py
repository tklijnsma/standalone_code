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

    input_dict = {

        'httCandidate' : [
            'fRec',
            'Ropt',
            'RoptCalc',
            'ptForRoptCalc',
            'pt',
            'eta',
            'phi',
            'mass',
            'sjW1pt',
            'sjW1eta',
            'sjW1phi',
            'sjW1mass',
            'sjW1btag',
            'sjW2pt',
            'sjW2eta',
            'sjW2phi',
            'sjW2mass',
            'sjW2btag',
            'sjNonWpt',
            'sjNonWeta',
            'sjNonWphi',
            'sjNonWmass',
            'sjNonWbtag',
            ],

        'FatjetCA15ungroomed' : [
            'pt',
            'eta',
            'phi',
            'mass',
            'tau1',
            'tau2',
            'tau3',
            'bbtag',
            ],

        'FatjetCA15pruned' : [
            'pt',
            'eta',
            'phi',
            'mass',
            ],

        'SubjetCA15pruned' : [
            'pt',
            'eta',
            'phi',
            'mass',
            'btag',
            ],

        }

    key_list = [
        'httCandidate',
        'FatjetCA15ungroomed',
        'FatjetCA15pruned',
        'SubjetCA15pruned',
        ]



    # Create branch codes
    output_str = ''    
    Type_str = ''

    for Type_name in key_list:

        Type_str = '{0}Type = NTupleObjectType("{0}Type", variables = ['.format(
            Type_name)

        for variable in input_dict[Type_name]:

            # If just a string, create normal NTupleVariable
            if isinstance( variable, basestring ):
                hasattr_else = False
            # Else, check if hasattr_else needs to be added
            else:
                ( variable, hasattr_else ) = variable

            if hasattr_else == False:
                variable_str = \
                    '\n    NTupleVariable("{0}", lambda x: x.{0} ),'.format(
                        variable
                        )
            else:
                variable_str = \
                    '\n    NTupleVariable("{0}", lambda x: x.{0} \\\n        if hasattr(ev,"{0}") else -1 ),'.format( variable )

            Type_str += variable_str

        Type_str += '\n])\n\n'

        output_str += Type_str



    # Also create the strings to call
    output_str += '\n'
    for Type_name in key_list:

        output_str += \
            '\n            "{0}" : NTupleCollection("{0}", {0}Type, {1}, help=""),'.format(
                Type_name, len(input_dict[Type_name] ) )
            



    # Write to file
    out_f = open('Create_branches_output.txt', 'w')
    out_f.write( output_str )
    out_f.close()



########################################
# End of Main
########################################
if __name__ == "__main__":
    main()
