
# %% Package imports

import pandas as pd
from pathlib import Path
import glob
import xlrd
import missingno as msno
from sql_connection import sql_connection


# %% Get files

# risk only
files = glob.glob(r'\\svrtcs04\Syndicate Data\Actuarial\Pricing\2_Account_Pricing\NFS_Edge\Knowledge\Data_Received\Monthly\**\*Bordereau*.xlsx')
files_ = [ file for file in files if "$" not in file ]


# %% Raw table

xls = xlrd.open_workbook(files[0], on_demand=True)

df_list = []

for sheet in xls.sheet_names():
    
    risk_bdx_raw = pd.read_excel(files[0], sheet_name=sheet)

    df_list.append(risk_bdx_raw)


# %% Missing fields check

msno.matrix(df_list[0].sample(250))
msno.heatmap(df_list[0].sample(250))
msno.bar(df_list[0].sample(1000))


# %% export raw tables to sql

# Need to define whether year of account should be separated

