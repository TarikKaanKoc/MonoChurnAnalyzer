import os
from dotenv import load_dotenv
import psycopg2
import pandas as pd
from datetime import timedelta

load_dotenv()

class ChurnAnalyzer:
    def __init__(self):
        """
        Initializes the ChurnAnalyzer object.
        """
        self.host = os.getenv("DB_HOST")
        self.port = os.getenv("DB_PORT")
        self.dbname = os.getenv("DB_NAME")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.sslmode = os.getenv("DB_SSLMODE")
        
    def _load_data(self):
        """
        Loads data from the PostgreSQL database and converts it to a DataFrame.

        Returns
        -------
        pandas.DataFrame
            DataFrame representation of the loaded data.
        """
        # Create a PostgreSQL connection
        conn = psycopg2.connect(
            host=self.host,
            port=self.port,
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            sslmode=self.sslmode
        )

        cursor = conn.cursor()

        refresh_tokens_query = "SELECT * FROM ******.'RefreshTokens'" # Replace with your own schema name
        active_users_query = "SELECT * FROM ******.'ActiveUsers'" # Replace with your own schema name

        cursor.execute(refresh_tokens_query)
        refresh_tokens = cursor.fetchall()

        cursor.execute(active_users_query)
        active_users = cursor.fetchall()

        df_refresh_tokens = pd.DataFrame(refresh_tokens, columns=["UserId", "LastUsedDate"])
        df_active_users = pd.DataFrame(active_users, columns=["UserId"])

        conn.close()

        return df_refresh_tokens, df_active_users

    def _clean_data(self, df_refresh_tokens, df_active_users):
        """
        Cleans the dataset by removing unnecessary columns and records with missing values.

        Parameters
        ----------
        df : pandas.DataFrame
            Dataset to be cleaned.

        Returns
        -------
        pandas.DataFrame
            Cleaned dataset.
        """
        # Data cleaning operations
        df_refresh_tokens.drop(['Id', 'CreatedDate', 'Status', 'ModifiedDate', 'DeviceId', 'UsageCount', 'Token'],
                inplace=True, axis=1)
        df_refresh_tokens['LastUsedDate'] = pd.to_datetime(df_refresh_tokens['LastUsedDate'], format='%Y-%m-%d %H:%M:%S.%f%z', errors='coerce')
        merged_df = pd.merge(df_active_users, df_refresh_tokens, on='UserId')
        merged_df.dropna(subset=['LastUsedDate'], inplace=True, axis=0)
        merged_df.drop_duplicates(subset=['UserId'], inplace=True, keep='last')
        return merged_df

    def calculate_churn_rate(self, df, days):
        """
        Calculates the churn rate within a specified number of days.

        Parameters
        ----------
        df : pandas.DataFrame
            Dataset for churn rate calculation.
        days : int
            Number of days for churn rate calculation.

        Returns
        -------
        pandas.DataFrame
            Churn rate calculation results.
        """
        cutoff_date = df['LastUsedDate'].max() - timedelta(days=days)
        inactive_users = df[df['LastUsedDate'] < cutoff_date]['UserId'].nunique()
        total_users = df['UserId'].nunique()
        churn_rate = round((inactive_users / total_users) * 100, 2)

        active_user_ids = df[df['LastUsedDate'] >= cutoff_date]['UserId'].unique()
        inactive_user_ids = df[df['LastUsedDate'] < cutoff_date]['UserId'].unique()

        result_df = pd.DataFrame({
            'ChurnRate': [churn_rate],
            'TotalUsers': [total_users],
            'InactiveUsers': [inactive_users],
            'ActiveUsers': [total_users - inactive_users],
            'ActiveUserIdx': [active_user_ids],
            'InactiveUserIdx': [inactive_user_ids]
        })

        return result_df

    def _check_user_status(self, result_df, target_user):
        """
        Checks the status of a specific user. Prints the status to the console. Example method for checking the status of a user.

        Parameters
        ----------
        result_df : pandas.DataFrame
            Dataset containing churn rate results.
        target_user : int
            ID of the user to check the status for.
        """
        active_status_list = result_df['ActiveUserIdx'].values[0].tolist()
        inactive_status_list = result_df['InactiveUserIdx'].values[0].tolist()

        if target_user in active_status_list:
            print("The user {} is in Active status.".format(target_user))
        elif target_user in inactive_status_list:
            print("The user {} is in Inactive status.".format(target_user))
        else:
            print("No such user found. ID {} not found.".format(target_user))

if __name__ == "__main__":
    analyzer = ChurnAnalyzer()
    df_refresh_tokens, df_active_users = analyzer._load_data()
    df = analyzer._clean_data(df_refresh_tokens, df_active_users)
    result_df = analyzer.calculate_churn_rate(df, 90) # Change the number of days here
    analyzer._check_user_status(result_df, 123456789) # Change the user ID here