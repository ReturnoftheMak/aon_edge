# %% Package Imports

import pandas as pd
from general_bdx_clean import BdxCleaner


# %% Set Params

mapping_file = r'\\svrtcs04\Syndicate Data\Actuarial\Pricing\2_Account_Pricing\NFS_Edge\Knowledge\Data_Received\Monthly\_ColumnMapping\premium_WITHACTIONS.xlsx'


# %% Cleaning function for risk bordereaux

def premium_bdx_clean(file, mapping_dict):
    """Read in file, change column headers and output only the required cols
    """

    df = pd.read_excel(file, sheet_name = 0, header=0)

    df = df.rename(columns=mapping_dict)

    df = df[[col for col in df.columns if type(col) is not float]]

    # Drop any subtotal rows
    df.dropna(axis=0, how='any', subset='ID_PolicyStem', inplace=True)

    #


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


