from dataclasses import dataclass
import boto3


@dataclass
class EC2Instance:
    instance_id: str
    ec2 = boto3.client('ec2', region_name='us-east-1')

    def start_instance(self):
        print('Starting instance', self.instance_id)
        self.ec2.start_instances(InstanceIds=[self.instance_id])

    def check_is_running(self, ) -> bool:
        print('Checking if instance is running', self.instance_id)
        response = self.ec2.describe_instance_status(
            InstanceIds=[self.instance_id])
        instances = response.get('InstanceStatuses')
        return len(instances) == 1

    def stop_instance(self):
        print('Stopping instance', self.instance_id)
        self.ec2.stop_instances(InstanceIds=[self.instance_id])


@dataclass
class EC2Helper:
    ec2 = boto3.client('ec2', region_name='us-east-1')

    @classmethod
    def get_instances(self):
        response = self.ec2.describe_instances()
        instances = response.get('Reservations').pop().get('Instances')

        return instances
