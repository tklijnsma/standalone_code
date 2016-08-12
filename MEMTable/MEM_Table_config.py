class MEM_Table_configuration:
    def __init__(self):

        # Loads the dict which contains the selection strings for each category
        self.Set_sel_dict() 

        self.Draw_plots = True


        # ==========================================
        # Select one configuration here

        #self.Rev_Phys_Restructured()
        #self.Rev_Phys_Unrestructered()
        self.Rev_Phys_Q1()

        #self.V12_1Q()
        #self.V12_restructured()
        #self.V12_test()
        #self.Oldcat_SJcat_pass_nopass()
        #self.Cat_overview()
        #self.NewTF_OldTF()

        # ==========================================


        # Set the selection string so that denominator > 0
        self.Set_selection_per_hypo(
            'denominatornonzero'
            )

        # Specify to use genweights
        self.UseGenWeights = False

        self.UsePhysical = True
        self.sigma_p = { 'sig' : 0.294 , 'bkg' : 425 }
        self.total_count = { 'sig' : 3784705.0, 'bkg' : 36786844.0 }
        self.target_lumi = 10000.0
        self.genWeight_norm = { 'sig' : 1.0, 'bkg' : 6384.0 }

        # Number of bins in mem ratio hist
        self.n_mem_hist_bins = 12
        #self.n_mem_hist_bins = 100



    ########################################
    # Different configurations
    ########################################




    def Rev_Phys_Unrestructered(self):

        self.input_dir = 'V12/V12_FULL_v3'

        #self.output_dir = self.input_dir + '_nocut_pickle_spec_all'
        self.output_dir = 'Rev_phys/Unrestructured/ETN17'

        self.sig_input_root_fn = 'tth_V12_13tev.root'
        self.bkg_input_root_fn = 'ttjets_V12_13tev.root'

        self.Store_table_as_picke = True

        # Define which index belongs to which hypothesis
        # (Should be read from MEAnalysis_cfg_heppy.py)
        self.hypo_dict = {
            "SL_2qW" : 0,
            "SL_2qW_NewTF" : 1,
            "SL_2qW_sj_NewTF" : 2,
            "SL_2qW_sj_perm_NewTF" : 3,
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
            #'Matching_subjet_bjet<=1',
            #'Matching_subjet_bjet>=0',

            #'cat==1',

            # Working point 1
            #'httCandidate_AC_fRec<0.13',
            #'httCandidate_AC_n_subjettiness<0.54',

            # Working point 3
            #'httCandidate_AC_fRec<0.18',
            #'httCandidate_AC_n_subjettiness<0.73',

            # Working point 5
            #'httCandidate_AC_fRec<0.13',
            #'httCandidate_AC_n_subjettiness<0.58',
            #'httCandidate_AC_delRopt>=-0.74',
            #'httCandidate_AC_delRopt<=0.15',

            # Working point 6
            #'httCandidate_AC_fRec<0.14',
            #'httCandidate_AC_n_subjettiness<0.67',
            #'httCandidate_AC_delRopt>=-0.49',
            #'httCandidate_AC_delRopt<=0.16',

            # Working point 7
            #'httCandidate_AC_fRec<0.19',
            #'httCandidate_AC_n_subjettiness<0.78',
            #'httCandidate_AC_delRopt>=-0.67',
            #'httCandidate_AC_delRopt<=0.25',

            # Working point 8
            #'httCandidate_AC_delRopt>=-0.53',
            #'httCandidate_AC_delRopt<=0.38',

            # Working point
            #'httCandidate_AC_fRec<0.12',
            #'httCandidate_AC_n_subjettiness<0.6',

            #'httCandidate_AC_bbtag<-0.5',
            

            ]

        self.x_key_list = [

            #'cat_btagH_+htt',
            #'not_cat_btagH_+htt',
            #'cat_btagH_nohtt',
            #'not_cat_btagH_nohtt',

            'All',
            'pass_2qW_def',
            'nonpass_2qW_def',

            #'pass_def',
            #'nonpass_def',

            #'WPtight1',
            #'pass_2qW_def&&WPtight1',
            #'nonpass_2qW_def&&WPtight1',

            #'pass_2qW_sj',
            #'nonpass_2qW_sj',
            #'pass_2qW_sjperm',
            #'nonpass_2qW_sjperm',
            ]

        self.y_key_list = [
            #'All',

            #'ETN7',
            #'ETN9',
            #'ETN16',
            'ETN17',

            ]

    def Rev_Phys_Restructured(self):

        self.input_dir = 'V12RESTRUCT/V12_v5'

        #self.output_dir = self.input_dir + '_HC_nocut'
        self.output_dir = 'Rev_phys/Restructured/higgs_1b'

        self.sig_input_root_fn = 'tth_V12_13tev.root'
        self.bkg_input_root_fn = 'ttjets_V12_13tev.root'

        self.Store_table_as_picke = True

        # Define which index belongs to which hypothesis
        # (Should be read from MEAnalysis_cfg_heppy.py)
        self.hypo_dict = {
            "SL_2qW" : 0,
            "SL_2qW_NewTF" : 1,
            "SL_2qW_sj_NewTF" : 2,
            "SL_2qW_sj_perm_NewTF" : 3,
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
            #'n_excluded_bjets<2',
            'n_excluded_bjets==1',
            
            # Working point 1
            #'topCandidate_fRec<0.13',
            #'topCandidate_n_subjettiness<0.54',

            # Working point 2
            #'topCandidate_fRec<0.14',
            #'topCandidate_n_subjettiness<0.62',

            # Working point 3
            #'topCandidate_fRec<0.18',
            #'topCandidate_n_subjettiness<0.73',

            # Working point 4
            #'topCandidate_fRec<0.39',
            #'topCandidate_n_subjettiness<0.87',

            # Working point 5
            #'topCandidate_fRec<0.13',
            #'topCandidate_n_subjettiness<0.58',
            #'topCandidate_delRopt>=-0.74',
            #'topCandidate_delRopt<=0.15',

            # Working point 6
            #'topCandidate_fRec<0.14',
            #'topCandidate_n_subjettiness<0.67',
            #'topCandidate_delRopt>=-0.49',
            #'topCandidate_delRopt<=0.16',

            # Working point 7
            #'topCandidate_fRec<0.19',
            #'topCandidate_n_subjettiness<0.78',
            #'topCandidate_delRopt>=-0.67',
            #'topCandidate_delRopt<=0.25',

            # Working point 8
            #'topCandidate_delRopt>=-0.53',
            #'topCandidate_delRopt<=0.38',


            ]

        self.x_key_list = [

            'All',
            'pass_2qW_def',
            'nonpass_2qW_def',

            ]

        self.y_key_list = [

            'All',
            #'0excluded',
            #'1excluded',
            #'23excluded',

            'higgs_nsbb',
            'higgs_bb1',
            #'higgs_bb2',
            'higgs_ns1',
            #'higgs_ns2',
            ]



    def Rev_Phys_Q1(self):

        self.input_dir = 'V12RESTRUCT/V12_1Q'

        #self.output_dir = self.input_dir + '/V12_1Q/V12_1Q_HC_nocut'
        self.output_dir = 'Rev_phys/Restructured/Q1_WP3'

        self.sig_input_root_fn = 'tth_V12_13tev.root'
        self.bkg_input_root_fn = 'ttjets_V12_13tev.root'

        self.Store_table_as_picke = True

        # Define which index belongs to which hypothesis
        # (Should be read from MEAnalysis_cfg_heppy.py)
        self.hypo_dict = {
            "SL_1qW" : 0,
            "SL_1qW_NewTF" : 1,
            "SL_1qW_sj_NewTF" : 2,
            "SL_1qW_sj_perm_NewTF" : 3,
            }

        # Define the background constant
        self.bkg_constant = 0.12

        # Define for which hypotheses the ROC curves should be drawn
        self.hypo_list = [
            'SL_1qW_NewTF',
            'SL_1qW_sj_NewTF',
            'SL_1qW_sj_perm_NewTF',
            ]

        # Selection criteria in this list are applied to all cells
        self.sel_list_for_all = [
            #'n_excluded_bjets<2',
            #'n_excluded_bjets==1',
            
            # Working point 1
            #'topCandidate_fRec<0.13',
            #'topCandidate_n_subjettiness<0.54',

            # Working point 2
            #'topCandidate_fRec<0.14',
            #'topCandidate_n_subjettiness<0.62',

            # Working point 3
            'topCandidate_fRec<0.18',
            'topCandidate_n_subjettiness<0.73',

            # Working point 4
            #'topCandidate_fRec<0.39',
            #'topCandidate_n_subjettiness<0.87',

            # Working point 5
            #'topCandidate_fRec<0.13',
            #'topCandidate_n_subjettiness<0.58',
            #'topCandidate_delRopt>=-0.74',
            #'topCandidate_delRopt<=0.15',

            # Working point 6
            #'topCandidate_fRec<0.14',
            #'topCandidate_n_subjettiness<0.67',
            #'topCandidate_delRopt>=-0.49',
            #'topCandidate_delRopt<=0.16',

            # Working point 7
            #'topCandidate_fRec<0.19',
            #'topCandidate_n_subjettiness<0.78',
            #'topCandidate_delRopt>=-0.67',
            #'topCandidate_delRopt<=0.25',

            # Working point 8
            #'topCandidate_delRopt>=-0.53',
            #'topCandidate_delRopt<=0.38',

            ]

        self.x_key_list = [
            'All',
            'pass_1qW_def',
            'nonpass_1qW_def',
            ]

        self.y_key_list = [
            'All',
            '0excluded',
            '1excluded',
            '23excluded',
            ]





    # Unrevised configs

    def V12_1Q(self):

        self.input_dir = 'V12RESTRUCT/V12_1Q'

        self.output_dir = self.input_dir + '/V12_1Q/V12_1Q_HC_nocut'

        self.sig_input_root_fn = 'tth_V12_13tev.root'
        self.bkg_input_root_fn = 'ttjets_V12_13tev.root'

        self.Store_table_as_picke = True

        # Define which index belongs to which hypothesis
        # (Should be read from MEAnalysis_cfg_heppy.py)
        self.hypo_dict = {
            "SL_1qW" : 0,
            "SL_1qW_NewTF" : 1,
            "SL_1qW_sj_NewTF" : 2,
            "SL_1qW_sj_perm_NewTF" : 3,
            }

        # Define the background constant
        self.bkg_constant = 0.12

        # Define for which hypotheses the ROC curves should be drawn
        self.hypo_list = [
            'SL_1qW_NewTF',
            'SL_1qW_sj_NewTF',
            'SL_1qW_sj_perm_NewTF',
            ]

        # Selection criteria in this list are applied to all cells
        self.sel_list_for_all = [
            #'n_excluded_bjets<2',
            #'n_excluded_bjets==1',
            
            # Working point 1
            #'topCandidate_fRec<0.13',
            #'topCandidate_n_subjettiness<0.54',

            # Working point 2
            #'topCandidate_fRec<0.14',
            #'topCandidate_n_subjettiness<0.62',

            # Working point 3
            #'topCandidate_fRec<0.18',
            #'topCandidate_n_subjettiness<0.73',

            # Working point 4
            #'topCandidate_fRec<0.39',
            #'topCandidate_n_subjettiness<0.87',

            # Working point 5
            #'topCandidate_fRec<0.13',
            #'topCandidate_n_subjettiness<0.58',
            #'topCandidate_delRopt>=-0.74',
            #'topCandidate_delRopt<=0.15',

            # Working point 6
            #'topCandidate_fRec<0.14',
            #'topCandidate_n_subjettiness<0.67',
            #'topCandidate_delRopt>=-0.49',
            #'topCandidate_delRopt<=0.16',

            # Working point 7
            #'topCandidate_fRec<0.19',
            #'topCandidate_n_subjettiness<0.78',
            #'topCandidate_delRopt>=-0.67',
            #'topCandidate_delRopt<=0.25',

            # Working point 8
            #'topCandidate_delRopt>=-0.53',
            #'topCandidate_delRopt<=0.38',

            ]

        self.x_key_list = [
            'All',
            'pass_1qW_def',
            'nonpass_1qW_def',
            ]

        self.y_key_list = [
            'All',
            '0excluded',
            '1excluded',
            '23excluded',

            #'higgs_nsbb',
            #'higgs_bb1',
            #'higgs_bb2',
            #'higgs_ns1',
            #'higgs_ns2',
            ]



    def V12_restructured(self):

        self.input_dir = 'V12RESTRUCT/V12_v5'

        self.output_dir = self.input_dir + '_HC_nocut'

        self.sig_input_root_fn = 'tth_V12_13tev.root'
        self.bkg_input_root_fn = 'ttjets_V12_13tev.root'

        self.Store_table_as_picke = True

        # Define which index belongs to which hypothesis
        # (Should be read from MEAnalysis_cfg_heppy.py)
        self.hypo_dict = {
            "SL_2qW" : 0,
            "SL_2qW_NewTF" : 1,
            "SL_2qW_sj_NewTF" : 2,
            "SL_2qW_sj_perm_NewTF" : 3,
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
            #'n_excluded_bjets<2',
            #'n_excluded_bjets==1',
            
            # Working point 1
            #'topCandidate_fRec<0.13',
            #'topCandidate_n_subjettiness<0.54',

            # Working point 2
            #'topCandidate_fRec<0.14',
            #'topCandidate_n_subjettiness<0.62',

            # Working point 3
            #'topCandidate_fRec<0.18',
            #'topCandidate_n_subjettiness<0.73',

            # Working point 4
            #'topCandidate_fRec<0.39',
            #'topCandidate_n_subjettiness<0.87',

            # Working point 5
            #'topCandidate_fRec<0.13',
            #'topCandidate_n_subjettiness<0.58',
            #'topCandidate_delRopt>=-0.74',
            #'topCandidate_delRopt<=0.15',

            # Working point 6
            #'topCandidate_fRec<0.14',
            #'topCandidate_n_subjettiness<0.67',
            #'topCandidate_delRopt>=-0.49',
            #'topCandidate_delRopt<=0.16',

            # Working point 7
            #'topCandidate_fRec<0.19',
            #'topCandidate_n_subjettiness<0.78',
            #'topCandidate_delRopt>=-0.67',
            #'topCandidate_delRopt<=0.25',

            # Working point 8
            #'topCandidate_delRopt>=-0.53',
            #'topCandidate_delRopt<=0.38',


            ]

        self.x_key_list = [

            #'cat_btagH_+htt',
            #'not_cat_btagH_+htt',
            #'cat_btagH_nohtt',
            #'not_cat_btagH_nohtt',

            'All',
            'pass_2qW_def',
            'nonpass_2qW_def',

            #'WPtight1',
            #'pass_2qW_def&&WPtight1',
            #'nonpass_2qW_def&&WPtight1',

            #'pass_2qW_sj',
            #'nonpass_2qW_sj',
            #'pass_2qW_sjperm',
            #'nonpass_2qW_sjperm',
            ]

        self.y_key_list = [

            'All',
            #'0excluded',
            #'1excluded',
            #'23excluded',
            #'higgspresent',
            #'not_higgspresent',
            #'very_not_higgspresent',

            'higgs_nsbb',
            'higgs_bb1',
            'higgs_bb2',
            'higgs_ns1',
            'higgs_ns2',
            ]




    def V12_test(self):

        self.input_dir = 'V12/V12_FULL_v3'

        self.output_dir = self.input_dir + '_nocut_pickle_spec_all'

        self.sig_input_root_fn = 'tth_V12_13tev.root'
        self.bkg_input_root_fn = 'ttjets_V12_13tev.root'

        self.Store_table_as_picke = True

        # Define which index belongs to which hypothesis
        # (Should be read from MEAnalysis_cfg_heppy.py)
        self.hypo_dict = {
            "SL_2qW" : 0,
            "SL_2qW_NewTF" : 1,
            "SL_2qW_sj_NewTF" : 2,
            "SL_2qW_sj_perm_NewTF" : 3,
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
            #'Matching_subjet_bjet<=1',
            #'Matching_subjet_bjet>=0',

            #'cat==1',

            # Working point 1
            #'httCandidate_AC_fRec<0.13',
            #'httCandidate_AC_n_subjettiness<0.54',

            # Working point 3
            #'httCandidate_AC_fRec<0.18',
            #'httCandidate_AC_n_subjettiness<0.73',

            # Working point 5
            #'httCandidate_AC_fRec<0.13',
            #'httCandidate_AC_n_subjettiness<0.58',
            #'httCandidate_AC_delRopt>=-0.74',
            #'httCandidate_AC_delRopt<=0.15',

            # Working point 6
            #'httCandidate_AC_fRec<0.14',
            #'httCandidate_AC_n_subjettiness<0.67',
            #'httCandidate_AC_delRopt>=-0.49',
            #'httCandidate_AC_delRopt<=0.16',

            # Working point 7
            #'httCandidate_AC_fRec<0.19',
            #'httCandidate_AC_n_subjettiness<0.78',
            #'httCandidate_AC_delRopt>=-0.67',
            #'httCandidate_AC_delRopt<=0.25',

            # Working point 8
            #'httCandidate_AC_delRopt>=-0.53',
            #'httCandidate_AC_delRopt<=0.38',

            # Working point
            #'httCandidate_AC_fRec<0.12',
            #'httCandidate_AC_n_subjettiness<0.6',

            #'httCandidate_AC_bbtag<-0.5',
            

            ]

        self.x_key_list = [

            #'cat_btagH_+htt',
            #'not_cat_btagH_+htt',
            #'cat_btagH_nohtt',
            #'not_cat_btagH_nohtt',

            'All',
            #'pass_2qW_def',
            #'nonpass_2qW_def',

            #'pass_def',
            #'nonpass_def',

            #'WPtight1',
            #'pass_2qW_def&&WPtight1',
            #'nonpass_2qW_def&&WPtight1',

            #'pass_2qW_sj',
            #'nonpass_2qW_sj',
            #'pass_2qW_sjperm',
            #'nonpass_2qW_sjperm',
            ]

        self.y_key_list = [
            'All',
            #'htt',
            #'No_htt',
            #'pass_2qW_sj_01b',
            #'pass_2qW_sj_0b',
            #'pass_2qW_sj_1b',
            #'pass_2qW_sj_23b',
            #'nonpass_2qW_sj',

            #'ETN1',
            #'ETN2',
            #'ETN3',
            #'ETN4',
            #'ETN5',
            #'ETN6',
            #'ETN7',
            #'ETN8',
            #'ETN9',

            #'ETN16',
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


            #'0b_matched' : [
            #    'nhttCandidate_aftercuts>0',
            #    'Matching_event_type_number>=1',
            #    'Matching_event_type_number<=5',
            #    ],

            #'1b_matched' : [
            #    'nhttCandidate_aftercuts>0',
            #    'Matching_event_type_number>=6',
            #    'Matching_event_type_number<=8',
            #    ],

            #'2or3b_matched' : [
            #    'nhttCandidate_aftercuts>0',
            #    'Matching_event_type_number>=9',
            #    'Matching_event_type_number<=11',
            #    ],

            'ETN1' : [
                'Matching_event_type_number==1',
                ],
            'ETN2' : [
                'Matching_event_type_number==2',
                ],
            'ETN3' : [
                'Matching_event_type_number==3',
                ],
            'ETN4' : [
                'Matching_event_type_number==4',
                ],
            'ETN5' : [
                'Matching_event_type_number==5',
                ],
            'ETN6' : [
                'Matching_event_type_number==6',
                ],
            'ETN7' : [
                'Matching_event_type_number==7',
                ],
            'ETN8' : [
                'Matching_event_type_number==8',
                ],
            'ETN9' : [
                'Matching_event_type_number==9',
                ],
            'ETN16' : [
                'Matching_event_type_number>=1',
                'Matching_event_type_number<=6',
                ],
            'ETN17' : [
                'Matching_event_type_number>=1',
                'Matching_event_type_number<=7',
                ],

            'WPtight1' : [
                'httCandidate_AC_fRec<0.12',
                'httCandidate_AC_n_subjettiness<0.6',
                ],

            'WPtight2' : [
                'httCandidate_AC_fRec<0.10',
                'httCandidate_AC_n_subjettiness<0.5',
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
                'nhttCandidate_aftercuts>0',
                'is_sl==1',
                'n_bjets>=4',
                'n_ljets>=2',
                ],

            'nonpass_2qW_def' : [
                'nhttCandidate_aftercuts>0&&(is_sl!=1||n_bjets<4||n_ljets<2)',
                ],

            'pass_1qW_def' : [
                'nhttCandidate_aftercuts>0',
                'is_sl==1',
                'n_bjets>=4',
                'n_ljets>=1',
                ],

            'nonpass_1qW_def' : [
                'nhttCandidate_aftercuts>0&&(is_sl!=1||n_bjets<4||n_ljets<1)',
                ],


            'higgspresent' : [
                'higgsCandidate_bbtag[0]>0.5',
                ],


            'higgs_bb1' : [
                'higgsCandidate_bbtag[0]>0.0',
                ],


            'higgs_bb2' : [
                'higgsCandidate_bbtag[0]>0.5',
                ],

            'higgs_ns1' : [
                'higgsCandidate_n_subjettiness[0]<0.6',
                ],

            'higgs_ns2' : [
                'higgsCandidate_n_subjettiness[0]<0.3',
                ],

            'higgs_nsbb' : [
                'higgsCandidate_bbtag[0]>0.0',
                'higgsCandidate_n_subjettiness[0]<0.5',
                ],

            'not_higgspresent' : [
                '(nhiggsCandidate==0||(nhiggsCandidate>0&&higgsCandidate_bbtag[0]<0.5))',
                ],

            'very_not_higgspresent' : [
                'higgsCandidate_bbtag[0]<-0.2',
                ],


            'pass_def' : [
                'is_sl==1',
                'n_bjets>=4',
                'n_ljets>=2',
                ],

            'nonpass_def' : [
                '(is_sl!=1||n_bjets<4||n_ljets<2)',
                ],

            '0excluded' : [
                'n_excluded_bjets==0',
                ],

            '1excluded' : [
                'n_excluded_bjets==1',
                ],

            '23excluded' : [
                'n_excluded_bjets>=2',
                ],

            }

    def Set_selection_per_hypo( self, *input_args ):

        self.sel_dict_per_hypo = {}

        for hypo in self.hypo_list:
            i_hypo = self.hypo_dict[hypo]
            self.sel_dict_per_hypo[hypo] = '1==1'

            if 'denominatornonzero' in input_args:
                self.sel_dict_per_hypo[hypo] += \
                    '&&mem_tth_p[{0}]+{1}*mem_ttbb_p[{0}]>0'.format( i_hypo,
                                                                   self.bkg_constant)



