# Lambda to change instance type

STEP 1. IAM ==> create ==> create policies in JSON ==> name : ModifyEc2Instance #name can we cay think

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
               "ec2:ModifyInstnaceAttribute",
	             "ec2:StartInstances",
	             "ec2:Stopinstances",
	             "ec2:DescribeInstances",
               "ec2:CopySnapshot",
               "ec2:Describe*",
               "ec2:CreateTags",
               "ec2:*",
               "ec2:CreateSnapshot"
            ],
            "Resource": "*"
        }
    ]
}
``` 
STEP 2 : Create Role ==> Lambda ==>[give name of role: ModifyInstance ] ==>select policy name : ModifyEc2Instance

STEP 3 : create lambda function "Author from scratch" ==> select Nodejs ==> Use an existing role ==> ModifyInstance

paste below nodejs code in index.js
 
```
const AWS = require('aws-sdk');

exports.handler = (event, context, callback) => {
    const { instanceId, instanceRegion, instanceType } = event;
    
    const ec2 = new AWS.EC2({ region: instanceRegion });
    
    Promise.resolve()
        .then(() => ec2.stopInstances({ InstanceIds: [instanceId] }).promise())
        .then(() => ec2.waitFor('instanceStopped', { InstanceIds: [instanceId] }).promise())
        .then(() => ec2.modifyInstanceAttribute({InstanceId: instanceId, InstanceType: { Value: instanceType } }).promise())
        .then(() => ec2.startInstances({ InstanceIds: [instanceId] }).promise())
        .then(() => callback(null, `Successfully modified ${event.instanceId} to ${event.instanceType}`))
        .catch(err => callback(err));
};
```

STEP 4: Configure Test Events:--
```
{
  "instanceRegion": "ap-south-1",
  "instanceId": "i-094ddb81424408afd",
  "instanceType": "t2.nano"
}
```
CronJob : cloudwatch ==> Rules ==> Create Rules ==> Schedule : 27 11 * * ? *
Add tag with Lambda function and select the Lambda name

NOTE : If you wan to run with cronjob need to change the index.js file and replace "instanceId, instanceRegion, instanceType " with there value 

```
const AWS = require('aws-sdk');

exports.handler = (event, context, callback) => {
   
   const ec2 = new AWS.EC2({ region: "ap-south-1" });
   
   Promise.resolve()
       .then(() => ec2.stopInstances({ InstanceIds: ["i-094ddb81424408afd"] }).promise())
       .then(() => ec2.waitFor('instanceStopped', { InstanceIds: ["i-094ddb81424408afd"] }).promise())
       .then(() => ec2.modifyInstanceAttribute({InstanceId: "i-094ddb81424408afd", InstanceType: { Value: "t2.nano" } }).promise())
       .then(() => ec2.startInstances({ InstanceIds: ["i-094ddb81424408afd"] }).promise())
       .then(() => callback(null, `Successfully modified ${event.instanceId} to ${event.instanceType}`))
       .catch(err => callback(err));
};
```

