# %% Package imports

import pandas as pd


# %% Get a dict of col name to mapped name



def get_mapping(filename):
    """Get a dictionary of column mapping, and a list of the column subset that we want to retain.
    """

    df_claim_mapping = pd.read_excel(filename)

    keys = df_claim_mapping.ColumnNames
    values = df_claim_mapping.Rename

    mapping_dict = dict(zip(keys, values))

    cols_required = list(df_claim_mapping[df_claim_mapping['Need?'] == 'Y']['Rename'])

    return mapping_dict, cols_required


def claims_bdx_clean(file, mapping_dict, cols_required):
    """Read in file, change column headers and output only the required cols
    """

    df = pd.read_excel(file, sheet_name = 0, header=2)

    df = df.rename(columns=mapping_dict)

    df = df[[col for col in df.columns if type(col) is not float]]

    # Implement Checks now

    df = df.drop(labels=['Name_Claimant', 'Name_Insured'])


