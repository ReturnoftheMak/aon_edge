# %% Package Imports

import pandas as pd
import openpyxl
from general_bdx_clean import BdxCleaner, mappings, header_dict, id_dict, sheet_dict


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
    def __init__(self, bdx_file, mappings, headers, IDs, sheet_dict):
        self.file = bdx_file
        self.mappings = mappings
        self.headers = headers
        self.IDs = IDs
        self.sheets = sheet_dict
        self.bdx_type = 'risk'
        self.dataframe = self.basic_cleaning()
        self.test_var = True
        self.xl_file = openpyxl.load_workbook(self.file, read_only=True, data_only=True)
        self.new_renewal_mapping = {}
        


    def policy_ID_formatting(self):
        """Change the id based on Grace's rules, possibly map to 2 cols
        """
        pass


    def new_or_renewal(self):
        """Map any rows which are not 'New' or 'Renewal'
        """

        if 'Status_NewRenew' in self.dataframe.columns:
            from fuzzywuzzy import process
            import json

            # could use a fillna here? but with what?
            # use fuzz.partial_ratio to compare to New/Renewal
            # Require a certain threshold, request confirmation
            # If confirmed, add to the dictionary
            # This dictionary likely needs to be exported then reimported on load
            # Hold it in a json, in a directory of dictionaries

            with open(r'\\svrtcs04\Syndicate Data\Actuarial\Pricing\2_Account_Pricing\NFS_Edge\Knowledge\Data_Received\Monthly\_ColumnMapping\risk_dictionaries\new_renewal.json') as json_file:
                data = json.load(json_file)
            
            status_list = list(self.dataframe.Status_NewRenew.unique())

            unmapped_statuses = [status for status in status_list if status not in list(data.keys())]

            # Firstly, we'll take a look at the values in the data dict to see if we can match close to one
            if len(unmapped_statuses) > 0:
                for status in unmapped_statuses:
                    # Is it close to one of the accepted dictionary values?
                    best_value_match = process.extractOne(status.lower(), list(data.values()))
                    if best_value_match[1] > 90:
                        # Prompt to accept the match if it hits above a threshold
                        while True:
                            answer = input("Should {0} be mapped to {1}? (y/n)".format(status, best_value_match[0]))
                            if answer.lower() not in ('y', 'n'):
                                print('Invalid response, please try again')
                            else:
                                break
                    else:
                        answer = 'n'
                    
                    if answer == 'y':
                        data[status] = best_value_match[0]
                    else:
                        while True:
                            label = input("Map {0} to New/Renewal? (N/R)")
                            if answer.lower() not in ('n', 'r'):
                                print('Invalid response, please try again')
                            else:
                                break
                        data[status] = label

                with open(r'\\svrtcs04\Syndicate Data\Actuarial\Pricing\2_Account_Pricing\NFS_Edge\Knowledge\Data_Received\Monthly\_ColumnMapping\risk_dictionaries\new_renewal.json') as json_file:
                    json.dump(data, json_file)
            else:
                pass

        else:
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
        """Add the bordereaux month as a column, 
        logic stated was to use last day of the month as the date.
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
        if 'Name_Broker' in self.dataframe.columns:
            self.dataframe = self.dataframe.drop(labels=['Name_Broker'], axis=1)
        else:
            pass


    def prior_loss_flag(self):
        """Needs populating
        """
        pass


    def renewed_flag(self):
        """This may actually need some more inputs
        """
        pass


    def run_all_checks(self):
        """This is for running all the checks you might need in a sequential fashion
        that breaks once a test fails.
        """
        # Order the tests sequentially here with conditional passes and updates to self.test_var

        # After all the tests have run
        if self.test_var:
            print('All tests have passed!')
        else:
            print('Bordereaux rejected.')
    

    def run_all_processing_functions(self):
        """Once all the tests have passed, we can run all the processing steps.
        """
        self.username_input()
        self.date_code_run()
        self.add_file_name()
        self.drop_gdpr_fields()
        self.new_or_renewal()

        print('Processing steps complete!')

