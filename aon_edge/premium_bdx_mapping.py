# %% Package Imports

import pandas as pd
import openpyxl
from general_bdx_clean import BdxCleaner, mappings, header_dict, id_dict


# %% Define class for premium

class PremiumBdxCleaner(BdxCleaner):
    """Used to clean AON Edge Premium bordereaux, inherits methods from BdxCleaner
    """
    def __init__(self, bdx_file, mappings, headers, IDs, sheet_dict):
        self.file = bdx_file
        self.mappings = mappings
        self.headers = headers
        self.IDs = IDs
        self.sheets = sheet_dict
        self.bdx_type = 'premium'
        self.xl_file = openpyxl.load_workbook(self.file, read_only=True, data_only=True)
        self.dataframe = self.basic_cleaning()
        self.test_var = True


    def funcname(self, parameter_list):
        pass


    def funcname2(self, parameter_list):
        pass


    def drop_gdpr_fields(self):
        """Drop GDPR sensitive fields
        """
        # May need to test if these are in bdx first
        # self.dataframe = self.dataframe.drop(labels=[''], axis=1)


