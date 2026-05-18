# This file contains all functions related to taking input from the user.
# Keeping input logic separate makes the main program cleaner and easier to maintain.

from datetime import datetime  # used for handling date parsing and formatting

# standard date format used across the project
date_format = "%d-%m-%Y"

# mapping short user input → full category names
# this ensures consistency in stored data
CATEGORIES = {
    "I": "Income",
    "E": "Expense"
}


def get_date(prompt, allow_default=False):
    """
    This function asks the user for a date input.

    Parameters:
    - prompt: message shown to the user (makes function reusable)
    - allow_default: if True, user can press Enter to use today's date

    Returns:
    - date string in format dd-mm-yyyy
    """

    # take input from user
    date_str = input(prompt)

    # if default is allowed and user presses Enter (empty input)
    if allow_default and not date_str:
        # return today's date formatted properly
        return datetime.today().strftime(date_format)

    try:
        # try converting input string → datetime object
        valid_date = datetime.strptime(date_str, date_format)

        # convert back to string in correct format (ensures consistency)
        return valid_date.strftime(date_format)

    except ValueError:
        # if user enters wrong format (like 2026/05/01 or invalid date)
        print("Invalid date format!! Please enter the date in dd-mm-yyyy")

        # recursively call function again until valid input is given
        return get_date(prompt, allow_default)


def get_amount():
    """
    This function takes amount input from user.

    Ensures:
    - input is a number
    - value is greater than 0

    Returns:
    - float value of amount
    """

    try:
        # convert input to float
        amount = float(input("Enter the amount: "))

        # check if amount is valid (positive number)
        if amount <= 0:
            raise ValueError("Amount must be greater than zero")

        return amount

    except ValueError as e:
        # handles both invalid number and negative value
        print(e)

        # retry until valid input is given
        return get_amount()


def get_category():
    """
    This function takes category input.

    User enters:
    - 'I' for Income
    - 'E' for Expense

    Returns:
    - full string ("Income" or "Expense")
    """

    # take input and convert to uppercase for consistency
    category = input("Enter the category ('I' for Income or 'E' for Expense): ").upper()

    # check if input is valid
    if category in CATEGORIES:
        return CATEGORIES[category]

    # invalid input case
    print("Invalid category!! Please enter from I or E only!!")

    # retry until valid input
    return get_category()


def get_description():
    """
    This function takes an optional description.

    No validation needed because it's free text.
    """
    return input("Enter any description(optional): ")

