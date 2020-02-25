# %% Imports

import glob
import pandas as pd
from claim_bdx_mapping import ClaimBdxCleaner
from risk_bdx_mapping import RiskBdxCleaner
from general_bdx_clean import mappings, header_dict, id_dict, sheet_dict
from sql_connection import sql_connection


# %% Params

directory = r"\\svrtcs04\Syndicate Data\Actuarial\Pricing\2_Account_Pricing\NFS_Edge\Knowledge\Data_Received\Monthly"
claims_bdx = glob.glob(directory + r"\**\Claims\*.xls*")

claims_test = claims_bdx[-15:]


# %% 

claim_bdx = ClaimBdxCleaner(claims_bdx[0], mappings, header_dict, id_dict, sheet_dict)

claim_bdx.run_all_checks()
claim_bdx.run_all_processing_functions()
claim_bdx.export_to_sql()


# %% New Plan - Get the cumulative bordereaux into SQL

# Try claims first, get all the bdx in with reporting period tag and evaluate headers

def full_claim_bdx(bdx_list, mappings, header_dict, id_dict, sheet_dict):
    """For all the bdx provided, run the checks and processing steps
    then return a combined table.
    """

    df_list = []

    bdx_list = [file for file in bdx_list if '$' not in file]

    for file in bdx_list:
        print(file)
        claim_bdx = ClaimBdxCleaner(file, mappings, header_dict, id_dict, sheet_dict)
        claim_bdx.run_all_checks()
        claim_bdx.run_all_processing_functions()
        df_list.append(claim_bdx.dataframe)
    
    df_combined = pd.concat(df_list, ignore_index=True)

    # Put any whole dataframe checks here

    return df_combined


# %% execute

df_combined = full_claim_bdx(claims_bdx, mappings, header_dict, id_dict, sheet_dict)

sql_con = sql_connection('tcspmSMDB02', 'PricingDevelopment')

df_combined.to_sql('NFS_Combined_Claims', sql_con, schema='bdx', if_exists='replace', index=False)


# %% Risk Cumulative Bordereaux

def cumulative_risk_bdx(bdx_list, mappings, header_dict, id_dict, sheet_dict):
    """For all the bdx provided, run the checks and processing steps
    then return a combined table.
    """

    df_list = []

    bdx_list = [file for file in bdx_list if '$' not in file]

    for file in bdx_list:
        print(file)
        risk_bdx = RiskBdxCleaner(file, mappings, header_dict, id_dict, sheet_dict)
        print('Object initialised')
        risk_bdx.run_all_checks()
        risk_bdx.run_all_processing_functions()
        df_list.append(risk_bdx.dataframe)
    
    df_combined = pd.concat(df_list, ignore_index=True)

    # Put any whole dataframe checks here

    return df_combined


# %% execute risk

risk_bdx_list = glob.glob(directory + r"\**\Risk\*.xls*")

df_combined = cumulative_risk_bdx(risk_bdx_list, mappings, header_dict, id_dict, sheet_dict)

df_combined.to_sql('NFS_Combined_Risk', sql_con, schema='bdx', if_exists='replace', index=False)



