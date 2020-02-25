# %% Imports

import glob
import pandas as pd
from claim_bdx_mapping import ClaimBdxCleaner
from general_bdx_clean import mappings, header_dict, id_dict
from sql_connection import sql_connection


# %% Params

directory = r"\\svrtcs04\Syndicate Data\Actuarial\Pricing\2_Account_Pricing\NFS_Edge\Knowledge\Data_Received\Monthly"
claims_bdx = glob.glob(directory + r"\**\Claims\*.xls*")

claims_test = claims_bdx[-15:]


# %% 

claim_bdx = ClaimBdxCleaner(claims_bdx[0], mappings, header_dict, id_dict)

claim_bdx.run_all_checks()
claim_bdx.run_all_processing_functions()
claim_bdx.export_to_sql()


# %% New Plan - Get the cumulative bordereaux into SQL

# Try claims first, get all the bdx in with reporting period tag and evaluate headers

def full_claim_bdx_upload(bdx_list, mappings, header_dict, id_dict):
    """For all the bdx provided, run the checks and processing steps
    then return a combined table.
    """

    df_list = []

    for file in bdx_list:
        print(file)
        claim_bdx = ClaimBdxCleaner(file, mappings, header_dict, id_dict)
        claim_bdx.run_all_checks()
        claim_bdx.run_all_processing_functions()
        df_list.append(claim_bdx.dataframe)
    
    df_combined = pd.concat(df_list, ignore_index=True)

    return df_combined


# %%

df_combined = full_claim_bdx_upload(claims_bdx, mappings, header_dict, id_dict)

sql_con = sql_connection('tcspmSMDB02', 'PricingDevelopment')

df_combined.to_sql('NFS_Combined_Claims', sql_con, schema='bdx', if_exists='replace', index=False)


# %% 



