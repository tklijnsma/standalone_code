class MEM_Table_configuration:
    def __init__(self):

        # Loads the dict which contains the selection strings for each category
        self.Set_sel_dict() 

        self.Draw_plots = True


        # ==========================================
        # Select one configuration here


        self.Oldcat_SJcat_pass_nopass()
        #self.Cat_overview()
        #self.NewTF_OldTF()


        # ==========================================


        # Set the selection string so that denominator > 0
        self.Set_selection_per_hypo(
            'denominatornonzero'
            )

        # Specify to use genweights
        self.UseGenWeights = True

        # Number of bins in mem ratio hist
        self.n_mem_hist_bins = 15



    ########################################
    # Different configurations
    ########################################

    def Oldcat_SJcat_pass_nopass(self):

        self.input_dir = 'A_NEWTF_PERMFIXED'

        self.output_dir = 'A_NEWTF_proper/' + self.input_dir + '_cat1_genweight'

        # Define which index belongs to which hypothesis
        # (Should be read from MEAnalysis_cfg_heppy.py)
        self.hypo_dict = {
            "SL_2qW" : 0,
            "SL_2qW_sj" : 1,
            "SL_2qW_sj_perm" : 2,
            "SL_2qW_NewTF" : 3,
            "SL_2qW_sj_NewTF" : 4,
            "SL_2qW_sj_perm_NewTF" : 5,
            }

        # Define the background constant
        self.bkg_constant = 0.20

        # Define for which hypotheses the ROC curves should be drawn
        self.hypo_list = [
            'SL_2qW_NewTF',
            'SL_2qW_sj_NewTF',
            'SL_2qW_sj_perm_NewTF',
            #'SL_2qW',
            #'SL_2qW_sj',
            #'SL_2qW_sj_perm',
            ]

        # Selection criteria in this list are applied to all cells
        self.sel_list_for_all = [
            #'Matching_subjet_bjet>=2',
            #'Matching_subjet_bjet<=1',
            #'Matching_subjet_bjet>=0',
            'cat==1',
            #'cat!=1&&cat!=2&&cat!=3',
            ]

        self.x_key_list = [
            #'All',
            #'cat_btagH_+htt',
            #'not_cat_btagH_+htt',
            #'cat_btagH_nohtt',
            #'not_cat_btagH_nohtt',
            'pass_2qW_def',
            'nonpass_2qW_def',
            #'pass_2qW_sj',
            #'nonpass_2qW_sj',
            #'pass_2qW_sjperm',
            #'nonpass_2qW_sjperm',
            ]

        self.y_key_list = [
            'All',
            'pass_2qW_sj_01b',
            #'pass_2qW_sj_0b',
            #'pass_2qW_sj_1b',
            'pass_2qW_sj_23b',
            'nonpass_2qW_sj',
            ]





    def Cat_overview(self):

        self.input_dir = 'A_NEWTF_PERMFIXED'

        self.output_dir = self.input_dir + '_catoverview'

        # Define which index belongs to which hypothesis
        # (Should be read from MEAnalysis_cfg_heppy.py)
        self.hypo_dict = {
            "SL_2qW" : 0,
            "SL_2qW_sj" : 1,
            "SL_2qW_sj_perm" : 2,
            "SL_2qW_NewTF" : 3,
            "SL_2qW_sj_NewTF" : 4,
            "SL_2qW_sj_perm_NewTF" : 5,
            }

        # Define the background constant
        self.bkg_constant = 0.12

        # Define for which hypotheses the ROC curves should be drawn
        self.hypo_list = [
            'SL_2qW_NewTF',
            'SL_2qW_sj_NewTF',
            'SL_2qW_sj_perm_NewTF',
            #'SL_2qW',
            #'SL_2qW_sj',
            #'SL_2qW_sj_perm',
            ]

        # Selection criteria in this list are applied to all cells
        self.sel_list_for_all = [
            #'Matching_subjet_bjet>=2',
            #'Matching_subjet_bjet<2',
            #'cat==-1',
            ]

        self.x_key_list = [
            'All',
            'cat1',
            'cat2',
            'cat3',
            ]

        self.y_key_list = [
            'All',
            #'cat1',
            #'cat2',
            #'cat3',
            #'pass_2qW_sj',
            #'nonpass_2qW_sj',
            ]



    def NewTF_OldTF(self):

        self.input_dir = 'A_NEWTF_PERMFIXED'

        self.output_dir = self.input_dir + '_newtf_oldtf'

        # Define which index belongs to which hypothesis
        # (Should be read from MEAnalysis_cfg_heppy.py)
        self.hypo_dict = {
            "SL_2qW" : 0,
            "SL_2qW_sj" : 1,
            "SL_2qW_sj_perm" : 2,
            "SL_2qW_NewTF" : 3,
            "SL_2qW_sj_NewTF" : 4,
            "SL_2qW_sj_perm_NewTF" : 5,
            }

        # Define the background constant
        self.bkg_constant = 0.12

        # Define for which hypotheses the ROC curves should be drawn
        self.hypo_list = [
            #'SL_2qW_NewTF',
            'SL_2qW_sj_NewTF',
            #'SL_2qW_sj_perm_NewTF',
            #'SL_2qW',
            'SL_2qW_sj',
            #'SL_2qW_sj_perm',
            ]

        # Selection criteria in this list are applied to all cells
        self.sel_list_for_all = [
            #'Matching_subjet_bjet>=2',
            #'Matching_subjet_bjet<2',
            #'cat==-1',
            ]

        self.x_key_list = [
            'All',
            'cat1',
            'cat2',
            'cat3',
            ]

        self.y_key_list = [
            'All',
            #'cat1',
            #'cat2',
            #'cat3',
            #'pass_2qW_sj',
            #'nonpass_2qW_sj',
            ]







    ########################################
    # Functions always needed for configuration
    ########################################

    def Set_sel_dict( self ):

        self.sel_dict = {

            # Horizonal axis

            'All' : [
                ],

            'No_htt' : [
                'nhttCandidate_aftercuts<=0',
                ],

            'htt' : [
                'nhttCandidate_aftercuts>0',
                ],

            '0b_matched' : [
                'nhttCandidate_aftercuts>0',
                'Matching_event_type_number>=1',
                'Matching_event_type_number<=5',
                ],

            '1b_matched' : [
                'nhttCandidate_aftercuts>0',
                'Matching_event_type_number>=6',
                'Matching_event_type_number<=8',
                ],

            '2or3b_matched' : [
                'nhttCandidate_aftercuts>0',
                'Matching_event_type_number>=9',
                'Matching_event_type_number<=11',
                ],


            # Vertical axis


            'cat_btagH' : [
                'cat_btag==1',
                ],

            'not_cat_btagH' : [
                'cat_btag!=1',
                ],

            'cat_btagH_+htt' : [
                'cat_btag==1',
                'nhttCandidate_aftercuts>0',
                ],

            'not_cat_btagH_+htt' : [
                'cat_btag!=1',
                'nhttCandidate_aftercuts>0',
                ],

            'cat_btagH_nohtt' : [
                'cat_btag==1',
                'nhttCandidate_aftercuts<=0',
                ],

            'not_cat_btagH_nohtt' : [
                'cat_btag!=1',
                'nhttCandidate_aftercuts<=0',
                ],



            'cat1' : [
                'cat==1',
                ],

            'cat1&&cat_btag==H' : [
                'cat==1',
                'cat_btag==1',
                ],

            'cat1&&cat_btag!=H' : [
                'cat==1',
                'cat_btag<1',
                ],

            'cat2' : [
                'cat==2',
                ],

            'cat2&&cat_btag==H' : [
                'cat==2',
                'cat_btag==1',
                ],

            'cat2&&cat_btag!=H' : [
                'cat==2',
                'cat_btag<1',
                ],

            'cat3' : [
                'cat==3',
                ],

            'cat3&&cat_btag==H' : [
                'cat==3',
                'cat_btag==1',
                ],

            'cat3&&cat_btag!=H' : [
                'cat==3',
                'cat_btag<1',
                ],

            'cat12' : [
                'cat==1',
                'cat==2',
                ],

            'cat123' : [
                'cat>=1',
                'cat<=3',
                ],

            'Allcat' : [
                ],

            'notcat123' : [
                'cat!=1',
                'cat!=2',
                'cat!=3',
                ],

            'pass_2qW_sj' : [
                'nhttCandidate>=1',
                'is_sl==1',
                'n_bjets_sj>=4',
                'n_ljets_sj>=2',
                ],

            'nonpass_2qW_sj' : [
                '(nhttCandidate<1||is_sl!=1||n_bjets_sj<4||n_ljets_sj<2)',
                ],



            'pass_2qW_sj_01b' : [
                '(Matching_subjet_bjet==0||Matching_subjet_bjet==1)',
                'nhttCandidate>=1',
                'is_sl==1',
                'n_bjets_sj>=4',
                'n_ljets_sj>=2',
                ],

            'pass_2qW_sj_0b' : [
                'Matching_subjet_bjet==0',
                'nhttCandidate>=1',
                'is_sl==1',
                'n_bjets_sj>=4',
                'n_ljets_sj>=2',
                ],

            'pass_2qW_sj_1b' : [
                'Matching_subjet_bjet==1',
                'nhttCandidate>=1',
                'is_sl==1',
                'n_bjets_sj>=4',
                'n_ljets_sj>=2',
                ],

            'pass_2qW_sj_23b' : [
                '(Matching_subjet_bjet==2||Matching_subjet_bjet==3)',
                'nhttCandidate>=1',
                'is_sl==1',
                'n_bjets_sj>=4',
                'n_ljets_sj>=2',
                ],



            'pass_2qW_sjperm' : [
                'nhttCandidate>=1',
                'Matching_subjet_bjet<2',
                'is_sl==1',
                'n_bjets_sj>=4',
                'n_ljets_sj>=2',
                ],

            'nonpass_2qW_sjperm' : [
                '(nhttCandidate<1||is_sl!=1||n_bjets_sj<4||n_ljets_sj<2||Matching_subjet_bjet>=2)',
                ],

            'pass_2qW_def' : [
                'is_sl==1',
                'n_bjets>=4',
                'n_ljets>=2',
                ],

            'nonpass_2qW_def' : [
                '(is_sl!=1||n_bjets<4||n_ljets<2)',
                ],


            }

    def Set_selection_per_hypo( self, *input_args ):

        self.sel_dict_per_hypo = {}

        for hypo in self.hypo_list:
            i_hypo = self.hypo_dict[hypo]
            self.sel_dict_per_hypo[hypo] = ''

            if 'denominatornonzero' in input_args:
                self.sel_dict_per_hypo[hypo] += \
                    'mem_tth_p[{0}]+{1}*mem_ttbb_p[{0}]>0'.format( i_hypo,
                                                                   self.bkg_constant)



