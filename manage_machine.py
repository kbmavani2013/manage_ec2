import boto3
from constants import ACTIONS


class ManageMachine:
    """This class will help to help in managing EC2 instances.

    Attributes:
        ami_id (str): AMI key to create EC2 instance from.
        min_count (int): Minimum number of instances to roll out.
        max_count (int): Maximum number of instances to roll out.
        instance_type (str): Type of the EC2 instance.
    """

    def __init__(self, ami_id=None, min_count=0, max_count=0, instance_type=None, instance_id=None):
        """constructor to initiate the object"""
        self.ami_id = ami_id
        self.min_count = min_count
        self.max_count = max_count
        self.instance_type = instance_type
        self.instance_id = instance_id

    def create_ec2(self, ec2: boto3.resources.base.ServiceResource, key_pair: str):
        """This method will create the EC2 instance on the AWS console.
        Prerequisites:
            1. Create your IAM or Admin user on AWS console along with the required permissions to create the EC2
                Instances.
            2. Create key_pair on the AWS console and store the same in your local machine.
        """
        try:
            self.instance = ec2.create_instances(
                ImageId=self.ami_id,
                MinCount=self.min_count,
                MaxCount=self.max_count,
                InstanceType=self.instance_type,
                KeyName=key_pair
            )
            self.instance_id = self.instance.id
        except Exception as error:
            print(f'Error while creating the EC2 instance: {error}')

    def stop_start_instance(self, client, action='stop'):
        """This method will start or stop the EC2 instance based on passed action. i.e. 'start' or 'stop'"""
        if action not in ACTIONS:
            return 'Error: Action should be either "start" or "stop"'
        func = client.stop_instances if action == 'stop:' else client.start_instances
        try:
            func(InstanceIds=[self.instance_id])
            print(f"Success action {action} EC2 instance.")
        except Exception as error:
            print(f'Error while action {action} the instance: {error}')
