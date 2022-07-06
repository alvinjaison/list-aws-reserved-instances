import boto3

session = boto3.session.Session()
sts = session.client("sts")
sp = session.client('savingsplans')

#regions = session.get_available_regions('dynamodb')
regions = ["eu-north-1", "ap-south-1", "eu-west-3", "eu-west-2", "eu-west-1", "ap-northeast-3", "ap-northeast-2", "ap-northeast-1", "sa-east-1", "ca-central-1", "ap-southeast-1", "ap-southeast-2", "eu-central-1", "us-east-1", "us-east-2", "us-west-1", "us-west-2"]
account_id = sts.get_caller_identity()["Account"]
response = sp.describe_savings_plans(
    states=[
        'active',
    ]
)
    
print ([spid['savingsPlanId'] for spid in response['savingsPlans']])
    
for region in regions:
    print(region)
    ec2 = session.client('ec2', region_name=region)
    rds = session.client('rds', region_name=region)
    redshift = session.client('redshift', region_name=region)
    es = session.client('elasticache', region_name=region)
    reservedEC2Instances = ec2.describe_reserved_instances(
        Filters=[
            {
                'Name': 'state',
                'Values': [
                    'retired',
                ]
            },
        ]
    )
        
    print ([ec2ReservedID['ReservedInstancesId'] for ec2ReservedID in reservedEC2Instances['ReservedInstances']])
        
    reservedRdsInstances = rds.describe_reserved_db_instances()
    print ("RDS reserved instances are:"[rdsReservedID['ReservedDBInstanceId'] for rdsReservedID in reservedRdsInstances['ReservedDBInstances']])

    redshiftReservedNodes = redshift.describe_reserved_nodes()
    print ("Redshift reserved nodes are:"[redshiftReservedID['ReservedNodeId'] for redshiftReservedID in redshiftReservedNodes['ReservedNodes']])

    esReserved = es.describe_reserved_cache_nodes()
    print ("Reserved Elastic Search nodes are:"[esReservedID['ReservedCacheNodeId'] for esReservedID in esReserved['ReservedCacheNodes']])
