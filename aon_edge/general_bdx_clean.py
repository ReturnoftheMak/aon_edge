# %% Package Imports

import pandas as pd



# %% Global vars, probably best to define in main

mappings = {'claim':r'\\svrtcs04\Syndicate Data\Actuarial\Pricing\2_Account_Pricing\NFS_Edge\Knowledge\Data_Received\Monthly\_ColumnMapping\claim_WITHACTIONS.xlsx',
            'risk':r'\\svrtcs04\Syndicate Data\Actuarial\Pricing\2_Account_Pricing\NFS_Edge\Knowledge\Data_Received\Monthly\_ColumnMapping\risk_WITHACTIONS.xlsx',
            'premium':r'\\svrtcs04\Syndicate Data\Actuarial\Pricing\2_Account_Pricing\NFS_Edge\Knowledge\Data_Received\Monthly\_ColumnMapping\premium_WITHACTIONS.xlsx'}


# %% Lets try to make use of inheritance here

class BdxCleaner(object):
    def __init__(self, bdx_type, bdx_file, mappings):
        self.bdx_type = bdx_type
        self.file = bdx_file
        self.mappings = mappings


    def get_mapping(self):
        """Get a dictionary of column mapping, and a list of the column subset 
        that we want to retain.
        """

        # Read in the mapping file
        df_claim_mapping = pd.read_excel(self.mappings[self.bdx_type])

        keys = df_claim_mapping.ColumnNames
        values = df_claim_mapping.Rename

        mapping_dict = dict(zip(keys, values))

        return mapping_dict


    def basic_cleaning(self):
        """Cleaning steps to be applied to any bordereaux
        """

        # Lookup the header row to use, maybe we shouldn't hard code these
        var_dict = {'claim':2,'risk':0,'premium':0}

        # Read the excel in with specified vars
        df = pd.read_excel(self.file, sheet_name=0, header=var_dict[self.bdx_type])

        # Map cols using the dictionary
        df = df.rename(columns=self.get_mapping())
        df = df[[col for col in df.columns if type(col) is not float]]

        # GDPR drop fields
        df = df.drop(labels=['Name_Claimant', 'Name_Insured'], axis=1)

        # Drop any subtotal rows
        df.dropna(axis=0, how='any', subset='ID_Claim', inplace=True)
    


