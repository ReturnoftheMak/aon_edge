# %% Package Imports

import pandas as pd


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


