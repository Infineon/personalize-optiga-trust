# AWS Account and Permission

Before you use Amazon AWS IoT Core for the first time, complete the following tasks: 

**Step 1: Account Creation**
1. To create an AWS account
2. Open [https://aws.amazon.com/](https://aws.amazon.com/), and then choose Create an AWS Account.
Note: If you previously signed in to the AWS Management Console using AWS account root user credentials, choose Sign in to a different account. If you previously signed in to the console using IAM credentials, choose Sign-in using root account credentials. Then choose Create a new AWS account.
3. Follow the online instructions.

**Step 2: Configuring the permission**
1. Sign in to the AWS Management Console and open the [AWS IoT console](https://console.aws.amazon.com/iot/home). 
2. To add an IAM user to your AWS account, see (IAM User Guide)(https://docs.aws.amazon.com/iam/index.html). To grant your IAM user account access to AWS IoT and Amazon FreeRTOS, attach the following IAM policies to your IAM user account:

    AmazonFreeRTOSFullAccess
    AWSIoTFullAccess

**Step 3: To attach the AmazonFreeRTOSFullAccess policy to your IAM user**
1. Browse to the [IAM console](https://console.aws.amazon.com/iam/home), and from the navigation pane, choose Users.
2. Enter your user name in the search text box, and then choose it from the list.
3. Choose **Add permissions**.
4. Choose **Attach existing policies directly**.
5. In the search box, enter **AmazonFreeRTOSFullAccess**, choose it from the list, and then choose 
   **Next: Review.**
6. Choose **Add permissions**.

**Step 4: To attach the AWSIoTFullAccess policy to your IAM user**
1. Browse to the [IAM console](https://console.aws.amazon.com/iam/home), and from the navigation pane, choose **Users**.
2. Enter your user name in the search text box, and then choose it from the list.
3. Choose **Add permissions**.
4. Choose **Attach existing policies directly**.
5. In the search box, enter **AWSIoTFullAccess**, choose it from the list, and then choose **Next: Review**.
6. Choose **Add permissions**.

For more information about IAM and user accounts, see [IAM User Guide](https://docs.aws.amazon.com/IAM/latest/UserGuide/). For more information about policies, see [IAM Permissions and Policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction_access-management.html).

**NEXT STEP: [Step 2. Setup preparation](step-2-setup-preparation.md)**
