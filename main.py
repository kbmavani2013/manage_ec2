import boto3
import datetime
import time

from constants import SLEEP_TIME, REGION, KEY_PAIR, SCHEDULED_DAYS, SCHEDULED_START_HOUR, SCHEDULED_START_MINUTE, \
    SCHEDULED_END_HOUR, SCHEDULED_END_MINUTE
from manage_machine import ManageMachine


def print_menu():
    """This function will print the menu for the human interaction."""
    print("Welcome to EC2 management system:")
    print("1. Launch EC2 instance.")
    print("2. Stop EC2 instance.")
    print("3. Start EC2 instance.")
    print("4. Schedule the running time.")


def take_data_and_create(ec2):
    """This function will take required inputs from the user and create an ec2 instance."""
    ami_id = input("Enter AMI id: ")
    if not ami_id:
        print("AMI id should not be blank.")
        return
    min_number = input("Enter minimum number (enter to 1): ")
    if not min_number or not min_number.isdigit():
        min_number = 1
    else:
        min_number = int(min_number)
    print(f"Minimum number is set to {min_number}")
    max_number = input("Enter maximum number (enter to 1): ")
    if not max_number or not max_number.isdigit():
        max_number = 1
    else:
        max_number = int(max_number)
    print(f"Maximum number is set to {max_number}")
    inst_type = input("Enter instance type: ")
    if not inst_type:
        print("Instance type should not be blank.")
        return

    instance = ManageMachine(ami_id=ami_id, min_count=min_number, max_count=max_number, instance_type=inst_type)
    instance.create_ec2(ec2, key_pair=KEY_PAIR)


def take_data_and_stop(client):
    """This will take instance id from user and stop that instance."""
    inst_id = input("Enter the instance id: ")
    if not inst_id:
        print("Instance id should not be empty.")
        return
    instance = ManageMachine(instance_id=inst_id)
    instance.stop_start_instance(client=client, action='stop')


def take_data_and_start(client):
    """This will take instance id from user and start that instance."""
    inst_id = input("Enter the instance id: ")
    if not inst_id:
        print("Instance id should not be empty.")
        return
    instance = ManageMachine(instance_id=inst_id)
    instance.stop_start_instance(client=client, action='start')


def take_data_and_schedule(client):
    """This method will schedule the start and stop time of the EC2 instances."""
    today = datetime.datetime.utcnow().weekday()

    inst_id = input("Enter the instance id: ")
    if not inst_id:
        print("Instance id should not be empty.")
        return
    instance = ManageMachine(instance_id=inst_id)

    if today in SCHEDULED_DAYS:
        time_now = datetime.datetime.utcnow().time()
        start_time = datetime.time(SCHEDULED_START_HOUR, SCHEDULED_START_MINUTE)
        end_time = datetime.time(SCHEDULED_END_HOUR, SCHEDULED_END_MINUTE)

        if start_time <= time_now <= end_time:
            instance.stop_start_instance(client, action='start')
        else:
            instance.stop_start_instance(client)
    else:
        instance.stop_start_instance(client, action='stop')


def run():
    """Main entry point to start our program."""
    try:
        ec2 = boto3.resource('ec2', region_name=REGION)
        client = boto3.client('ec2', region_name=REGION)
    except Exception as error:
        print(f"Error connecting to AWS: {error}")
        exit(0)

    while True:
        print_menu()
        human_input = input("Enter your choice: ")
        if not human_input or human_input == '0':
            print("Exiting system. Good bye!")
            time.sleep(SLEEP_TIME)
            break
        if human_input == '1':
            print('Creating EC2 instance:')
            take_data_and_create(ec2)
        elif human_input == '2':
            print('Stopping EC2 instance:')
            take_data_and_stop(client)
        elif human_input == '3':
            print('Starting EC2 instance:')
            take_data_and_start(client)
        elif human_input == '4':
            print('Schedule start and stop of EC2 instance:')
            take_data_and_schedule(client)
        else:
            print("Please enter the correct input:")
        time.sleep(SLEEP_TIME)


if __name__ == '__main__':
    run()
