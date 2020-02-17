# %% Package imports

import pandas as pd


# %% Get a dict of col name to mapped name

filename_claims = r'\\svrtcs04\Syndicate Data\Actuarial\Pricing\2_Account_Pricing\NFS_Edge\Knowledge\Data_Received\Monthly\_ColumnMapping\claim_WITHACTIONS.xlsx'

def get_mapping(filename):
    """Get a dictionary of column mapping, and a list of the column subset that we want to retain.
    """

    df_claim_mapping = pd.read_excel(filename)

    keys = df_claim_mapping.ColumnNames
    values = df_claim_mapping.Rename

    mapping_dict = dict(zip(keys, values))

    return mapping_dict


def claims_bdx_clean(file, mapping_dict):
    """Read in file, change column headers and output only the required cols
    """

    df = pd.read_excel(file, sheet_name = 0, header=2)

    df = df.rename(columns=mapping_dict)

    df = df[[col for col in df.columns if type(col) is not float]]

    # Implement Checks

    # GDPR drop fields
    df = df.drop(labels=['Name_Claimant', 'Name_Insured'], axis=1)

    # Total checks on Incurred
    incurred_check = round(df.Incurred,0) == round(df.Incurred_Indemnity + df.Incurred_Expenses + df.Incurred_TPA_Fees, 0)

    df_false = df[~incurred_check]

    # Need to also check on the policy ID at some point

    if len(df_false) > 0:
        print('Output rejected due to {0} rows not matching on Incurred values'.format(len(df_false)))
    else:
        return df



# %%
