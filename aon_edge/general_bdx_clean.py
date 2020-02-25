# %% Package Imports

import pandas as pd
from sql_connection import sql_connection


# %% Global vars, probably best to define in main

mappings = {'claim':r'\\svrtcs04\Syndicate Data\Actuarial\Pricing\2_Account_Pricing\NFS_Edge\Knowledge\Data_Received\Monthly\_ColumnMapping\claim_WITHACTIONS.xlsx',
            'risk':r'\\svrtcs04\Syndicate Data\Actuarial\Pricing\2_Account_Pricing\NFS_Edge\Knowledge\Data_Received\Monthly\_ColumnMapping\risk_WITHACTIONS.xlsx',
            'premium':r'\\svrtcs04\Syndicate Data\Actuarial\Pricing\2_Account_Pricing\NFS_Edge\Knowledge\Data_Received\Monthly\_ColumnMapping\premium_WITHACTIONS.xlsx'}

header_dict = {'claim':2,'risk':0,'premium':0}

id_dict = {'claim':'ID_Claim', 'risk':'ID_PolicyStem', 'premium':'ID_PolicyStem'}


# %% Lets try to make use of inheritance here

class BdxCleaner(object):
    """Base Class for cleaning bordereaux for AON Edge
    """
    def __init__(self, bdx_file, mappings, headers, IDs, bdx_type):
        self.file = bdx_file
        self.mappings = mappings
        self.headers = headers
        self.IDs = IDs
        self.bdx_type = bdx_type
        self.dataframe = self.basic_cleaning()


    def get_mapping(self):
        """Get a dictionary of column mapping, and a list of the column subset 
        that we want to retain.
        """

        # Read in the mapping file
        df_mapping = pd.read_excel(self.mappings[self.bdx_type])

        keys = df_mapping.ColumnNames
        values = df_mapping.Rename

        mapping_dict = dict(zip(keys, values))

        return mapping_dict


    def basic_cleaning(self):
        """Cleaning steps to be applied to any bordereaux, utilising mappings.
        Reads in the excel file, taking the first sheet only, with a header row based on type of bdx.
        Then utilises the column mapping to rename the columns and drop any columns which were not mapped.
        Lastly the function drops any 
        """

        # Read the excel in with specified vars
        df = pd.read_excel(self.file, sheet_name=0, header=self.headers[self.bdx_type])

        # Map cols using the dictionary
        df = df.rename(columns=self.get_mapping())
        df = df[[col for col in df.columns if type(col) is not float]]

        # Drop any subtotal rows
        df.dropna(axis=0, how='any', subset=[self.IDs[self.bdx_type]], inplace=True)

        return df
    

    def username_input(self):
        """Add in a username for whoever ran the code
        """
        from getpass import getuser
        user = getuser()
        self.dataframe['Updated_Name'] = user


    def date_code_run(self):
        """Adding in a run date for the df.
        May need to be done just prior to upload after all checks have passed
        """
        from datetime import date
        today = date.today()
        self.dataframe['Updated_Date'] = today


    def add_file_name(self):
        """Add in the name of the file into the dataframe
        """
        from pathlib import Path
        file_name = Path(self.file).stem
        bdx_month = Path(self.file).parent.parent.stem
        self.dataframe['Updated_Source'] = file_name
        self.dataframe['Bordereau_Month'] = bdx_month


    def export_to_sql(self, df, server_name, database_name, table_name):
        """Exports the cleaned dataframe to sql, replacing the old version if existing
        """

        sql_con = sql_connection(server_name, database_name)

        df.to_sql(table_name, sql_con, if_exists='replace')
    

    #


