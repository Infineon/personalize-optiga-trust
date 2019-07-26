### _Important: You will need to complete the OPTIGA™ Trust personalization steps before proceeding:_

***
## In the nutshell

```console
#Creates a Thing in AWS Registry
$ aws iot create-thing --thing-name "IoT_Object_With_OPTIGA_Trust"

#Extract the ARN
$ export AWS_ARN=$(sed 's/.//;s/.$//' optiga.aws_arn)

#Confirm the value of the ARN
$ echo $AWS_ARN

#Attach the Thing with the certificate
$ aws iot attach-thing-principal --thing-name "IoT_Object_With_OPTIGA_Trust" --principal $AWS_ARN

#Create the Policy
$ aws iot create-policy --policy-name IoT_Thing_Weak_Policy --policy-document file://IoT_Thing_Weak_Policy

#Attach the Policy to the certificate
$ aws iot attach-principal-policy --policy-name "IoT_Thing_Weak_Policy" --principal $AWS_ARN
```
***

## Adding a Thing to AWS IoT Thing Registry

**1. Creates a Thing called “IoT_Object_With_OPTIGA_Trust” and register on AWS IoT Core Registry**

```console
#Creates a Thing in AWS Registry
$ aws iot create-thing --thing-name "IoT_Object_With_Trust_X"
```
<details>
<summary>Expected output:</summary>

```console
{
    "thingArn": "arn:aws:iot:us-west-2:065398228892:thing/IoT_Object_With_OPTIGA_Trust",
    "thingName": "IoT_Object_With_Trust_X",
    "thingId": "9208211e-9657-4e6c-84f5-56e1f26c9704"
}
```
</details>


***


**2. Creates a temporary variable that stores the ARN.**
Attach the Thing to the certificate.

```console
#Extract the ARN
$ export AWS_ARN=$(sed 's/.//;s/.$//' optiga.aws_arn)

#Confirm the value of the ARN
$ echo $AWS_ARN

#Attach the Thing with the certificate
$ aws iot attach-thing-principal --thing-name "IoT_Object_With_OPTIGA_Trust" --principal $AWS_ARN

```

***

**3. Create and attach the policy to a certificate.<br>**
_Note: This is a sample policy and must be further fine-tune after initial configuration._

_Note: YOu should have a file named IoT_Thing_Weak_Policy in order to proceed here. The content might look like the following:_

```console
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "iot:Connect",
            "Resource": "arn:aws:iot:<aws-region>:<aws-account-id>:*"
        },
        {
            "Effect": "Allow",
            "Action": "iot:Publish",
            "Resource": "arn:aws:iot:<aws-region>:<aws-account-id>:*"
        },
        {
            "Effect": "Allow",
            "Action": "iot:Subscribe",
            "Resource": "arn:aws:iot:<aws-region>:<aws-account-id>:*"
        },
        {
            "Effect": "Allow",
            "Action": "iot:Receive",
            "Resource": "arn:aws:iot:<aws-region>:<aws-account-id>:*"
        }
    ]
}
```

where the values <aws-region> and <aws-account> correspond to you AWS configuration. 
You can use the following commands to extract the region you use or the account-id

```console
# Get Your region
$ aws configure get region
eu-central-1
```
    
```console
# Get your Account ID
$ aws sts get-caller-identity
{
    "UserId": "Your-User-ID",
    "Account": "Your-Account-Id-use-it-for-policy",
    "Arn": "Your-arn-id"
}
```

```console
#Create the Policy
$ aws iot create-policy --policy-name IoT_Thing_Weak_Policy --policy-document file://IoT_Thing_Weak_Policy
```

```console
#Attach the Policy to the certificate
$ aws iot attach-principal-policy --policy-name "IoT_Thing_Weak_Policy" --principal $AWS_ARN

```
<details>
<summary>Expected Output</summary>

```console
{
    "policyName": "IoT_Thing_Weak_Policy",
    "policyArn": "arn:aws:iot:us-west-2:065398228892:policy/IoT_Thing_Weak_Policy",
    "policyDocument": "{\n  \"Version\": \"2012-10-17\",\n  \"Statement\": [\n    {\n      \"Effect\": \"Allow\",\n      \"  }\n  ]\n}\n",
    "policyVersionId": "1"
}
```
</details>

***

## Personalization completed
The Thing is successfully personalized. Move yout OPTIGA™ Trust to the AWS IoT edge for testing. 
