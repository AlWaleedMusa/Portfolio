from tabulate import tabulate
import time
import csv
import sys
import os
import re


def main():
    """
    run the program starting with the main prompt
    """
    prompt_menu()


def prompt_menu():
    """
    function that will display a choices table and wait for user input

    Return:
        nothing
    """

    os.system("cls")
    choices = [
        ["", "Choices"],
        ["1", "Add medicine"],
        ["2", "Edit medicine"],
        ["3", "Show medicines"],
        ["Q", "Quit"]
    ]

    # printing the table using print_table function
    print_table(choices)
    user_input = input()

    # validating the user input and make sure its correct if not ask again
    if user_input in ["1", "2", "3", "q"]:
        handle_input(user_input)
    else:
        print("Try a valid choice\n")


def handle_input(choice):
    """
    handel user input and call the corresponding function

    Args:
        choice (str): number passed by the user

    Return:
        nothing
    """
    if choice == "1":
        # calling add_medicine function if input = 1
        new_med = add_medicine()

        #write the new dictionary returned from the add_medicine function to the csv file
        write_csv_appending(new_med)
        re_run()
    elif choice == "2":
        edit_medicine()
        re_run()
    elif choice == "3":
        path = os.path.abspath("main.csv")
        show_medicine(path)
        re_run()
    elif choice.lower() == "q":
        sys.exit()

def re_run():

    while True:
        rerun = input("\nWould you like to do another task (Y/N): ")
        if rerun.upper() == "Y":
            prompt_menu()
            break
        elif rerun.upper() == 'N':
            sys.exit("Get well soon :)")
        else:
            print("Not a valid input")


def add_medicine():
    print("\n* Adding Medicine\n")
    repeat_time_list = [
        ["", "Choices"],
        ["1", "Every 8 Hours"],
        ["2", "Every 12 Hours"],
        ["3", "Other"]
    ]
    new_medicines = []

    try:
        n = int(input("How many medicines are you adding: "))
    except ValueError:
        print("Input must be an integer")
        return new_medicines

    for _ in range(n):
        adding_dict = {}
        medicine_name = input("Enter medicine name to add: ")
        adding_dict["Pill_Name"] = medicine_name.lower().title()

        #get time input for the first pill time
        starting_time = get_valid_time_input()
        adding_dict["Starting_time"] = starting_time

        # print a choice table
        print_table(repeat_time_list)

        # calling get_valid_repeat_time to make sure input is correct
        repeat_time = get_valid_repeat_time_input("Whats the Dose: ")
        adding_dict["Dose"] = repeat_time

        # calling calculate next pill to do as its name
        adding_dict["Next_pill"] = calculate_next_pill(starting_time, repeat_time)

        print("Adding....")
        time.sleep(1)
        print("{} added, Next pill at {}\n".format(medicine_name, calculate_next_pill(starting_time, repeat_time)))
        time.sleep(.5)
        new_medicines.append(adding_dict)

    return new_medicines



def get_valid_time_input():
    """
    ask use to input time for first pill time

    Return:
        a valid time format
    """
    while True:
        starting_time = input("When did you take the first pill: ")

        # call validate_time() to see if input is valid
        validated_time = validate_time(starting_time)
        if validated_time:
            return validated_time
        print("Time format must be in (HH:mm) format")


def validate_time(time):
    """
    validate time input passed from the user to make sure no wrong input is passed

    Args:
        time (str): time format to check
    
    Return:
        a string (hh:mm) and None if match was not found
    """
    pattern = re.compile(r"([01]\d|2[0-3]):([0-5]\d)")
    match = re.fullmatch(pattern, time)

    if match:
        hour, minutes = map(str, match.groups())

        if len(hour) == 1 and hour[0] == "0":
            hour = "0" + hour
        elif len(minutes) < 2 and minutes[0] == "0":
            minutes = "0" + minutes
            
        return "{}:{}".format(hour, minutes)
    else:
        return None


def get_valid_repeat_time_input(prompt):
    """
    check the user input and make sure its a valid input

    Argv:
        prompt (str): string passed by the user

    Return string repeat_time if input is valid
    """
    while True:
        try:
            repeat_time = int(input(prompt))
            if repeat_time in [1, 2]:
                repeat_time = 8 if repeat_time == 1 else 12
                return repeat_time
            elif repeat_time > 2:
                repeat_time = int(input("Custom time: "))
                return repeat_time
            else:
                print("Invalid choice")
        except ValueError:
            print("Must be an integer")


def calculate_next_pill(start, repeat):
    """
    a function that calculate the time for the next pill deponing on the repeating provided by the user input

    Args:
        start (str): time when first pill was taken
        repeat (int): after hoe many hours the next pill should be

    Return:
        string of the next pill time
    """

    # calculate the next time pill and return it as a string
    if isinstance(repeat, int):
        hour, minuet = str(start).split(":")
        next_pill = (int(hour) + repeat) % 24
        
        if len(str(next_pill)) < 2:
            return "0{}:{}".format(next_pill, minuet)
        return "{}:{}".format(next_pill, minuet)


def show_medicine(file_path):
    """
    read a csv file and print the data as a table

    Args:
        file_path (str): path to the file to read

    Return:
        nothing
    """
    with open(file_path) as file:
        reader  = csv.DictReader(file)
        print("\n* Medicines table")
        print(tabulate(reader, headers="keys", tablefmt="mixed_grid"))

def edit_medicine():

    edit_options_list = [
        ["", "Available Edits"],
        ["1", "Name"],
        ["2", "Starting time"],
        ["3", "Dose"]
    ]

    print_table(edit_options_list)
    while True:

        choice = input("What would you like to edit: ")
        if choice in ["1", "2", "3"]:
            handel_choices(choice)
            break
        else:
            print("Enter a valid choice\n")

def handel_choices(choice):
    
    if choice == "1":
        if change_name():
            time.sleep(.5)
            print("\nName Changed successfully")
    elif choice == "2":
        if change_starting_time():
            time.sleep(.5)
            print("\nStarting time Changed successfully")
    elif choice == "3":
        ...

def change_name():

    path = os.path.abspath("main.csv")

    while True:
        name = input("\nMedicine name: ")

        # call validate_name() to see if input is valid
        if validate_name(name, path):
            validated_name = validate_name(name,path)
            break
        else:
            print("Invalid medicine name")

    new_name = input("New name: ").strip()
    data = read_csv(path)

    for row in data:
        if row["Pill_Name"] == validated_name:
            row["Pill_Name"] = new_name.title()

    write_csv(data, path)
    return True
        

            
def read_csv(file_path):
    data = []
    with open(file_path, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data
    

def write_csv(data, file_path):

    with open(file_path, mode='w', newline='') as file:
        field_names = data[0].keys() if data else []
        writer = csv.DictWriter(file, fieldnames=field_names)

        writer.writeheader()
        for row in data:
            writer.writerow(row)
    

def validate_name(prompt, path):
    
    with open(path, "r") as file:
        reader = csv.DictReader(file)
        for line in reader:
            for key, value in line.items():
                if value == prompt.strip().title() and key == "Pill_Name":
                    return prompt.title()
        return None


def change_starting_time():
    path = os.path.abspath("main.csv")

    while True:
        name = input("\nMedicine name: ")

        if validate_name(name, path):
            # call validate_time() to see if input is valid
            validated_name = validate_name(name, path)
            break
        else:
            print("Invalid medicine name")

    while True:
        new_starting_time = input("New starting time (HH:mm): ").strip()

        if validate_time(new_starting_time):
            new_starting_time = validate_time(new_starting_time)
            break
        else:
            print("Invalid time format (HH:mm)")

    data = read_csv(path)

    for row in data:
        if row["Pill_Name"] == validated_name:
            row["Starting_time"] = new_starting_time
            row["Next_pill"] = calculate_next_pill(new_starting_time, int(row["Dose"]))

    write_csv(data, path)
    return True



def print_table(list_of_lists):
    """
    print a table from a list of list using tabulate

    Args:
        list_of_lists (matrix): a list of lists to print a table from

    Return:
        nothing
    """
    header = list_of_lists[0]
    data = list_of_lists[1:]
    print("\n" + tabulate(data, headers=header, tablefmt="mixed_grid"))


def write_csv_appending(input_dict):
    """
    write a dictionary to the main csv file

    Args:
        input_dict (list): new medicine list of dictionaries passed from the add medicine function

    Return:
        nothing
    """
    field_names = ["Pill_Name", "Starting_time", "Next_pill", "Dose"]
    file_path = os.path.abspath("main.csv")

    # Check if the file exists
    file_exists = os.path.exists(file_path)

    # Open the CSV file in append mode create it if it doesn't exist
    with open(file_path, "a", newline="") as file:
        csv_writer = csv.DictWriter(file, fieldnames=field_names)

        # Write the header only if the file is newly created
        if not file_exists:
            csv_writer.writeheader()

        # Write the data rows
        for row in input_dict:
            csv_writer.writerow(row)


if __name__ == "__main__":
    main()
