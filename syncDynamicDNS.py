#!/use/bin/python3
import boto3
import urllib
import os

# Set AWS access for Route 53 changes
# acces key and secret key are passed with ENV variables AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY
# alternatively use an aws/config file?
# aws_user = os.environ.get("AWSUSER")
# aws_password = os.environ.get("AWSPASS")
aws_zone_id = os.environ.get("HOSTED_ZONE_ID")

# Set domain options
dynamic_url = os.environ.get("URL")

# Set action options
get_ip_url = "http://checkip.amazonaws.com/"

# Get current public IP
current_ip = urllib.request.urlopen(get_ip_url).read().decode("utf-8").strip()

# Get current DNS value from AWS
client = boto3.client('route53')
response = client.list_resource_record_sets(
    HostedZoneId=aws_zone_id,
    StartRecordName=dynamic_url,
    StartRecordType="A",
    MaxItems="1"
    )

# Verify URLS match
verify_url = response["ResourceRecordSets"][0]["Name"][:-1]
if (verify_url != dynamic_url):
    exit(0)
    #exit routine due to not matching

# Check IPs
dns_ip = response["ResourceRecordSets"][0]["ResourceRecords"][0]["Value"]
if (dns_ip == current_ip):
    exit(0)
    #exit routine due to no update needed

# Update the IP in Route 53
response = client.change_resource_record_sets(
    ChangeBatch={
        'Changes': [
            {
                'Action': 'UPSERT',
                'ResourceRecordSet': {
                    'Name': dynamic_url,
                    'ResourceRecords': [
                        {
                            'Value': current_ip,
                        },
                    ],
                    'TTL': 300,
                    'Type': 'A',
                },
            },
        ],
        'Comment': 'Dynamic DNS',
    },
    HostedZoneId=aws_zone_id,
)

