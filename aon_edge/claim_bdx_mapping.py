# %% Package imports

import pandas as pd
import openpyxl
from general_bdx_clean import BdxCleaner, mappings, header_dict, id_dict, sheet_dict


# %% Claims class - using inheritance

class ClaimBdxCleaner(BdxCleaner):
    """Used to clean AON Edge Claims bordereaux, inherits methods from BdxCleaner
    """
    def __init__(self, bdx_file, mappings, headers, IDs, sheet_dict):
        self.file = bdx_file
        self.mappings = mappings
        self.headers = headers
        self.IDs = IDs
        self.sheets = sheet_dict
        self.bdx_type = 'claim'
        self.dataframe = self.basic_cleaning()
        self.test_var = True
        self.xl_file = openpyxl.load_workbook(self.file, read_only=True, data_only=True)


    def incurred_check(self):
        """Does the incurred approximately match in all rows?
        If not, export the rows which do not to an error log.
        """

        incurred_check = round(self.dataframe.Incurred,0) == round(self.dataframe.Incurred_Indemnity +
                                                                   self.dataframe.Incurred_Expenses +
                                                                   self.dataframe.Incurred_TPA_Fees, 0)
        df_false_inc = self.dataframe[~incurred_check]

        if len(df_false_inc) > 0:
            print('Output rejected due to {0} rows not matching on Incurred values\nRejected rows exported to Rejected_Files directory'.format(len(df_false_inc)))
            test_inc = False
        else:
            test_inc = True
            print('Incurred values match to nearest integer, test passed!')
        
        return test_inc, df_false_inc


    def other_claims_checks(self):
        """Enter other checks here or in similar functions
        """
        return True


    def drop_gdpr_fields(self):
        """Drop GDPR sensitive fields
        """
        # May need to test if these in bdx first
        self.dataframe = self.dataframe.drop(labels=['Name_Claimant', 'Name_Insured'], axis=1)


    def run_all_checks(self):
        """This is for running all the checks you might need in a sequential fashion
        that breaks once a test fails.

        Grace requests that the tests all run, with the option to accept the rejected rows or not
        """
        # First check that the incurred matches
        test_inc, df_false_inc = self.incurred_check()
        self.test_var = test_inc

        if self.test_var:
            pass
        else:
            df_false_inc.to_excel(r'\\svrtcs04\Syndicate Data\Actuarial\Pricing\2_Account_Pricing\NFS_Edge\Knowledge\Data_Received\Monthly\Rejected_Files\claims_incurred_non_matching.xlsx')
        
        # Run the other checks in a similar way, but we only run the test function 
        # if the test_var is true which is to say the previous test has passed
        if self.test_var:
            test_result_example = self.other_claims_checks()
            self.test_var = test_result_example
            if self.test_var:
                pass
            else:
                # Run the rejection output if necessary
                pass
        else:
            pass

        # After all the tests have run
        if self.test_var:
            print('All tests have passed!')
        else:
            print('Bordereaux rejected.')
    

    def run_all_processing_functions(self):
        """Once all the tests have passed, we can run all the processing steps.
        """
        # Maybe add a print output to this one?
        self.drop_gdpr_fields()
        self.username_input()
        self.date_code_run()
        self.add_file_name()

    


# %% Actually running the class

# 


