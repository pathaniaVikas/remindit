
"""
Basic remid me
nothing much here
"""
import csv
import time
import dateutil.parser as dp
import os


def read_csv():
    with open('task_files/reminders.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            yield row


def convert_iso_to_epoch(iso_date):
    parsed_datetime = dp.parse(iso_date)
    return parsed_datetime.timestamp()


def announce(task):
    bash_command = "say " + task
    os.system(bash_command)


def make_a_change(csv_row_dict):
    """
    TODO: Screen will be stuck here, if user does not input anything
    """
    print("Please choose option for this task")
    print("1. Suspend for x hours(we will take x in next input)")
    print("2. Remove this task from list")
    print("3. Mark this task as complete")
    print("4. Increase deadline(will take input in next line)")
    print("*** FOR 2, 3 and 4 you can directly change the csv file also here: \n" +
        "/Users/vikpath/personal_workspace/remindit/sourcecode/remindit/src/app/task_files")

    choice = input("Choice")
    if choice not in ["1", '2', '3', '4']:
        print("wrong choice")
        return 0
    choice = int(choice)
    if choice == 1:
        sleep_time = input("Suspend for how many minutes")
        try:
            return int(sleep_time)
        except Exception("wrong input"):
            return 0
    elif choice == 2:
        print("Not implemented yet")
        return 0
    elif choice == 3:
        # csv_row_dict["status"] = "COMPLETED"
        print("Not implemented yet")
        return 0
    elif choice == 4:
        print("Not implemented yet")
        return 0
    return 0


def write_to_csv(csv_dict_list):
    with open('task_files/reminders.csv', 'w', newline='') as csvfile:
        fieldnames = ["task", "deadline", "estimated_time_in_hours", "status"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for csv_dict in csv_dict_list:
                writer.writerow(csv_dict)

def remind_me():
    """
    Basic function to read from csv file and check tasks which needs to be reminded
    based on if time left is there
    """
    read_csv_gen = read_csv()
    csv_dict_list = []
    sleeptime = 0
    for row in read_csv_gen:
        csv_dict_list.append(row)
        # check if time left is less than estimated time
        estimated_time = row.get("estimated_time_in_hours")
        estimated_time_in_seconds = int(float(estimated_time) * 60 )* 60

        deadline = row.get("deadline")
        deadline_in_seconds = convert_iso_to_epoch(deadline)
        task = row.get("task")
        status = row.get("status")

        current_time_in_seconds = time.time()
        # if deadline is already passed dont remind it: TODO: Change it in future to call out this also
        if deadline_in_seconds < current_time_in_seconds:
            print("Deadline is in past for task: {}".format(task))
            continue

        if status in ["COMPLETED", "IN PROGRESS"]:
            continue

        time_left_for_completion = deadline_in_seconds - current_time_in_seconds

        if time_left_for_completion <= estimated_time_in_seconds:
            print(task)
            print("current time in seconds: ", current_time_in_seconds)
            print("deadline in seconds: ", deadline_in_seconds)
            print("estimated time in seconds: ", estimated_time_in_seconds)
            print("time left for compeltion: ", time_left_for_completion)
            # beep
            announce(task)
            sleeptime = make_a_change(row)
            # this will break the loop over next tasks
            if (sleeptime * 60 > 0):
                break

    # write updated csv
    # Implement someting like incremental changes
    # write_to_csv(csv_dict_list)
    # - 5 seconds as it will sleep for 5 minutes in main
    print("Sleeping for {} seconds".format(sleeptime * 60))
    time.sleep((sleeptime * 60))




if __name__ == '__main__':
    while True:
        remind_me()
        print("Sleeping for {} seconds".format(300))
        time.sleep(300)
