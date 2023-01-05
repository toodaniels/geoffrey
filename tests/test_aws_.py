from aws import EC2Helper


def test_get_instances():
    ec2_helper = EC2Helper()

    instances = ec2_helper.get_instances()
    assert len(instances) == 1
