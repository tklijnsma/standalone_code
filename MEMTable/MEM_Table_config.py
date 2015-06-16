class MEM_Table_configuration:
    def __init__(self):
        # Loads the dict which contains the selection strings for each category
        self.Set_sel_dict() 


        # Select one configuration here


        #self.NewTF_vs_OldTF()
        #self.NewTF_vs_OldTF_4_plots()
        #self.NoPerm_vs_Perm()

        self.Cat_changed_and_added_events()



    def Cat_changed_and_added_events(self):

        self.input_dir = 'A_NEWTF_PERM'

        self.output_dir = self.input_dir + '_test'

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

        # Define which hypothesis should be compared
        #self.compare_dict = {

            #'Perm_2qW' : ( 'SL_2qW' , 'SL_2qW_sj' ),
            #'Perm_1qW' : ( 'SL_1qW' , 'SL_1qW_sj_perm' ),

            #}

        self.hypo_list = [
            'SL_2qW_NewTF',
            'SL_2qW_sj_NewTF',
            'SL_2qW_sj_perm_NewTF',
            'SL_2qW',
            #'SL_2qW_sj_perm',
            ]

        # Selection criteria in this list are applied to all cells
        self.sel_list_for_all = [
            #'nhttCandidate_aftercuts>0',
            ]


        self.x_key_list = [
            #'All',
            'cat_btagH_+htt',
            'not_cat_btagH_+htt',
            'cat_btagH_nohtt',
            'not_cat_btagH_nohtt',
            ]

        self.y_key_list = [
            #'All',
            'cat1',
            'cat2',
            'cat3',
            ]



    def NoPerm_vs_Perm(self):

        self.input_dir = 'BMEM_PERM'

        self.output_dir = self.input_dir + '_def_vs_sj_2qW'

        # Define which index belongs to which hypothesis
        # (Should be read from MEAnalysis_cfg_heppy.py)
        self.hypo_dict = {
            "SL_2qW" : 0,
            "SL_1qW" : 1,
            "SL_2qW_sj" : 2,
            "SL_1qW_sj" : 3,
            "SL_2qW_sj_perm" : 4,
            "SL_1qW_sj_perm" : 5,
            }

        # Define the background constant
        self.bkg_constant = 0.12

        # Define which hypothesis should be compared
        self.compare_dict = {

            #'Perm_2qW' : ( 'SL_2qW' , 'SL_2qW_sj_perm' ),
            #'Perm_1qW' : ( 'SL_1qW' , 'SL_1qW_sj_perm' ),

            '2qW' : ( 'SL_2qW' , 'SL_2qW_sj' ),

            }

        # Selection criteria in this list are applied to all cells
        self.sel_list_for_all = [
            #'nhttCandidate_aftercuts>0',
            ]


        # To keep order consistent and easily turn categories on or off

        self.x_key_list = [ 'All', 'No_htt', 'htt',
                       '0b_matched', '1b_matched', '2or3b_matched' ]
        self.y_key_list = [ 'NA', 'Cat1', 'Cat2', 'Cat3' ]

        #self.x_key_list = [ 'No_htt', 'htt' ]
        #self.y_key_list = [ 'Cat1', 'AllCat' ]



    def NewTF_vs_OldTF_4_plots(self):

        #self.input_dir = 'BMEM_V11_SB_FULL'
        #self.input_dir = 'BMEM_V11_SB_FULL_njetsbranches_S5changed'
        self.input_dir = 'BMEM_NEWTF'

        self.output_dir = self.input_dir + '_output_test'

        # Define which index belongs to which hypothesis
        # (Should be read from MEAnalysis_cfg_heppy.py)
        self.hypo_dict = {
            "SL_2qW" : 0,
            "SL_1qW" : 1,
            "SL_2qW_sj" : 2,
            "SL_1qW_sj" : 3,
            "SL_2qW_sj_perm" : 4,
            "SL_1qW_sj_perm" : 5,
            "SL_2qW_NewTF" : 4,
            "SL_1qW_NewTF" : 5,
            "SL_2qW_sj_NewTF" : 6,
            "SL_1qW_sj_NewTF" : 7,
            }

        # Define the background constant
        self.bkg_constant = 0.12

        # Define which hypothesis should be compared
        self.compare_dict = {

            #'TFs' : ( 'SL_2qW' , 'SL_2qW_NewTF' ),
            'TFs_sj' : ( 'SL_2qW_sj' , 'SL_2qW_sj_NewTF' ),

            }

        # Selection criteria in this list are applied to all cells
        self.sel_list_for_all = [
            #'nhttCandidate_aftercuts>0',
            ]


        # To keep order consistent and easily turn categories on or off

        #self.x_key_list = [ 'All', 'No_htt', 'htt',
        #               '0b_matched', '1b_matched', '2or3b_matched' ]
        #self.y_key_list = [ 'NA', 'Cat1', 'Cat2', 'Cat3', 'Cat123' ]

        self.x_key_list = [ 'All', 'htt' ]
        self.y_key_list = [ 'All' ]



    def NewTF_vs_OldTF(self):

        #self.input_dir = 'BMEM_V11_SB_FULL'
        #self.input_dir = 'BMEM_V11_SB_FULL_njetsbranches_S5changed'
        self.input_dir = 'BMEM_NEWTF'

        self.output_dir = self.input_dir + '_output_test'

        # Define which index belongs to which hypothesis
        # (Should be read from MEAnalysis_cfg_heppy.py)
        self.hypo_dict = {
            "SL_2qW" : 0,
            "SL_1qW" : 1,
            "SL_2qW_sj" : 2,
            "SL_1qW_sj" : 3,
            "SL_2qW_sj_perm" : 4,
            "SL_1qW_sj_perm" : 5,
            "SL_2qW_NewTF" : 4,
            "SL_1qW_NewTF" : 5,
            "SL_2qW_sj_NewTF" : 6,
            "SL_1qW_sj_NewTF" : 7,
            }

        # Define the background constant
        self.bkg_constant = 0.12

        # Define which hypothesis should be compared
        self.compare_dict = {

            'OldTF_2qW' : ( 'SL_2qW' , 'SL_2qW_sj' ),
            'OldTF_1qW' : ( 'SL_1qW' , 'SL_1qW_sj' ),

            #'NewTF_2qW' : ( 'SL_2qW_NewTF' , 'SL_2qW_sj_NewTF' ),
            #'NewTF_1qW' : ( 'SL_1qW_NewTF' , 'SL_1qW_sj_NewTF' ),

            }

        # Selection criteria in this list are applied to all cells
        self.sel_list_for_all = [
            #'nhttCandidate_aftercuts>0',
            ]


        # To keep order consistent and easily turn categories on or off

        #self.x_key_list = [ 'All', 'No_htt', 'htt',
        #               '0b_matched', '1b_matched', '2or3b_matched' ]
        #self.y_key_list = [ 'NA', 'Cat1', 'Cat2', 'Cat3', 'Cat123' ]

        self.x_key_list = [ 'No_htt', 'htt' ]
        self.y_key_list = [ 'Cat1', 'AllCat' ]




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

            }
