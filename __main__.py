"""An AWS Python Pulumi program"""

import pulumi
from pulumi_aws import s3, ec2


# Create an AWS resource (S3 Bucket)
bucket = s3.Bucket('my-bucket')

# Export the name of the bucket
pulumi.export('bucket_name', bucket.id)


# Create a security group
sg = ec2.SecurityGroup("Webserver-sg", description="Security group for webserver")

# Allow SSH traffic
allow_ssh = ec2.SecurityGroupRule(
    "allow-ssh",
    type="ingress",
    from_port=22,
    to_port=22,
    protocol="tcp",
    cidr_blocks=["0.0.0.0/0"],  # Allow traffic from any IPv4 address
    security_group_id=sg.id
)

# Allow HTTP traffic
allow_http = ec2.SecurityGroupRule(
    "allow-http",
    type="ingress",
    from_port=80,
    to_port=80,
    protocol="tcp",
    cidr_blocks=["0.0.0.0/0"],  # Allow traffic from any IPv4 address
    security_group_id=sg.id
)

# Allow all egress traffic
allow_egress = ec2.SecurityGroupRule(
    "allow-egress",
    type="egress",
    from_port=0,
    to_port=0,
    protocol="-1",
    cidr_blocks=["0.0.0.0/0"],  # Allow all outgoing traffic
    security_group_id=sg.id
)
instance_names = ["web1","web2", "web3"]
output_public_Ip= []

#Loop over the  array to create  Ec2 instance
for instance in instance_names:
    
# Create an AWS resource (EC2 instance)
    ec2_instance = ec2.Instance(
        instance,
        ami="ami-080e1f13689e07408",
        instance_type="t3.nano",
        key_name="Linux5",
        vpc_security_group_ids=[sg.id],
        tags={"Name": instance}
    )
    output_public_Ip.append(ec2_instance.public_ip)

# Export the Public IP of the server
pulumi.export('Public_Ip', output_public_Ip)

#pulumi.export('Public_Ip', ec2_instance.public_ip)
#pulumi.export('instance_url', ec2_instance.public_dns )
#pulumi.export('instance_url', pulumi.Output.concat("http://", ec2_instance.public_dns))

