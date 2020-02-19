# %% Package imports

import pandas as pd
from general_bdx_clean import BdxCleaner


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


# %% Claims class - using inheritance

class ClaimBdxCleaner(BdxCleaner):
    """Used to clean AON Edge Claims bordereaux, inherits methods from BdxCleaner
    """
    def __init__(self, bdx_file, mappings, bdx_type='claim'):
        self.bdx_type = bdx_type
        self.file = bdx_file
        self.mappings = mappings


    def incurred_check(self, df):
        """Does the incurred approximately match in all rows?
        If not, export the rows which do not to an error log.
        """

        incurred_check = round(df.Incurred,0) == round(df.Incurred_Indemnity + df.Incurred_Expenses + df.Incurred_TPA_Fees, 0)
        df_false_inc = df[~incurred_check]

        if len(df_false_inc) > 0:
            print('Output rejected due to {0} rows not matching on Incurred values'.format(len(df_false_inc)))
            test_inc = False
        else:
            test_inc = True
        
        return test_inc, df_false_inc


    def other_claims_checks(self):
        """Enter other checks here
        """
        pass


    def run_checks(self):
        """Run all the checks sequentially with outputs on errors if any
        """
        pass


    def drop_gdpr_fields(self, df):
        """Drop GDPR sensitive fields
        """
        # May need to test if these in bdx first
        df = df.drop(labels=['Name_Claimant', 'Name_Insured'], axis=1)








