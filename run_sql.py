import sqlite3
import pandas as pd
import argparse
import os

# Python script to execute a SQL statement and store the results in a CSV file.
#
# Usage:
#   python3 run_sql.py [path_to_db] [path_to_sql] [path_to_csv]
#
# Where:
#
#   path_to_db: the path to the sqlite3 database file. default is 
#               "data/fashion_magazines.db"
# 
#   path_to_sql: the path to the file containing the sql query. default is 
#               "sql/fashion_magazines.sql"
# 
#   path_to_csv: the path to the csv file that will be created with the results 
#               of the query. default is "data/fashion_magazines.csv"

def get_paths() -> tuple:
    """Get the paths names from the arguments passed in
    @return a tuple containing (path_to_db, path_to_sql, path_to_csv)
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("db", nargs="?",
                        help="path to the sqlite3 database file", 
                        default="db/fashion_magazines.db")
    parser.add_argument("sql", nargs="?",
                        help="path to the file containing the sql query",
                        default="sql/fashion_magazines.sql")
    parser.add_argument("csv", nargs="?",
                        help="path to the csv file that will be created",
                        default="data/fashion_magazines.csv")
    args = parser.parse_args()
    return args.db, args.sql, args.csv

def create_connection(path_to_db_file: str) -> sqlite3.Connection:
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(path_to_db_file)
        return conn
    except Error as e:
        print(e)
    return conn

def get_sql(file_path: str) -> str:
    """retrieve the SQL commands from a text file
    @param: file_path - the path to the text file
    @return: str - a string containing the contents of the file"""
    fd = open(file_path, 'r')
    sql = fd.read()
    fd.close()
    return sql

def main() -> None:
    path_to_db, path_to_sql, path_to_csv = get_paths()
    conn = create_connection(path_to_db)
    sql = get_sql(path_to_sql)
    
    if sql == "-- Add your SQL here" or sql == "":
        print("Error: Add your SQL to the sql/fashion_magazines.sql file before running.")
        exit(1)
    
    if conn is not None:
        # Update the SQL query here
        sql = """
        SELECT
            c.customer_name AS Customer,
            printf("$%.2f", SUM(s.price_per_month * s.subscription_length)) AS "Amount Due"
        FROM
            customers c
        JOIN
            orders o ON c.customer_id = o.customer_id
        JOIN
            subscriptions s ON o.subscription_id = s.subscription_id
        WHERE
            o.order_status = 'unpaid'
            AND s.description = 'Fashion Magazine'
        GROUP BY
            c.customer_name;
        """
        
        data = pd.read_sql(sql, conn)

        if len(data) == 0:
            print("Error: Query did not return any results")
            exit(1)
        
        csv_dir = os.path.dirname(path_to_csv)
        if not os.path.exists(csv_dir):
            os.makedirs(csv_dir)
        
        data.to_csv(path_to_csv, index=False)

    else:
        print("Error: Could not connect to the database.")
        exit(1)
        
    conn.close()

if __name__ == "__main__":
    main()
