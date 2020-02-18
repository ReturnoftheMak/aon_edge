
# %% Package Imports

import glob
import pandas as pd
from pathlib import Path
from sql_connection import sql_connection


# %% Files area

sqlcon = sql_connection('tcspmSMDB02', 'PricingDevelopment')

directory = r"\\svrtcs04\Syndicate Data\Actuarial\Pricing\2_Account_Pricing\NFS_Edge\Knowledge\Data_Received\Monthly"

excel_files = glob.glob(directory + r"\**\*.xls*")


# %% Parse files from relevant sections

risk_bdx = glob.glob(directory + r"\**\Risk\*.xls*")
premium_bdx = glob.glob(directory + r"\**\Premium\*.xls*")
claims_bdx = glob.glob(directory + r"\**\Claims\*.xls*")


# %% Get the column names

def get_col_names_by_month_and_unique(bdx_list, header_var=0):
    """Retrieve list of column names from the list of bdx provided
    """

    col_names_dict = {}
    col_names_unique = []

    bdx_list = [file for file in bdx_list if "$" not in file]
    
    for file in bdx_list:

        df = pd.read_excel(file, header=header_var)

        bdx_month = Path(file).parent.parent.stem
        col_names_dict[bdx_month] = df.columns

        new_names = [col for col in df.columns if col not in col_names_unique]
        for name in new_names:
            col_names_unique.append(name)
    
    return col_names_dict, col_names_unique


# %% run for excel bdx

risk_col_names_by_month, risk_col_names_unique = get_col_names_by_month_and_unique(risk_bdx)
premium_col_names_by_month, premium_col_names_unique = get_col_names_by_month_and_unique(premium_bdx)
claim_col_names_by_month, claim_col_names_unique = get_col_names_by_month_and_unique(claims_bdx, 2)


# %% Also need to get data from the database

# Weirdly can't connect, not sure whats going on here, try again later

df_risk_col_names_old = pd.read_sql_query('select * from bdx.NFSRiskBdx201904', sqlcon)
risk_col_names_by_month['NFSRiskBdx201904'] = df_risk_col_names_old.columns


# %% Export column names to excel

risk_col = pd.DataFrame.from_dict(risk_col_names_by_month, orient='index')
risk_col.to_excel(r"\\svrtcs04\Syndicate Data\Actuarial\Pricing\2_Account_Pricing\NFS_Edge\Knowledge\Data_Received\Monthly\_ColumnMapping\risk_column_headers_all_v2.xlsx", sheet_name='names_by_month')
risk_col_unique = pd.DataFrame(risk_col_names_unique + list(df_risk_col_names_old.columns), columns=['ColumnNames']).drop_duplicates()
risk_col_unique.to_excel(r"\\svrtcs04\Syndicate Data\Actuarial\Pricing\2_Account_Pricing\NFS_Edge\Knowledge\Data_Received\Monthly\_ColumnMapping\risk_column_headers_unique_v2.xlsx", sheet_name='unique_names')

premium_col = pd.DataFrame.from_dict(premium_col_names_by_month, orient='index')
premium_col.to_excel(r"\\svrtcs04\Syndicate Data\Actuarial\Pricing\2_Account_Pricing\NFS_Edge\Knowledge\Data_Received\Monthly\_ColumnMapping\premium_column_headers.xlsx", sheet_name='names_by_month')
premium_col_unique = pd.DataFrame(premium_col_names_unique, columns=['ColumnNames'])
premium_col_unique.to_excel(r"\\svrtcs04\Syndicate Data\Actuarial\Pricing\2_Account_Pricing\NFS_Edge\Knowledge\Data_Received\Monthly\_ColumnMapping\premium_column_headers_unique.xlsx", sheet_name='unique_names')

claim_col = pd.DataFrame.from_dict(claim_col_names_by_month, orient='index')
claim_col.to_excel(r"\\svrtcs04\Syndicate Data\Actuarial\Pricing\2_Account_Pricing\NFS_Edge\Knowledge\Data_Received\Monthly\_ColumnMapping\claim_column_headers.xlsx", sheet_name='names_by_month')
claim_col_unique = pd.DataFrame(claim_col_names_unique, columns=['ColumnNames'])
claim_col_unique.to_excel(r"\\svrtcs04\Syndicate Data\Actuarial\Pricing\2_Account_Pricing\NFS_Edge\Knowledge\Data_Received\Monthly\_ColumnMapping\claim_column_headers_unique.xlsx", sheet_name='unique_names')


# %%
