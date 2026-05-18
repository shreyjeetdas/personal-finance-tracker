import pandas as pd              # used for handling CSV data easily
import csv                      # used for writing data into CSV manually
from datetime import datetime   # used to work with date objects
from data_entry import get_amount, get_category, get_date, get_description  # user input functions
import matplotlib.pyplot as plt # used for plotting graphs


# This class handles all CSV-related operations (read, write, filter)
class CSV:
    CSV_FILE = "data/finance_data.csv"   # file where all data is stored
    COLUMNS = ["DATE", "AMOUNT", "CATEGORY", "DESCRIPTION"]  # column structure
    date_format = "%d-%m-%Y"        # expected date format

    @classmethod
    def initialise_csv(cls):
        """
        This function ensures that the CSV file exists.
        If it doesn't exist, it creates a new one with proper columns.
        """
        try:
            pd.read_csv(cls.CSV_FILE)  # try reading the file
        except FileNotFoundError:
            # if file not found → create empty dataframe with required columns
            df = pd.DataFrame(columns=cls.COLUMNS)

            # save it as a CSV file
            df.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def add_entry(cls, DATE, AMOUNT, CATEGORY, DESCRIPTION):
        """
        Adds a new transaction entry into the CSV file.
        """

        # make sure CSV exists before writing
        cls.initialise_csv()

        # create a dictionary (row) to insert into CSV
        new_entry = {
            "DATE": DATE,
            "AMOUNT": AMOUNT,
            "CATEGORY": CATEGORY,
            "DESCRIPTION": DESCRIPTION,
        }

        # open file in append mode ("a") so new data is added at the end
        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)

            # write one row into CSV
            writer.writerow(new_entry)

        print("Entry added successfully!!")

    @classmethod
    def get_transactions(cls, start_date, end_date):
        """
        Reads CSV data and filters transactions between given dates.
        Also calculates summary (income, expense, savings).
        """

        # read CSV into pandas dataframe
        df = pd.read_csv(cls.CSV_FILE)

        # convert DATE column from string → datetime object
        df["DATE"] = pd.to_datetime(df["DATE"], format=cls.date_format)

        # convert user input string → datetime object
        start_date = datetime.strptime(start_date, cls.date_format)
        end_date = datetime.strptime(end_date, cls.date_format)

        # create a filter condition (mask)
        mask = (df["DATE"] >= start_date) & (df["DATE"] <= end_date)

        # apply mask → get only required rows
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print("No transaction found in the given date range!!")

        else:
            print(
                f"\nTransactions from {start_date.strftime(cls.date_format)} to {end_date.strftime(cls.date_format)}"
            )

            # print dataframe nicely (formatted dates)
            print(
                filtered_df.to_string(
                    index=False,
                    formatters={
                        "DATE": lambda x: x.strftime(cls.date_format)
                    },
                )
            )

            # calculate total income
            total_income = filtered_df[
                filtered_df["CATEGORY"] == "Income"
            ]["AMOUNT"].sum()

            # calculate total expense
            total_expense = filtered_df[
                filtered_df["CATEGORY"] == "Expense"
            ]["AMOUNT"].sum()

            print("\n:::::SUMMARY:::::")

            print(f"Total Income: {total_income:.2f}/-")
            print(f"Total Expense: {total_expense:.2f}/-")

            # net savings = income - expense
            print(f"Net Savings: {total_income - total_expense:.2f}/-")

        # return dataframe so it can be used for plotting
        return filtered_df


# function to take input and add a transaction
def add():
    CSV.initialise_csv()

    # take user inputs using helper functions
    DATE = get_date(
        "Enter the date of transaction(dd-mm-yyyy) or press enter for today's date: ",
        allow_default=True,
    )
    AMOUNT = get_amount()
    CATEGORY = get_category()
    DESCRIPTION = get_description()

    # store data into CSV
    CSV.add_entry(DATE, AMOUNT, CATEGORY, DESCRIPTION)


# function to plot income vs expense graph
def plot_transactions(df):
    """
    Takes filtered dataframe and plots daily income vs expense.
    """

    # create a copy to avoid modifying original data
    df = df.copy()

    # set DATE column as index (required for resampling)
    df.set_index("DATE", inplace=True)

    # filter only income rows, then resample daily and sum amounts
    income_df = (
        df[df["CATEGORY"] == "Income"]
        .resample("D")     # group data by each day
        .sum()             # sum values for same day
    )

    # same for expenses
    expense_df = (
        df[df["CATEGORY"] == "Expense"]
        .resample("D")
        .sum()
    )

    # create plot
    plt.figure(figsize=(10, 5))

    # plot income line
    plt.plot(income_df.index, income_df["AMOUNT"], label="Income", color="g")

    # plot expense line
    plt.plot(expense_df.index, expense_df["AMOUNT"], label="Expense", color="r")

    # labels and title
    plt.xlabel("DATE")
    plt.ylabel("AMOUNT")
    plt.title("Income and Expenses Over Time")

    # legend + grid
    plt.legend()
    plt.grid(True)

    # show graph
    plt.show()


# main program loop (CLI interface)
def main():
    while True:
        print("\n1. Add a new Transaction: ")
        print("2. View transactions and summary within a date range")
        print("3. Exit")

        choice = input("Enter your choice(1-3): ")

        if choice == "1":
            add()

        elif choice == "2":
            start_date = get_date("Enter the start date (dd-mm-yyyy): ")
            end_date = get_date("Enter the end date (dd-mm-yyyy): ")

            # get filtered data
            df = CSV.get_transactions(start_date, end_date)

            # ask user if they want a plot
            if input("Do you want to see a plot? (y/n): ").lower() == "y":
                plot_transactions(df)

        elif choice == "3":
            print("Exiting...")
            break

        else:
            print("Invalid Choice!!! Enter 1, 2 or 3.")


# ensures main() runs only when file is executed directly
if __name__ == "__main__":
    main()

