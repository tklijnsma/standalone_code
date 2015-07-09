#!/usr/bin/env python
"""
Thomas:

"""

########################################
# Imports
########################################


import ROOT


########################################
# Functions
########################################

def Read_unfitted_datafile( filename ):

    f_in = open( filename, 'r' )

    x_values = []
    x_errors = []
    y_values = []
    y_errors = []

    while True:
        line = f_in.readline()
        if not line: break
        line = line.strip()

        points_list = line.split(',')
        x_values.append( float( points_list[0] ) )
        x_errors.append( float( points_list[1] ) )
        y_values.append( float( points_list[2] ) )
        y_errors.append( float( points_list[3] ) )

    f_in.close()

    return ( x_values, x_errors, y_values, y_errors )

def Get_TGraph( filename ):

    ( x_values, x_errors, y_values, y_errors ) = Read_unfitted_datafile( filename )

    n_points = len(x_values)

    gr = ROOT.TGraphErrors( n_points )

    for i in range( n_points ):

        gr.SetPoint(
            i,
            x_values[i],
            y_values[i] )

        gr.SetPointError(
            i,
            x_errors[i],
            x_errors[i] )

    gr.SetTitle( 'TGraph_{0}'.format( filename.split('.')[0] ) )

    gr.SetMarkerColor(4)
    gr.SetMarkerStyle(22)
    gr.SetMarkerSize(0.8)

    return gr



def Fit_TGraph( gr ):


    #func_str = "sqrt([0]*[0] + x*[1]*[1] + x*x*[2]*[2])"
    #func_init = [ "0", "0", "0" ]

    func_str = '[0]*1.0/x + [1]*x*x*x+[2]*x*x+[3]*x+[4]'

    func_init = []


    f1 = ROOT.TF1( "fit1", func_str )

    for i, init_val in enumerate( func_init ):
        f1.SetParameter( i, float(init_val) )

    #f1.SetRange( 30.0, 300.0 )

    gr.Fit(f1,'Q')
    gr.Fit(f1,'Q')
    gr.Fit(f1,'Q')





def Draw_TGraph( gr, c1 ):

    gr.Draw('AP')
    c1.Update()

    out_name = 'plots/' + gr.GetTitle()

    c1.Print( out_name , 'pdf')

    img = ROOT.TImage.Create()
    img.FromPad(c1)
    img.WriteImage( out_name + '.png' )

    setattr( gr, 'out_name', out_name )
    


########################################
# Main
########################################

def main():

    ROOT.gROOT.SetBatch(True)
    ROOT.gROOT.ProcessLine("gErrorIgnoreLevel = 1001;")

    c1 = ROOT.TCanvas("c1","c1",500,400)
    c1.SetGrid()

    filenames = [
        'unfittedpoints_2_b0.txt',
        'unfittedpoints_2_b1.txt',
        'unfittedpoints_2_l0.txt',
        'unfittedpoints_2_l1.txt',
        ]

    f_html = open( 'overview_2.html' , 'w' )
    f_html.write( '<html><body>\n<h1>Fittest overview\n</h1>\n<br>\n<hr />' )

    number_of_cols = 2
    plot_count = 0

    for filename in filenames:
        gr = Get_TGraph( filename )
        Fit_TGraph( gr )
        Draw_TGraph( gr, c1 )
    
        f_html.write('<a href="{0}"><img width="500" src="{0}.png"></a>\n'.format(gr.out_name) )

        plot_count += 1
        if plot_count == number_of_cols:
            f_html.write( '<br>\n' )
        
    








########################################
# End of Main
########################################
if __name__ == "__main__":
    main()
