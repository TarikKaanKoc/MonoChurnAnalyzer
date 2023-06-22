# Mono-ChurnAnalyzer

<img width="1449" alt="Ekran Resmi 2023-06-23 00 03 51" src="https://github.com/TKaanKoc/MonoChurnAnalyzer/assets/83168207/671b411f-bf75-4335-a9ac-efac07d8a79c">

ChAnalyzer is a Python script designed to analyze churn rates based on user activity data stored in a PostgreSQL database. This script fetches data from the database, cleans it, and calculates the churn rate for a specified number of days. Additionally, it provides a method to check the status of a specific user.

## Prerequisites
Before running the ChAnalyzer script, make sure you have the following prerequisites installed:

- Python 3.x
- PostgreSQL
- `psycopg2` library (`pip install psycopg2`)
- `pandas` library (`pip install pandas`)
- `dotenv` library (`pip install python-dotenv`)

## Configuration
To connect to the PostgreSQL database, you need to set up a `.env` file in the same directory as the script. The `.env` file should contain the following environment variables:

- `DB_HOST`: The host address of the PostgreSQL database.
- `DB_PORT`: The port number of the PostgreSQL database.
- `DB_NAME`: The name of the PostgreSQL database.
- `DB_USER`: The username to authenticate with the PostgreSQL database.
- `DB_PASSWORD`: The password to authenticate with the PostgreSQL database.
- `DB_SSLMODE`: The SSL mode to use for the database connection (e.g., `require` or `verify-full`).

Make sure to replace the placeholder values with your actual database credentials.

## Usage
To run the ChAnalyzer script, follow these steps:

1. Clone the repository or download the script file.
2. Install the required dependencies listed in the "Prerequisites" section.
3. Create a `.env` file and set the necessary environment variables as described in the "Configuration" section.
4. Open a terminal or command prompt and navigate to the directory where the script is located.
5. Run the following command:

```python
  $ python ChAnalyzer.py
```


The script will fetch the data from the PostgreSQL database, clean it, calculate the churn rate for the specified number of days (default: 90), and display the result on the console.

**Note:** You can modify the number of days and the user ID to check by modifying the relevant parameters in the `calculate_churn_rate` and `_check_user_status` method calls, respectively.

6. The script will print the churn rate and the status of the specified user to the console.

## Script Details

### `ChurnAnalyzer` Class
The `ChurnAnalyzer` class represents the main logic of the churn analysis script. It has the following methods:

- `__init__()`: Initializes the `ChurnAnalyzer` object and retrieves the database connection details from environment variables.
- `_load_data()`: Loads data from the PostgreSQL database and converts it into a pandas DataFrame.
- `_clean_data(df_refresh_tokens, df_active_users)`: Cleans the dataset by removing unnecessary columns and records with missing values.
- `calculate_churn_rate(df, days)`: Calculates the churn rate within a specified number of days.
- `_check_user_status(result_df, target_user)`: Checks the status of a specific user and prints the result to the console.

### Running the Script
The script's entry point is the `if __name__ == "__main__":` block at the bottom. It creates an instance of the `ChurnAnalyzer` class, loads data from the database, cleans the data, calculates the churn rate, and checks the status of a specific user.

You can modify the number of days and the user ID to check by changing the arguments passed to the `calculate_churn_rate` and `_check_user_status` method calls, respectively.

## Conclusion
The ChAnalyzer script provides a convenient way to analyze churn rates based on user activity data stored in a PostgreSQL database. By following the instructions outlined in this README, you can easily configure and run the script to obtain churn rate insights for your application or service.


