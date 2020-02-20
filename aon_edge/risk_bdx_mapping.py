# %% Package Imports

import pandas as pd
from general_bdx_clean import BdxCleaner


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


# %%

class RiskBdxCleaner(BdxCleaner):
    """Used to clean AON Edge Risk bordereaux, inherits methods from BdxCleaner
    """
    def __init__(self, bdx_file, mappings):
        self.file = bdx_file
        self.mappings = mappings
        self.bdx_type = 'risk'
        self.dataframe = self.basic_cleaning()
    

    def policy_ID_formatting(self):
        """Change the id based on Grace's rules, possibly map to 2 cols
        """
        pass


    def new_or_renewal(self):
        """Map any rows which are not 'New' or 'Renewal'
        """

        # could use a fillna here? but with what?
        pass


    def premium_checks(self):
        """Check premium by policy against premium bordereaux
        """
        pass


    def flood_score_populate(self):
        """Where blank, may need to use a different source to populate
        """
        pass


    def add_bdx_date(self):
        """Add the bordereaux month as a column
        """
        pass


    def locname_split(self):
        """Need to turn this into policy ID?
        """
        pass


    def drop_gdpr_fields(self):
        """Drop GDPR sensitive fields
        """
        # May need to test if these are in bdx first
        self.dataframe = self.dataframe.drop(labels=['Name_Broker'], axis=1)
    

    def prior_loss_flag(self):
        """Needs populating
        """
        pass


    def renewed_flag(self):
        """This may actually need some more inputs
        """
        pass


    def username_input(self):
        """Add in a username for whoever ran the code
        """

        from getpass import getuser
        user = getuser()
        self.dataframe['Updated_Name'] = user
    
    #
    

