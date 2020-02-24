# %% Imports

import glob
from claim_bdx_mapping import ClaimBdxCleaner
from general_bdx_clean import mappings, header_dict, id_dict


# %% Params

directory = r"\\svrtcs04\Syndicate Data\Actuarial\Pricing\2_Account_Pricing\NFS_Edge\Knowledge\Data_Received\Monthly"
claims_bdx = glob.glob(directory + r"\**\Claims\*.xls*")


# %%



