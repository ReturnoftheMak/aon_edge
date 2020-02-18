# %% Package imports

import pandas as pd


# %% Mapping file location

mapping_file = r'\\svrtcs04\Syndicate Data\Actuarial\Pricing\2_Account_Pricing\NFS_Edge\Knowledge\Data_Received\Monthly\_ColumnMapping\claim_WITHACTIONS.xlsx'


# %% Mapping function, can be used for all bdx types

def get_mapping(mapping_file):
    """Get a dictionary of column mapping, and a list of the column subset that we want to retain.
    """

    df_claim_mapping = pd.read_excel(mapping_file)

    keys = df_claim_mapping.ColumnNames
    values = df_claim_mapping.Rename

    mapping_dict = dict(zip(keys, values))

    return mapping_dict


# %% Cleaning function for claims bdx

def claims_bdx_clean(file, mapping_dict):
    """Read in file, change column headers and output only the required cols
    """

    df = pd.read_excel(file, sheet_name = 0, header=2)

    # Map cols
    df = df.rename(columns=mapping_dict)
    df = df[[col for col in df.columns if type(col) is not float]]

    # GDPR drop fields
    df = df.drop(labels=['Name_Claimant', 'Name_Insured'], axis=1)

    # Drop any subtotal rows
    df.dropna(axis=0, how='any', subset='ID_Claim', inplace=True)

    # Total checks on Incurred
    incurred_check = round(df.Incurred,0) == round(df.Incurred_Indemnity + df.Incurred_Expenses + df.Incurred_TPA_Fees, 0)
    df_false_inc = df[~incurred_check]

    # Need to also check on the policy ID at some point

    if len(df_false_inc) > 0:
        print('Output rejected due to {0} rows not matching on Incurred values'.format(len(df_false_inc)))
        test_inc = False
    else:
        test_inc = True

    return df, test_inc, df_false_inc


# %% Lets try to make use of inheritance here

class BdxCleaner(object):
    def __init__(self, bdx_type, bdx_file):
        self.bdx_type = bdx_type
        self.file = bdx_file
        self.mapping_dict = get_mapping(self.bdx_type)


    def get_mapping(self):
        """Get a dictionary of column mapping, and a list of the column subset that we want to retain.
        """

        # Link to mapping files here
        mappings = {'claim':r'\\svrtcs04\Syndicate Data\Actuarial\Pricing\2_Account_Pricing\NFS_Edge\Knowledge\Data_Received\Monthly\_ColumnMapping\claim_WITHACTIONS.xlsx',
                    'risk':r'\\svrtcs04\Syndicate Data\Actuarial\Pricing\2_Account_Pricing\NFS_Edge\Knowledge\Data_Received\Monthly\_ColumnMapping\risk_WITHACTIONS.xlsx',
                    'premium':r'\\svrtcs04\Syndicate Data\Actuarial\Pricing\2_Account_Pricing\NFS_Edge\Knowledge\Data_Received\Monthly\_ColumnMapping\premium_WITHACTIONS.xlsx'}

        # Read in the mapping file
        df_claim_mapping = pd.read_excel(mappings[self.bdx_type])

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
        df = df.rename(columns=self.mapping_dict)
        df = df[[col for col in df.columns if type(col) is not float]]

        # GDPR drop fields
        df = df.drop(labels=['Name_Claimant', 'Name_Insured'], axis=1)

        # Drop any subtotal rows
        df.dropna(axis=0, how='any', subset='ID_Claim', inplace=True)
    


