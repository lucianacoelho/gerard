import pandas as pd

class Report:
    def __init__(self, df, response_column, issuing_bank, source):
        self.df = df
        self.response_column = response_column
        self.issuing_bank = issuing_bank
        self.source = source
    
    def summarize(self):
        """
        Gives a brief report with top 5 responses (auth rate etc),
        issuer with most transactions and top 5 issuers with higher decline rate.
        """
        upper = self.source.upper()

        if upper == 'TD':
            not_approved = self.df[self.df[self.response_column] != "APPROVED"]
        elif upper == 'LP':
            not_approved = self.df[self.df[self.response_column] != "Approved"]
        else:
            raise ValueError("Invalid source value.")

        normalized_response = self.df[self.response_column]
        issuer = self.df[self.issuing_bank]
        responses = (normalized_response.value_counts(normalize=True)*100).head(5)
        issuer_not_approved = (not_approved[self.issuing_bank].value_counts(normalize=True)*100).head(10)
        issuer = (issuer.value_counts(normalize=True)*100).head(10)

        print(f"The responses are (%):\n{responses}\n\nIssuers with most transactions:\n{issuer}\n\nIssuers with higher decline rate:\n{issuer_not_approved}")
        
    def impact(self, filter_by, sub_filter):
        """
        Returns the impact x has on the operation.
        """
        new_df = pd.crosstab(self.df[self.response_column], self.df[filter_by], normalize=True)*100
        bank = new_df[sub_filter]
        bank_df = pd.DataFrame(bank).T
        if self.response_column == 'nrmlzd_response':
            improvement = bank.sum() - bank_df['APPROVED']
        elif self.response_column == 'Processor Response Text':
            improvement = bank.sum() - bank_df['Approved']
        else:
            raise ValueError("Invalid response column value.")
        return improvement

class Crosstab:
    def __init__(self, df, col1, col2):
        self.df = df
        self.col1 = col1
        self.col2 = col2
        
    def crosstab(self):
        """
        Crosses two columns inside a dataframe.
        """
        result = pd.crosstab(self.df[self.col1], self.df[self.col2], normalize=True)*100
        print(result)


## use:
# report = Report(df, 'nrmlzd_response', 'Issuing Bank', 'TD')
# report.summarize()

## use:
# crosstab = Crosstab(df, 'col1', 'col2')
# crosstab.crosstab()

class TransactionAnalyzer:
    """Analyzes transaction data."""

    def __init__(self, df):
        """Initializes the TransactionAnalyzer with a DataFrame.

        Args:
            df (pd.DataFrame): The transaction data.
        """
        self.df = df

    def specific_approval(self, response_column, filter_by, sub_filter=None):
        """Returns the approval rate for specific parameters.

        Args:
            response_column (str): The column used to calculate the approval rate, which should contain the values "Approved" or "Declined".
            filter_by (str): The parameter/column to be analyzed, e.g. "acquirer".
            sub_filter (str, optional): A special parameter/category to be analyzed, e.g. "CILO", or None if you just want the general approval rate for a column. Defaults to None.

        Returns:
            pd.DataFrame: A cross tabulation of approval rates by parameter/category.
        """
        if sub_filter is None:
            new_df = self.df[filter_by]
            result = pd.crosstab(self.df[response_column], new_df, normalize=True)*100
        else:
            new_df = self.df[self.df[filter_by]==sub_filter]
            result = pd.crosstab(self.df[response_column], new_df[filter_by], normalize=True)*100
        return result

    def dedup(self):
        """Removes duplicate rows based on specified columns.

        Returns:
            pd.DataFrame: The dataframe with duplicate rows removed.
        """
        non_retry_transactions_df = self.df.drop_duplicates(subset=['Amount Submitted For Settlement', 'Credit Card Number', 'Descriptor Name'], keep='last')
        return non_retry_transactions_df

    def share(self, filter_by, sub_filter=None):
        """Returns the share that x represents in the operation.

        Args:
            filter_by (str): The parameter to filter the possible improvement by, e.g. "Issuing Bank".
            sub_filter (str, optional): A filter inside the filter_by, e.g. "NU PAGAMENTOS S.A.", or None for no sub filter. Defaults to None.

        Returns:
            pd.Series: The share represented by x.
        """
        a = self.df[filter_by]
        share = (a.value_counts(normalize=True)*100).head(10)
        if sub_filter is None:
            return share
        else:
            try:
                share = share[sub_filter]
            except KeyError:
                raise ValueError(f"{sub_filter} not found in {filter_by}")
            return share
