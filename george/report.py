import os
from Inspect.report import BaseReport


class Report(BaseReport):
    '''Skeleton for creating a report. It is recommended that the developer change the name
    of this class to something reasonably descriptive given the purpose of the report.

    Attributes:
        path (str): The path to the report.yaml file. By default a report.yaml file is created
         in the report app directory. This attribute must be set by the developer. When an instance
         of the Report class is created it reads in the

         Example:
             path = '{0}/report.yaml'.format(os.path.dirname(os.path.realpath(__file__)))

    Methods:
        __init__

            Note: The __init__ method is defined on the BaseReport class. It initializes the instance
            by first setting self.data to an empty list and then calling self.load_yaml() which parses
            the report.yaml file and loads the data from the database as a list of lists where each sub list
            is a list of dictionaries of the results returned by the database.

        load_yaml
            Args:
                target (Optional[str]): A fully qualified path to a yaml file. This reloads the report object
                    with the data represented by the new yaml file.
    '''
    path = '{0}/report.yaml'.format(os.path.dirname(os.path.realpath(__file__)))

    def generate_report(self):
        '''Customize self.data for report generation

            Note: This method is defined on BaseReport as an abstract method and must
            be implemented

            Returns:
                List of records as specified by the developer
        '''
        return self.data
        # Simplest example
