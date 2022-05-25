#!/bin/sh

RegionList=$(aws ec2 describe-regions \
    --all-regions \
    --query "Regions[].{Name:RegionName}" \
    --output text --region us-east-1)

for region in $RegionList
    do
    echo $region
    ec2RI=$(aws ec2 describe-reserved-instances --filters Name=state,Values=active --region $region --query 'ReservedInstances[*].ReservedInstancesId' --output                                                                              text)
    rdsRI=$(aws rds describe-reserved-db-instances  --query 'ReservedDBInstances[*].LeaseId' --region us-east-1 --output text)
    redShiftRN=$(aws redshift describe-reserved-nodes  --region us-east-1 --query 'ReservedNodes[*].ReservedNodeId' --output text)
    esRN=$(aws elasticache describe-reserved-cache-nodes  --region us-east-1 --query 'ReservedCacheNodes[*].ReservedCacheNodesOfferingId' --output text)
    if [[ -z "$ec2RI" ]]; then
        echo -e "No reserved instance found in $region"
    else
        echo -e "Reserved instances found in $region  are:\n $ec2RI"
    #echo $ec2RI >> list.txt
    fi

    if [[ -z "$rdsRI" ]]; then
        echo -e "No reserved DB instances found in $region"
    else
        echo -e "Reserved DB instances found in $region are:\n $rdsRI"
        #echo $rdsRI >> list.txt
    fi

    if [[ -z "$redShiftRN" ]]; then
        echo -e "No Redshift reserved nodes found in $region"
    else
        echo -e "Redshift reserved nodes found in $region are:\n $redShiftRN"
        #echo $redshiftRN >> list.txt
    fi

    if [[ -z "$esRN" ]]; then
        echo -e "No ElasticSearch reserved nodes found found in $region"
    else
        echo -e "ElasticSearch reserved nodes found in $region are:\n $esRN"
        #echo $esRN >> list.txt
    fi
    done
