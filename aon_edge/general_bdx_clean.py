# %% Package Imports

import pandas as pd
from sql_connection import sql_connection


# %% Global vars, probably best to define in main

mappings = {'claim':r'\\svrtcs04\Syndicate Data\Actuarial\Pricing\2_Account_Pricing\NFS_Edge\Knowledge\Data_Received\Monthly\_ColumnMapping\claim_WITHACTIONS.xlsx',
            'risk':r'\\svrtcs04\Syndicate Data\Actuarial\Pricing\2_Account_Pricing\NFS_Edge\Knowledge\Data_Received\Monthly\_ColumnMapping\risk_WITHACTIONS.xlsx',
            'premium':r'\\svrtcs04\Syndicate Data\Actuarial\Pricing\2_Account_Pricing\NFS_Edge\Knowledge\Data_Received\Monthly\_ColumnMapping\premium_WITHACTIONS.xlsx'}


# %% Lets try to make use of inheritance here

class BdxCleaner(object):
    """Base Class for cleaning bordereaux for AON Edge
    """
    def __init__(self, bdx_file, mappings, bdx_type):
        self.file = bdx_file
        self.mappings = mappings
        self.bdx_type = bdx_type
        self.dataframe = self.basic_cleaning()


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
        """Cleaning steps to be applied to any bordereaux, utilising mappings
        """

        # Lookup the header row to use, maybe we shouldn't hard code these
        var_dict = {'claim':2,'risk':0,'premium':0}

        # Read the excel in with specified vars
        df = pd.read_excel(self.file, sheet_name=0, header=var_dict[self.bdx_type])

        # Map cols using the dictionary
        df = df.rename(columns=self.get_mapping())
        df = df[[col for col in df.columns if type(col) is not float]]

        # Drop any subtotal rows
        df.dropna(axis=0, how='any', subset='ID_Claim', inplace=True)

        return df


    def export_to_sql(self, df, server_name, database_name, table_name):
        """Exports the cleaned dataframe to sql, replacing the old version if existing
        """

        sql_con = sql_connection(server_name, database_name)

        df.to_sql(table_name, sql_con, if_exists='replace')
    

    #


