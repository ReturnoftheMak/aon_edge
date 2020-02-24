# %% Package Imports

import pandas as pd
from general_bdx_clean import BdxCleaner, mappings, header_dict, id_dict


# %% Define class for premium

class PremiumBdxCleaner(BdxCleaner):
    """Used to clean AON Edge Premium bordereaux, inherits methods from BdxCleaner
    """
    def __init__(self, bdx_file, mappings):
        self.file = bdx_file
        self.mappings = mappings
        self.bdx_type = 'premium'
        self.dataframe = self.basic_cleaning()
    

    def funcname(self, parameter_list):
        pass


    def funcname2(self, parameter_list):
        pass


    def drop_gdpr_fields(self):
        """Drop GDPR sensitive fields
        """
        # May need to test if these are in bdx first
        # self.dataframe = self.dataframe.drop(labels=[''], axis=1)


