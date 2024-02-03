from datetime import datetime
from plyer import notification
import schedule
import time
import csv
import os


def main():
    # Specify full path to the CSV file
    csv_file_path = os.path.abspath("main.csv")
    
    # List of alert times in 24-hour format
    alert_times = read_file(csv_file_path)
    update_dates(csv_file_path)

    # Schedule alerts for each time in the list
    for alert_time in alert_times:
        schedule.every().day.at(alert_time.get("Next_pill")).do(lambda pill_name=alert_time.get("Pill_Name"): alert(pill_name))

    #main loop to run schedule
    while True:
        schedule.run_pending()
        time.sleep(1)


def alert(pill_name):
    """
    setting for alert

    Args:
        pill_name (str): name of the medicine to include in the message

    Return:
        nothing
    """
    # Customize the notification message and title
    message = "It's time for your {} Pill!".format(pill_name)
    title = "Reminder"
    
    # Display the notification
    notification.notify(
        title=title,
        message=message,
        app_icon="./images/pill.ico",
        timeout=10,
    )


def read_file(file_path):
    """
    read the csv file with all the data

    Args:
        file_path (str): path for the "main.csv" file

    Return:
        a list of dictionaries
    """
    list_of_dicts = []

    # Use the provided file path
    with open(file_path) as file:
        reader = csv.DictReader(file)
        for line in reader:
            list_of_dicts.append(line)

    return list_of_dicts


def update_dates(csv_file_path):
    """
    thi function will read the csv file and get the current time then pass all these value to the get_time_update()

    Args:
        csv_file_path (str): path to "main.csv" file

    Return:
        Nothing, will call write_new_dates()
    """

    #reading csv file
    timing_dict_list = read_file(csv_file_path)

    # getting current time and split it to get the time portion
    date_now = str(datetime.now()).split()

    # get the hour only out of the whole time
    hour = date_now[1][:2]
    minutes = date_now[1][3:5]


    # calling get_time_update() with the dict, hour, minutes values
    new_dates_dict = get_time_updates(timing_dict_list, hour, minutes)

    # write the updated data
    write_new_dates(new_dates_dict)



def get_time_updates(timing_dict_list, hour, minutes):
    """
    this function will use the current hour, minuet and compare that to the timing on the dict passed with it and if th time passed it will update the value accordingly

    Args:
        timing_dict_list (list of dicts): list of dicts got from the csv file
        hour (str): current hour
        minutes (str): current minuet

    Return:
        updated dictionary
    """
    for item in timing_dict_list:
        for key in item.keys():
            if key == "Starting_time":
                if int(hour) >= (int(item["Next_pill"][:2])) and int(minutes) > int(item["Next_pill"][3:5]):
                    item[key] = item["Next_pill"]
                    next = (int(item["Next_pill"][:2]) + int(item["Dose"])) % 24
                    if len(str(next)) < 2:
                        next = "0" + str(next)
                    item["Next_pill"] = str(next) + ":" + item["Next_pill"][-2:]

    return timing_dict_list


def write_new_dates(new_dates_dict):
    """
    write a dictionary to the main csv file

    Args:
        new_dates_dict (dict): new medicine list of dictionaries passed from the add medicine function

    Return:
        nothing
    """
    field_names = ["Pill_Name", "Starting_time", "Next_pill", "Dose"]
    file_path = os.path.abspath("main.csv")

    # Check if the file exists
    # file_exists = os.path.exists(file_path)

    # Open the CSV file in write mode and write new data
    with open(file_path, "w", newline="") as file:
        csv_writer = csv.DictWriter(file, fieldnames=field_names)

        # write header
        csv_writer.writeheader()

        # Write the data rows
        for row in new_dates_dict:
            csv_writer.writerow(row)


if __name__ == "__main__":
    main()
