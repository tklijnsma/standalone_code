#!/usr/bin/env python
"""
Thomas:

Examples on how to use TFMatrix.dat

2 plots are created: 1 transfer function, and 1 cumulative distribution function

"""

########################################
# Imports
########################################

import pickle
import ROOT
import os

from TFClasses import TF


########################################
# Main
########################################

def main():

    ROOT.gROOT.SetBatch(True)
    ROOT.gROOT.ProcessLine("gErrorIgnoreLevel = 1001;")
    ROOT.gStyle.SetOptFit(1011)
    ROOT.gStyle.SetLegendBorderSize(0)

    c1 = ROOT.TCanvas("c1","c1",500,400)
    c1.SetGrid()

    outputdir = 'TFtest_output_revised'

    if not os.path.isdir( outputdir ):
        os.makedirs( outputdir + '/plots' )
        os.makedirs( outputdir + '/specifics' )

    # Open TFMatrix.dat
    pickle_f = open( 'TFMatrix.dat' , 'rb' )
    TFmat = pickle.load( pickle_f )
    pickle_f.close()

    # Open config
    #pickle_f = open( outputdir + '/config.dat' , 'rb' )
    #config = pickle.load( pickle_f )
    #pickle_f.close()

    # Choose a TF; As an example the TF for a b in the first eta-bin is chosen.
    #   (b is fitted with double Gaussians, l with single Gaussians)
    myTF = TFmat['b'][0]

    # Determine Make_Formula output:
    # - True:  [0] = reconstr., x = mc/gen/quark
    # - False: [0] = mc/gen/quark, x = reconstr.
    # No argument is treated as True

    #plot_pts = [ -10.0, 0.0, 20.0, 50.0, 100.0, 150.0, 250.0, 400.0 ]
    plot_pts = [ 50.0, 100.0 ]

    ########################################
    # Plot example functions
    ########################################

    # plot_pts as reco pts (get distribution of quark energies)
    # ======================================

    hf = open( outputdir + '/reco_overview.html', 'w' )
    hf.write( '<html><body>\n<h1>Set reco, get quark dist\n</h1>\n<br>\n<hr />\n' )

    for i_pt, reco_pt in enumerate(plot_pts):

        f1 = myTF.Make_Formula( True )
        f1.SetLineWidth(2)

        # Normalize
        f1.SetParameter( 1, 1.0/f1.Integral(-10.0,400.0) )

        # Set reco pt
        f1.SetParameter( 0, reco_pt )

        # Write some specifics to text file
        f_spec = open( outputdir + '/specifics/TF_reco_{0}.txt'.format(i_pt) , 'w' )
        f_spec.write( 'Specifics of the TF:\n' )
        f_spec.write( f1.GetTitle() + '\n' )
        for i in range( f1.GetNumberFreeParameters() ):
            f_spec.write( '    [{0}] = {1}\n'.format( i, f1.GetParameter(i) ) )
        f_spec.close()

        # Drawing
        #f1.SetRange( min( 2*reco_pt, 0.0 ) , max( 2*reco_pt, 50.0 ) )
        f1.SetRange( 30.0, 180.0 )


        #f1.SetTitle( 'Set reco_pt = {0}, draw reco pt distribution'.format(reco_pt))
        f1.SetTitle( '' )

        f1.Draw()


        # Vertical line
        #y_min = c1.GetUymin()
        #y_max = c1.GetUymax()
        y_max = f1.GetMaximum()

        v_line = ROOT.TLine( reco_pt, 0.0, reco_pt, 0.061 )
        v_line.SetLineStyle(2)
        v_line.SetLineColor(13)
        v_line.SetLineWidth(4)
        v_line.Draw("SAME")


        # Lerecod
        leg = ROOT.TLegend(0.7,0.78,0.88,0.88)
        leg.SetTextAlign(12)
        leg.SetFillStyle(0)
        leg.AddEntry( f1, 'P(p_{T,gen})', 'l' )
        leg.AddEntry( v_line, 'p_{T,reco}', 'l' )
        leg.Draw("SAME")

        
        #x_label = ROOT.TLatex( 0.0, 0.0, 'p_T');
        #f1.GetXaxis().SetTitle( x_label )
        f1.GetXaxis().SetTitle( "p_{T} (GeV)" )
        f1.GetYaxis().SetTitle( "A.U." )
        f1.GetYaxis().SetTitleOffset(1.3)


        c1.Modified()
        c1.Update()

        fn_out = outputdir + '/plots/TF_reco_{0}'.format(i_pt)
        fn_out_hlink = 'plots/TF_reco_{0}'.format(i_pt)

        c1.Print( fn_out + ".pdf" , "pdf", )
        c1.Print( fn_out + ".tex" , "tex", )

        img = ROOT.TImage.Create()
        img.FromPad(c1)
        img.WriteImage( fn_out + '.png' )

        hf.write( '<a href="{0}.pdf"><img width="350" src="{0}.png"></a>\n'.format(fn_out_hlink) )
        hf.write( '</br>\n' )

    hf.close()



    # plot_pts as gen pts (get distribution of reco energies)
    # ======================================

    hf = open( outputdir + '/gen_overview.html', 'w' )
    hf.write( '<html><body>\n<h1>Set gen, get quark dist\n</h1>\n<br>\n<hr />\n' )

    for i_pt, gen_pt in enumerate(plot_pts):

        f1 = myTF.Make_Formula( False )
        f1.SetLineWidth(2)

        # Normalize
        f1.SetParameter( 1, 1.0/f1.Integral(-10.0,400.0) )

        # Set gen pt
        f1.SetParameter( 0, gen_pt )

        # Write some specifics to text file
        f_spec = open( outputdir + '/specifics/TF_gen_{0}.txt'.format(i_pt) , 'w' )
        f_spec.write( 'Specifics of the TF:\n' )
        f_spec.write( f1.GetTitle() + '\n' )
        for i in range( f1.GetNumberFreeParameters() ):
            f_spec.write( '    [{0}] = {1}\n'.format( i, f1.GetParameter(i) ) )
        f_spec.close()

        # Drawing
        f1.SetRange( min( 2*gen_pt, 0.0 ) , max( 2*gen_pt, 50.0 ) )


        #f1.SetTitle( 'Set gen_pt = {0}, draw reco pt distribution'.format(gen_pt))
        f1.SetTitle( '' )

        f1.Draw()


        # Vertical line
        y_min = c1.GetUymin()
        y_max = c1.GetUymax()

        v_line = ROOT.TLine( gen_pt, 0.0, gen_pt, y_max )
        v_line.SetLineStyle(2)
        v_line.SetLineColor(13)
        v_line.SetLineWidth(4)
        v_line.Draw("SAME")


        # Legend
        leg = ROOT.TLegend(0.7,0.78,0.88,0.88)
        leg.SetTextAlign(12)
        leg.SetFillStyle(0)
        ROOT.gStyle.SetLegendBorderSize(0)
        leg.AddEntry( f1, 'P(p_{T,reco})', 'l' )
        leg.AddEntry( v_line, 'p_{T,gen}', 'l' )
        leg.Draw("SAME")

        
        #x_label = ROOT.TLatex( 0.0, 0.0, 'p_T');
        #f1.GetXaxis().SetTitle( x_label )
        f1.GetXaxis().SetTitle( "p_{T} (GeV)" )
        f1.GetYaxis().SetTitle( "A.U." )
        f1.GetYaxis().SetTitleOffset(1.3)


        c1.Update()

        fn_out = outputdir + '/plots/TF_gen_{0}'.format(i_pt)
        fn_out_hlink = 'plots/TF_gen_{0}'.format(i_pt)

        c1.Print( fn_out + ".pdf" , "pdf", )
        c1.Print( fn_out + ".tex" , "tex", )

        img = ROOT.TImage.Create()
        img.FromPad(c1)
        img.WriteImage( fn_out + '.png' )

        hf.write( '<a href="{0}.pdf"><img width="350" src="{0}.png"></a>\n'.format(fn_out_hlink) )
        hf.write( '</br>\n' )

    hf.close()


    # plot_pts as gen pts, drawing the CDF
    # ======================================

    hf = open( outputdir + '/cdf_overview.html', 'w' )
    hf.write( '<html><body>\n<h1>Set cdf, get quark dist\n</h1>\n<br>\n<hr />\n' )

    for i_pt, cdf_pt in enumerate(plot_pts):

        f1 = myTF.Make_CDF()
        f1.SetLineWidth(2)

        # Normalize
        #f1.SetParameter( 1, 1.0/f1.Integral(-10.0,400.0) )

        # Set cdf pt
        f1.SetParameter( 0, cdf_pt )

        # Write some specifics to text file
        f_spec = open( outputdir + '/specifics/TF_cdf_{0}.txt'.format(i_pt) , 'w' )
        f_spec.write( 'Specifics of the TF:\n' )
        f_spec.write( f1.GetTitle() + '\n' )
        for i in range( f1.GetNumberFreeParameters() ):
            f_spec.write( '    [{0}] = {1}\n'.format( i, f1.GetParameter(i) ) )
        f_spec.close()

        # Drawing
        #f1.SetRange( min( 2*cdf_pt, 0.0 ) , max( 2*cdf_pt, 50.0 ) )
        f1.SetRange( 0.0, 100.0 )


        #f1.SetTitle( 'Set cdf_pt = {0}, draw cdf pt distribution'.format(cdf_pt))
        f1.SetTitle( '' )

        f1.Draw()


        # Vertical line
        #y_min = c1.GetUymin()
        #y_max = c1.GetUymax()
        y_max = f1.GetMaximum()

        v_line = ROOT.TLine( cdf_pt, 0.0, cdf_pt, 1.05 )
        v_line.SetLineStyle(2)
        v_line.SetLineColor(13)
        v_line.SetLineWidth(4)
        v_line.Draw("SAME")


        print 'Cutoff chance at pt={0}: {1}'.format( cdf_pt, f1.Eval(30.0) )

        v_line2 = ROOT.TLine( 30.0, 0.0, 30.0, f1.Eval(30.0) )
        v_line2.SetLineStyle(1)
        v_line2.SetLineColor(4)
        v_line2.SetLineWidth(4)
        v_line2.Draw("SAME")


        # Legend
        leg = ROOT.TLegend(0.7,0.75,0.88,0.85)
        leg.SetTextAlign(12)
        leg.SetFillStyle(0)
        leg.AddEntry( f1, 'CDF(p_{T,reco})', 'l' )
        leg.AddEntry( v_line, 'p_{T,gen}', 'l' )
        leg.Draw("SAME")

        
        #x_label = ROOT.TLatex( 0.0, 0.0, 'p_T');
        #f1.GetXaxis().SetTitle( x_label )
        f1.GetXaxis().SetTitle( "p_{T} (GeV)" )
        f1.GetYaxis().SetTitle( "A.U." )
        f1.GetYaxis().SetTitleOffset(1.3)


        c1.Modified()
        c1.Update()

        fn_out = outputdir + '/plots/TF_cdf_{0}'.format(i_pt)
        fn_out_hlink = 'plots/TF_cdf_{0}'.format(i_pt)

        c1.Print( fn_out + ".pdf" , "pdf", )
        c1.Print( fn_out + ".tex" , "tex", )

        img = ROOT.TImage.Create()
        img.FromPad(c1)
        img.WriteImage( fn_out + '.png' )

        hf.write( '<a href="{0}.pdf"><img width="350" src="{0}.png"></a>\n'.format(fn_out_hlink) )
        hf.write( '</br>\n' )

    hf.close()






########################################
# End of Main
########################################
if __name__ == "__main__":
  main()
