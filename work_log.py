import csv
import datetime
import os
import re
import sys
from collections import OrderedDict

# Global Variables

DATE_FORMAT = "%d-%m-%Y"
FILE_NAME = "work_log.csv"


class Task(object):
    """ Initiates tasks"""
    def __init__(self):
        super(Task, self).__init__()
        clear_screen()
        self.add_task_name()
        clear_screen()
        self.add_task_date()
        clear_screen()
        self.add_task_duration()
        clear_screen()
        self.add_task_notes()

    def add_task_name(self):
        """ Prompts user for task name """
        while True:
            task_name = input("Please enter the title of your task?:  ")
            if len(task_name) == 0:
                clear_screen()
                print("Task name cannot be empty. Please try again.")
                continue
            else:
                self.task_name = task_name
                break

    def add_task_date(self):
        """ Prompts user for task date """
        while True:
            task_date = input("Please enter the date of your task in "
                              "DD-MM-YYYY format:  ")
            try:
                task_date = datetime.datetime.strptime(task_date, DATE_FORMAT)
            except ValueError:
                clear_screen()
                print("Sorry, {} is not a valid date.".format(task_date))
                continue
            else:
                self.task_date = task_date.strftime(DATE_FORMAT)
                break

    def add_task_duration(self):
        """ Prompts user for duration of task """

        while True:
            task_duration = input("Please enter the duration of your task in "
                                  "minutes:  ")
            try:
                task_duration = int(task_duration)
            except ValueError:
                clear_screen()
                print("Not a valid number of minutes. Please try again")
                continue
            else:
                self.task_duration = task_duration
                break

    def add_task_notes(self):
        """ Prompts user for notes on task (optional) """
        notes_option = input("Do you wish to add some notes about "
                             "this task? Y/N  ")

        if notes_option.upper() == "Y":
            clear_screen()
            task_notes = input("Add notes:  ")
            self.task_notes = task_notes
        else:
            self.task_notes = " "

    def __str__(self):
        """ Returns task in str format for use"""
        return """"\
        \nTask: {}\
        \nDate: {}\
        \nDuration: {}\
        \nNotes: {}
        """.format(self.task_name,
                   self.task_date,
                   self.task_duration,
                   self.task_notes)


class WorkLog(object):

    def add_task(self, task):
        """ Adds a task to the CSV file """
        new_task = {'Task name': task.task_name,
                    'Date': task.task_date,
                    'Duration': task.task_duration,
                    'Notes': task.task_notes}
        # Checking for duplicates
        new_task_ord = OrderedDict(new_task)
        new_task_ord['Duration'] = str(new_task_ord['Duration'])
        existing_tasks = self.fetch_tasks()
        for existing_task in existing_tasks:
            if new_task_ord == existing_task:
                clear_screen()
                input("This task already exists. "
                      "Task has not been added. Please try again.\n"
                      "Press any button to go back to the main menu.")
                self.main_menu()
        else:
            with open(FILE_NAME, 'a', newline='') as csvfile:
                fieldnames = ['Task name', 'Date', 'Duration', 'Notes']
                file_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                file_writer.writerow(new_task)
            clear_screen()
            input("Task saved! Press any button to continue.  ")
            clear_screen()
            self.main_menu()

    def fetch_tasks(self):
        """ Finds all the entries in work log and returns for searching"""
        with open(FILE_NAME, 'a+') as csvfile:
            csvfile.seek(0)
            fieldnames = ['Task name', 'Date', 'Duration', 'Notes']
            reader = csv.DictReader(csvfile, fieldnames=fieldnames)
            tasks = list(reader)
            return tasks

    def search_menu(self):
        """ Menu for user to search work log"""
        tasks = self.fetch_tasks()
        clear_screen()
        if len(tasks) == 0:
            input("Sorry! There are no tasks to search. "
                  "Press any button to go back to the "
                  "main menu to add some!")
            self.main_menu()
        else:
            ''' Menu for the search options '''
            print("""SEARCH
            Please choose how you would like to search.
            A) View all entries
            B) Exact date
            C) Range of dates
            D) Task duration
            E) Exact search
            F) Pattern search
            G) Back to main menu
            H) QUIT""")
            pass

            while True:
                choice = input("Please choose an option. ")

                if choice.upper() == "A":
                    self.view_all()
                    break
                elif choice.upper() == "B":
                    self.search_by_exact_date()
                    break
                elif choice.upper() == "C":
                    self.search_by_date_range()
                    break
                elif choice.upper() == "D":
                    self.search_by_duration()
                    break
                elif choice.upper() == "E":
                    self.search_by_exact()
                    break
                elif choice.upper() == "F":
                    self.search_by_regex()
                    break
                elif choice.upper() == "G":
                    self.main_menu()
                    break
                elif choice.upper() == "H":
                    quit()
                    break
                else:
                    print("Not a valid choice. Please try again.")
                    continue

    def print_tasks(self, tasks):

        clear_screen()

        index = 0
        while True:
            pagination = ['[E]dit entry', '[D]elete entry', '[N]ext',
                          '[P]revious', '[B]ack to search menu.']
            task = tasks[index]
            print("Task Name: {}\nDate: {} \nDuration: {} minutes\n"
                  "Notes: {}\n".format(
                    task['Task name'],
                    task['Date'],
                    task['Duration'],
                    task['Notes']))
            if index == 0:
                pagination.remove("[P]revious")
            if index == len(tasks) - 1:
                pagination.remove("[N]ext")

            options = ', '.join(pagination)
            print("Entry {} of {}.".format(index + 1, len(tasks)))
            print(options)
            navigation = input(">")

            # Controls index count and continues in loop

            if navigation.lower() in "npbed" and navigation.upper() in \
                    options:
                if navigation.lower() == "n":
                    clear_screen()
                    index += 1
                    continue
                elif navigation.lower() == "p":
                    clear_screen()
                    index -= 1
                    continue
                elif navigation.lower() == "b":
                    self.search_menu()
                    break
                elif navigation.lower() == "e":
                    self.edit_task(tasks[index])
                    break
                elif navigation.lower() == "d":
                    confirmation = input("Are you sure? Y/N: ")
                    if confirmation.lower() == "y":
                        self.delete_task(tasks[index])
                        break
                    else:
                        continue
            else:
                print("Try again. Sorry")
                continue

    def view_all(self):
        """ View all entries """
        tasks = self.fetch_tasks()
        self.print_tasks(tasks)

    def find_all_dates(self, tasks):
        """ Find all dates for display on date searches"""
        unique_dates = []
        for task in tasks:
            if task['Date'] not in unique_dates:
                unique_dates.append(task['Date'])
        task_dates = unique_dates
        return task_dates

    def print_dates(self, task_dates):
        """ Prints unique dates """
        print("DATES WITH TASKS")
        for date in task_dates:
            print(date)

    def search_by_exact_date(self):
        """ User can search by exact date """
        clear_screen()
        tasks = self.fetch_tasks()
        task_dates = self.find_all_dates(tasks)
        results = []

        while True:
            self.print_dates(task_dates)
            search_date = input("The above dates have tasks. Please "
                                "enter the date of your task in "
                                "DD-MM-YYYY format:  ")
            try:
                search_date = \
                    datetime.datetime.strptime(search_date, DATE_FORMAT)
            except ValueError:
                print("Sorry, {} is not a valid date.".format(search_date))
                continue
            else:
                for task in tasks:
                    if task['Date'] == search_date.strftime(DATE_FORMAT):
                        results.append(task)
                if len(results) == 0:
                    clear_screen()
                    print("{} not found. "
                          "Please try again.".format(search_date))
                    continue
                else:
                    clear_screen()
                    self.print_tasks(results)
                    break

    def search_by_date_range(self):
        """ Search between two dates """
        clear_screen()
        tasks = self.fetch_tasks()
        results = []

        while True:
            start_date = input("Search between two dates.\n"
                               "Enter the start date to begin in "
                               "DD-MM-YYYY format:   ")
            try:
                start_date = \
                    datetime.datetime.strptime(start_date, DATE_FORMAT)
            except ValueError:
                print("Sorry, {} is not a valid date.".format(start_date))
                continue
            else:
                end_date = input("Enter the end date in "
                                 "DD-MM-YYYY format:   ")
                try:
                    end_date = \
                        datetime.datetime.strptime(end_date, DATE_FORMAT)
                except ValueError:
                    print("Sorry, {} is not a valid date.".format(end_date))
                    continue
                if start_date > end_date:
                    clear_screen()
                    print("Sorry. the start date cannot be after the end "
                          "date. Please try again.")
                    continue
                else:
                    for task in tasks:
                        if ((datetime.datetime.strptime(
                                task['Date'], DATE_FORMAT).timestamp() >=
                             start_date.timestamp()) and
                                (datetime.datetime.strptime(
                                    task['Date'], DATE_FORMAT).timestamp() <=
                                 end_date.timestamp())):
                            results.append(task)
                    if len(results) == 0:
                        print("Sorry. No matches. Please try again.")
                        continue
                    else:
                        clear_screen()
                        self.print_tasks(results)
                        break

    def search_by_duration(self):
        """ Search for the duration of time spent on task"""
        clear_screen()
        tasks = self.fetch_tasks()
        results = []

        while True:
            duration_search = input("Search by duration of task.\n"
                                    "Please enter a number of "
                                    "minutes to search by:   ")
            try:
                duration_search = int(duration_search)
            except ValueError:
                clear_screen()
                print("{} is not a number, please try again."
                      .format(duration_search))
                continue
            else:
                for task in tasks:
                    if int(task['Duration']) == int(duration_search):
                        results.append(task)
                if len(results) == 0:
                    clear_screen()
                    print("Sorry. No matches. Please try again.")
                    continue
                else:
                    clear_screen()
                    self.print_tasks(results)
                    break

    def search_by_exact(self):
        """ Search by exact string"""
        clear_screen()
        tasks = self.fetch_tasks()
        results = []

        while True:
            exact_search = input("This will search the task "
                                 "name and notes for an exact term. "
                                 "Please enter:   ")

            for task in tasks:
                if (re.search(exact_search, task['Task name']) or
                        re.search(exact_search, task['Notes'])):
                    results.append(task)
            if len(results) == 0:
                clear_screen()
                print("Sorry. No matches. Please try again.")
                continue
            else:
                clear_screen()
                self.print_tasks(results)
                break

    def search_by_regex(self):
        """ Search by regex pattern"""
        clear_screen()
        tasks = self.fetch_tasks()
        results = []

        while True:
            regex_search = input("This will search regular expression. "
                                 "Please enter:   ")
            try:
                regex_search = re.compile(regex_search)
            except re.error():
                print("Not a valid regular expression. Try again.")
                continue
            for task in tasks:
                if (re.search(regex_search, task['Task name']) or
                        re.search(regex_search, task['Date']) or
                        re.search(regex_search, task['Duration']) or
                        re.search(regex_search, task['Notes'])):
                    results.append(task)
            if len(results) == 0:
                clear_screen()
                print("Sorry. No matches. Please try again.")
                continue
            else:
                clear_screen()
                self.print_tasks(results)
                break

    def edit_task(self, old_task):
        """ Edit a particular task"""
        clear_screen()
        tasks = self.fetch_tasks()
        all_tasks = []
        print()
        for task in tasks:
            if task != old_task:
                all_tasks.append(task)

        while True:
            while True:
                print("Old task name: {}\n".format(old_task['Task name']))
                task_name = input("Please enter a new task name:  ")
                if len(task_name) == 0:
                    print("Task name cannot be empty. Please try again.")
                    continue
                else:
                    old_task['Task name'] = task_name
                    break
            # Date
            clear_screen()
            while True:
                print("Old date: {}\n".format(old_task['Date']))
                task_date = input("Please enter a new date in "
                                  "DD-MM-YYYY format:  ")
                try:
                    task_date = \
                        datetime.datetime.strptime(task_date, DATE_FORMAT)
                except ValueError:
                    print("Sorry, {} is not a valid date.".format(task_date))
                    continue
                else:
                    old_task['Date'] = task_date.strftime(DATE_FORMAT)
                    break
            # Duration
            clear_screen()
            print("Old duration of task: {}\n".format(old_task['Duration']))
            while True:
                task_duration = input("Please enter a duration of your task "
                                      "in minutes:  ")
                try:
                    task_duration = int(task_duration)
                except TypeError:
                    print("Not a valid number. Please try again")
                    continue
                else:
                    old_task['Duration'] = task_duration
                    break
            # Notes
            clear_screen()
            print("Old notes: {}\n".format(old_task['Notes']))
            task_notes = input("Please enter task notes. (Optional):  ")
            if len(task_notes) == 0:
                task_notes = " "
            else:
                old_task['Notes'] = task_notes

            old_task['Duration'] = str(old_task['Duration'])
            # Checks for duplicate
            for task in tasks:
                if task == old_task:
                    clear_screen()
                    print("Sorry. This entry already exists. Please try again")
                    input("Press any button to continue")
                    clear_screen()
                    continue
            else:
                all_tasks.append(old_task)
                with open(FILE_NAME, 'w') as outfile:
                    fp = csv.DictWriter(outfile, all_tasks[0].keys())
                    fp.writerows(all_tasks)

                clear_screen()
                input("Task updated. Press any button to continue.")
                self.main_menu()

    def delete_task(self, task_to_delete):
        """ Delete a particular task"""
        clear_screen()
        tasks = self.fetch_tasks()
        remaining_tasks = []
        # Checks for duplicates
        for task in tasks:
            if task != task_to_delete:
                remaining_tasks.append(task)

        # Deletes file, writes nothing to file if number of entries is zero
        with open(FILE_NAME, 'w') as outfile:
            if len(remaining_tasks) > 0:
                fp = csv.DictWriter(outfile, remaining_tasks[0].keys())
                fp.writerows(remaining_tasks)
            else:
                fp = csv.DictWriter(outfile, "")
                fp.writerows("")

        clear_screen()
        input("Task deleted. Press any button to continue.")
        self.main_menu()

    def main_menu(self):
        """ Main menu"""
        clear_screen()
        print("""WORK LOG MAIN MENU
        Please choose an option.
        A) Add new task
        B) Search existing tasks
        C) QUIT""")

        while True:
            choice = input(">  ")
            if choice.upper() == "A":
                task = Task()
                self.add_task(task)
                break
            elif choice.upper() == "B":
                self.search_menu()
                break
            elif choice.upper() == "C":
                quit()
            else:
                print("Choice not recognised, please try again")
                continue

    def __init__(self):
        super(WorkLog, self).__init__()
        self.main_menu()


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def quit():
    sys.exit()


if __name__ == "__main__":
    WorkLog()
