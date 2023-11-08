import os
import json
import datetime


# The user data is stored in the JSON file format.
user_data = {}

# This use to track the logged-in user.
logged_in_user = None  

# Dictionary to store important file passwords.
important_file_passwords = {}

# Function to load user data from a JSON file.
def load_user_data():
    try:
        with open("user_data.json", "r") as file:
            user_data.update(json.load(file))
    except FileNotFoundError:
        pass

# Function to save user data to a JSON file
def save_user_data():
    with open("user_data.json", "w") as file:
        json.dump(user_data, file)

# Function to register a new user
def SignUp():
    while True:
        username = input("\nEnter a username: ")
        if username in user_data:
            print("Username already exists.")
        else:
            break

    password = input("\nEnter a password: ")  
    user_data[username] = password
    save_user_data()
    print("Account created successfully. You can now log in.")

# Function to log in with an existing username and password
def login():
    global logged_in_user

    if logged_in_user:
        print(f"Already logged in as {logged_in_user}")
        return

    if not user_data:
        print("\nUser is not registered.")
        return

    username = input("\nEnter your username: ")
    password = input("Enter your password: ")  

    if username in user_data and user_data[username] == password:
        logged_in_user = username
        print(f"\nLogin successful. Welcome, {username}!")
    else:
        print("\nLogin failed. Please check your username and password.")

# Function to log out
def logout():
    global logged_in_user
    logged_in_user = None
    print("\nLogged out successfully.")

# Function to rename the username
def rename_username():
    if not user_data:
        print("\nUser is not registered.")
        return

    current_username = input("\nEnter your current username: ")

    if current_username not in user_data:
        print("\nPlease enter a valid username.")
        return

    new_username = input("\nEnter your new username: ")
    user_data[new_username] = user_data.pop(current_username)
    save_user_data()
    print("\nUsername updated successfully.")

# Function to reset the password by entering the current password
def reset_password():
    if not user_data:
        print("\nUser is not registered.")
        return

    username = input("\nEnter your username: ")

    if username in user_data:
        current_password = input("\nEnter your current password: ")  

        if user_data[username] == current_password:
            new_password = input("Enter your new password: ")  
            user_data[username] = new_password  
            save_user_data()
            print("\nPassword reset successfully.")
        else:
            print("\nCurrent password is incorrect.")
    else:
        print("\nPlease enter a valid username.")

# File Management Functions
def create_file(file_name):
    if not logged_in_user:
        print("\nPlease log-in to access the file management.")
        return

    is_important = input("\nIs this file important? (yes/no): ").lower() == "yes"
    if is_important:
        password = input("Enter the password for the important file: ") 
        important_file_passwords[file_name] = password

    file = open(file_name, 'w')
    print(f"\nFile '{file_name}' Created successfully.")
    file.close()

def read_file(file_name):
    if not logged_in_user:
        print("\nPlease log-in to access the file management.")
        return

    if file_name in important_file_passwords:
        password = input("\nEnter the password for the important file: ")  
        if important_file_passwords[file_name] != password:
            print("\nIncorrect password.")
            return

    if os.path.exists(file_name):
        file = open(file_name, 'r')
        content = file.read()
        print(f"\nContents of '{file_name}':\n{content}")
        file.close()
    else:
        print(f"\nFile '{file_name}' not found.")

def append_file(file_name, content):
    if not logged_in_user:
        print("\nPlease log-in to access the file management.")
        return

    if file_name in important_file_passwords:
        password = input("\nEnter the password for the important file: ")  
        if important_file_passwords[file_name] != password:
            print("Incorrect password.")
            return

    file = open(file_name, 'a')
    file.write(content + '\n')
    print(f"\nContent appended to '{file_name}' successfully.")
    file.close()

def delete_file(file_name):
    if not logged_in_user:
        print("\nPlease log-in to access the file management.")
        return

    if file_name in important_file_passwords:
        password = input("\nEnter the password for the important file: ")  
        if important_file_passwords[file_name] != password:
            print("Incorrect password.")
            return

    if os.path.exists(file_name):
        os.remove(file_name)
        print(f"\nFile '{file_name}' deleted successfully.")
    else:
        print(f"\nFile '{file_name}' not found.")

# Task Management Functions
tasks = []

def add_task():
    task = input("\nEnter a task: ")
    is_important = input("Is this task important? (yes/no): ").lower() == "yes"
    creation_date = datetime.date.today().strftime("%Y-%m-%d")
    tasks.append({"task": task, "important": is_important, "creation_date": creation_date, "completed": False})
    print("\nTask added!")

def display_tasks():
    if not tasks:
        print("\nYour to-do list is empty.")
    else:
        print("\nTo-Do List:")
        for index, task_data in enumerate(tasks, start=1):
            importance = "Important" if task_data["important"] else "Not Important"
            completion_status = "Completed" if task_data["completed"] else "Not Completed"
            print(f" {index}.{task_data['task']} \n--{importance} \n--Created on: {task_data['creation_date']} \n--{completion_status}")

def mark_completed():
    if not tasks:
        print("\nYour to-do list is empty.")
    else:
        try:
            task_number = int(input("\nEnter the task number to mark as completed: "))
            if 1 <= task_number <= len(tasks):
                tasks[task_number - 1]["completed"] = True
                print("\nTask marked as completed.")
            else:
                print("Invalid task number.")
        except ValueError:
            print("Invalid input. Please enter a valid task number.")

def remove_task():
    if not tasks:
        print("\nYour to-do list is empty.")
    else:
        try:
            task_number = int(input("\nEnter the task number to remove: "))
            if 1 <= task_number <= len(tasks):
                removed_task = tasks.pop(task_number - 1)
                print(f"Task '{removed_task['task']}' removed!")
            else:
                print("Invalid task number.")
        except ValueError:
            print("Please enter a valid task number.")

# Main program loop
if __name__ == "__main__":

    # Load user data from the JSON file
    load_user_data()  

    print("\nWelcome to the Task and File Management System!")

    while True:
        if not logged_in_user:
            print("\nUser Management Menu:")
            print("1. Sign Up")
            print("2. Log In")
            print("3. Reset Password")
            print("4. Rename Username")
            print("5. Exit")
            choice = input("\nSelect an option (1/2/3/4/5): ")

            if choice == '1':
                SignUp()
            elif choice == '2':
                login()
            elif choice == '3':
                reset_password()
            elif choice == '4':
                rename_username()
            elif choice == '5':
                break
            else:
                print("\nInvalid choice. Please select 1, 2, 3, 4, or 5.")
        else:
            print("\nMain Menu:")
            print("1. File Management")
            print("2. Task Management")
            print("3. Log Out")
            main_choice = input("\nSelect an option (1/2/3): ")

            if main_choice == '1':
                while True:
                    print("\nFile Management Menu:")
                    print("1. Create File")
                    print("2. Read File")
                    print("3. Append to File")
                    print("4. Delete File")
                    print("5. Go Back") 
                    file_choice = input("\nSelect a file operation (1/2/3/4/5): ")

                    if file_choice == '1':
                        file_name = input("\nEnter the file name: ")
                        create_file(file_name)
                    elif file_choice == '2':
                        file_name = input("Enter the file name: ")
                        read_file(file_name)
                    elif file_choice == '3':
                        file_name = input("Enter the file name: ")
                        content = input("Enter content to append: ")
                        append_file(file_name, content)
                    elif file_choice == '4':
                        file_name = input("Enter the file name: ")
                        delete_file(file_name)
                    elif file_choice == '5':
                        break  
                    else:
                        print("\nInvalid choice. Please select 1, 2, 3, 4, or 5.")
            elif main_choice == '2':
                while True:
                    print("\nTask Management Menu:")
                    print("1. Add a Task")
                    print("2. Display Tasks")
                    print("3. Mark Task as Completed")
                    print("4. Remove a Task")
                    print("5. Go Back")  
                    task_choice = input("\nSelect a task operation (1/2/3/4/5): ")

                    if task_choice == '1':
                        add_task()
                    elif task_choice == '2':
                        display_tasks()
                    elif task_choice == '3':
                        mark_completed()
                    elif task_choice == '4':
                        remove_task()
                    elif task_choice == '5':
                        break  
                    else:
                        print("\nInvalid choice. Please select 1, 2, 3, 4, or 5.")
            elif main_choice == '3':
                logout()
            else:
                print("\nInvalid choice. Please select 1, 2, or 3.")
                



