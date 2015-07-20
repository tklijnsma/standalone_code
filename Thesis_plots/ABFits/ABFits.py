#!/usr/bin/env python
"""
Thomas:

"""

counter = 0

########################################
# Imports
########################################


import ROOT
import copy


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
            y_errors[i] )

    #gr.SetTitle( 'TGraph_{0}'.format( filename.split('.')[0] ) )

    gr.SetMarkerColor(4)
    gr.SetMarkerStyle(22)
    gr.SetMarkerSize(0.8)

    return gr



def Fit_TGraph( gr, par, filename ):

    
    if par == 2 or par == 4:
        func_str = "sqrt([0]*[0] + x*[1]*[1] + x*x*[2]*[2])"
        func_init = [ "0", "0", "0" ]
    else:
        func_str = "[0]+[1]*x"
        func_init = []

    #func_str = '[0]*1.0/x + [1]*x*x*x+[2]*x*x+[3]*x+[4]'
    #func_str = '[0]*x*x*x+[1]*x*x+[2]*x+[3]'
    #func_init = []


    f1 = ROOT.TF1( "fit1", func_str )

    #for i, init_val in enumerate( func_init ):
    #    f1.SetParameter( i, float(init_val) )

    # Dummy fit to link objects
    #f1.SetRange( 30.0, 300.0 )
    #gr.Fit(f1,'Q')



    # Get actual pars
    f_in = open( filename, 'r' )
    fitpars_list = ['']
    while True:
        line = f_in.readline()
        if not line: break
        line = line.strip()
        fitpars_list.append( line.split(',')[:-1] )
    f_in.close()
    fitpars = fitpars_list[par]

    for i_fitpar, fitpar in enumerate(fitpars):
        f1.SetParameter(i_fitpar, float(fitpar))

    for i in range(len(fitpars)):
        print f1.GetParameter(i)

    return copy.deepcopy(f1)



def Draw_TGraph( gr, f1, c1, par ):

    gr.Draw('AP')
    f1.Draw("SAME")
    f1.SetRange(30.0,300.0)

    par_strs = [ '', '#mu_{1}', '#sigma_{1}', '#mu_{2}', '#sigma_{2}' ]
    par_letters = [ '', 'a', 'c', 'b', 'd' ]
    par_funcs = [ '',
        '#mu_{1} = a_{0} + a_{1} p_{T,gen}',
        '#sigma_{1} = #sqrt{ c_{0}^{2} + c_{1}^{2} p_{T,gen} + c_{2}^{2} p_{T,gen}^{2} }',
        '#mu_{2} = b_{0} + b_{1} p_{T,gen}',
        '#sigma_{2} = #sqrt{ d_{0}^{2} + d_{1}^{2} p_{T,gen} + d_{2}^{2} p_{T,gen}^{2} }',
        ]

    par_str = '{0}(p_{{T,gen}})'.format( par_strs[par] )

    gr.SetTitle( 'Fit for ' + par_str )
    gr.GetXaxis().SetTitle( 'p_{T,gen} (GeV)' )
    gr.GetYaxis().SetTitle( par_str )


    # Set label specifics
    lbl = ROOT.TText()
    lbl.SetNDC()
    lbl.SetTextSize(0.04)
    lbl.SetTextColor(1)

    tl = ROOT.TLatex()
    tl.SetNDC()
    tl.SetTextSize(0.04)
    tl.SetTextColor(1)


    # Coordinates for the histogram specifics
    anchorx = 0.13
    anchory = 0.80
    nl = 0.05
    nc = 0.07

    #lbl.SetTextColor(4)
    #lbl.DrawText( anchorx, anchory, 'Hist spec.')
    #lbl.SetTextColor(1)
    #anchory-=nl

    let = par_letters[par]

    #f1 = gr.GetFunction('fit1')

    tl.SetTextSize(0.05)
    tl.DrawLatex( anchorx, anchory , par_funcs[par] )
    tl.SetTextSize(0.04)
    anchory -= nl+0.03

    tl.DrawLatex( anchorx, anchory , let + '_{0}:' )
    lbl.DrawText( anchorx + nc, anchory , '{0:.4g}'.format(f1.GetParameter(0)) )
    anchory -= nl

    tl.DrawLatex( anchorx, anchory , let + '_{1}:' )
    lbl.DrawText( anchorx + nc, anchory , '{0:.4g}'.format(f1.GetParameter(1)) )
    anchory -= nl

    if par == 2 or par == 4:
        tl.DrawLatex( anchorx, anchory , let + '_{2}:' )
        lbl.DrawText( anchorx + nc, anchory , '{0:.4g}'.format(f1.GetParameter(2)) )
        anchory -= nl


    c1.Modified()
    c1.Update()

    global counter
    out_name = 'plots/' + str(counter)
    counter += 1

    c1.Print( out_name + '.pdf' , 'pdf')

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

    #par = 1
    parteta = 'b0'


    for par in range(1,5):

        fn_unfitted = 'unfittedpoints/unfittedpoints_{0}_{1}.txt'.format( par, parteta )
        fn_fitpars = 'fitpars/fitpars_{0}.txt'.format(parteta)

        f_html = open( 'overview_{0}.html'.format(par), 'w' )
        f_html.write( '<html><body>\n<h1>Fittest overview\n</h1>\n<br>\n<hr />' )

        number_of_cols = 2
        plot_count = 0


        gr = Get_TGraph( fn_unfitted )
        f1 = Fit_TGraph( gr, par, fn_fitpars )
        Draw_TGraph( gr, f1, c1, par )

        f_html.write('<a href="{0}"><img width="500" src="{0}.png"></a>\n'.format(gr.out_name) )

        plot_count += 1
        if plot_count == number_of_cols:
            f_html.write( '<br>\n' )
            
    








########################################
# End of Main
########################################
if __name__ == "__main__":
    main()
