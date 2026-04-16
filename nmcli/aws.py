import logging
import boto3
from botocore.exceptions import NoCredentialsError, ClientError

logger = logging.getLogger(__name__)


def get_vpc_info(region: str = "us-east-1") -> list:
    logger.info(f"Fetching VPC data from AWS region: {region}")
    try:
        ec2 = boto3.client("ec2", region_name=region)
        vpcs = ec2.describe_vpcs()["Vpcs"]

        print(f"\n{'VPC ID':<22} {'CIDR':<20} {'DEFAULT':<10} {'STATE'}")
        print("-" * 65)

        for vpc in vpcs:
            name = next(
                (t["Value"] for t in vpc.get("Tags", []) if t["Key"] == "Name"),
                "unnamed"
            )
            print(
                f"{vpc['VpcId']:<22} "
                f"{vpc['CidrBlock']:<20} "
                f"{str(vpc['IsDefault']):<10} "
                f"{vpc['State']}"
            )
        return vpcs

    except NoCredentialsError:
        logger.error("AWS credentials not configured. Run: aws configure")
        return []
    except ClientError as e:
        logger.error(f"AWS API error: {e.response['Error']['Message']}")
        return []


def get_ec2_instances(region: str = "us-east-1") -> list:
    logger.info(f"Fetching EC2 instances in {region}")
    try:
        ec2 = boto3.client("ec2", region_name=region)
        reservations = ec2.describe_instances()["Reservations"]

        instances = []
        print(f"\n{'INSTANCE ID':<22} {'TYPE':<16} {'STATE':<12} {'PUBLIC IP'}")
        print("-" * 65)

        for r in reservations:
            for i in r["Instances"]:
                state = i["State"]["Name"]
                pub_ip = i.get("PublicIpAddress", "N/A")
                print(
                    f"{i['InstanceId']:<22} "
                    f"{i['InstanceType']:<16} "
                    f"{state:<12} "
                    f"{pub_ip}"
                )
                instances.append(i)
        return instances

    except NoCredentialsError:
        logger.error("AWS credentials not configured.")
        return []
    except ClientError as e:
        logger.error(f"AWS API error: {e.response['Error']['Message']}")
        return []
