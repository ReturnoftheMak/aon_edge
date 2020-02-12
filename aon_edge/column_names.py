
# %% Package Imports

import glob
import pandas as pd
from pathlib import Path

# %% Files area

directory = r"\\svrtcs04\Syndicate Data\Actuarial\Pricing\2_Account_Pricing\NFS_Edge\Knowledge\Data_Received\Monthly"

excel_files = glob.glob(directory + r"\**\*.xls*")


# %% Parse files from relevant sections

risk_bdx = glob.glob(directory + r"\**\Risk\*.xls*")
premium_bdx = glob.glob(directory + r"\**\Premium\*.xls*")
claims_bdx = glob.glob(directory + r"\**\Claims\*.xls*")


# %% Get the column names

def get_col_names(bdx_list):
    """Retrieve list of column names from the list of bdx provided
    """

    col_names = []

    bdx_list = [file for file in bdx_list if "$" not in file]
    
    for file in bdx_list:
        
        df = pd.read_excel(file)

        new_names = [col for col in df.columns if col not in col_names]
        col_names.append(new_names)
    
    return col_names


risk_col_names = get_col_names(risk_bdx)
premium_col_names = get_col_names(premium_bdx)
claim_col_names = get_col_names(claims_bdx)


# %%
