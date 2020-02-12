
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

    col_names = {}

    bdx_list = [file for file in bdx_list if "$" not in file]
    
    for file in bdx_list:

        df = pd.read_excel(file)

        bdx_month = Path(risk_bdx[0]).parent.parent.stem

        col_names[bdx_month] = df.columns
    
    return col_names


risk_col_names = get_col_names(risk_bdx)
premium_col_names = get_col_names(premium_bdx)
claim_col_names = get_col_names(claims_bdx)


# %% Export column names to excel

risk_col = pd.DataFrame.from_dict(risk_col_names, orient='index')
risk_col.to_excel(r"\\svrtcs04\Syndicate Data\Actuarial\Pricing\2_Account_Pricing\NFS_Edge\Knowledge\Data_Received\Monthly\_ColumnMapping\risk_column_headers.xlsx")

premium_col = pd.DataFrame(premium_col_names, columns=['ColumnHeader'])
premium_col.to_excel(r"\\svrtcs04\Syndicate Data\Actuarial\Pricing\2_Account_Pricing\NFS_Edge\Knowledge\Data_Received\Monthly\_ColumnMapping\premium_column_headers.xlsx")

claim_col = pd.DataFrame(claim_col_names, columns=['ColumnHeader'])
claim_col.to_excel(r"\\svrtcs04\Syndicate Data\Actuarial\Pricing\2_Account_Pricing\NFS_Edge\Knowledge\Data_Received\Monthly\_ColumnMapping\claim_column_headers.xlsx")


# %%
