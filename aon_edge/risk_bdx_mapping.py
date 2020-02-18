# %% Package Imports

import pandas as pd


# %% Set Params

mapping_file = r'\\svrtcs04\Syndicate Data\Actuarial\Pricing\2_Account_Pricing\NFS_Edge\Knowledge\Data_Received\Monthly\_ColumnMapping\risk_WITHACTIONS.xlsx'


# %% Cleaning function for risk bordereaux

def risk_bdx_clean(file, mapping_dict):
    """Read in file, change column headers and output only the required cols
    """

    df = pd.read_excel(file, sheet_name = 0, header=0)

    df = df.rename(columns=mapping_dict)

    df = df[[col for col in df.columns if type(col) is not float]]

    # Drop any subtotal rows
    df.dropna(axis=0, how='any', subset='ID_PolicyStem', inplace=True)

    # New / Renewal mapping, needs populating
    new_renew_dict = {}
    df.Status_NewRenew.rename(to_replace=new_renew_dict)

    # Create ID_Policy column from policy stem and inception year
    df['ID_Policy'] = df.ID_PolicyStem + '_' + df.Date_Inception_Policy.dt.year.astype(str)

    # Check premium against premium bordereaux - to do
    # Possibly other checks to be done




