# SimpleMusictify
 A simple music application

## Tech stacks used: Flask, HTML5/CSS3, AWS services

## Deployment instruction: 

#### 1. Configure a DynamoDB instance using your desired settings.

#### 2. Create an initial Lambda function and run the `MusicTableProcess` in the `lambda_package` to create a S3 bucket and to connect to your DynamoDB instance, make sure to modifed the URL destination, bucket name and DynamoDB login entry in the code file to make it point toward a suitable destination.

#### 3. Create additional Lambda functions for every folder in the `lambda_package`, make sure to review the code and make suitable adjustment to the database and storage destination.

#### 4. Review the code in the `Web` to make that it point toward the correct `Lambda` functions that you just created.

#### 5. Configure an EC2 instance using your desired settings and host the `Web` folder.

## Short Note: 

This application will not work locally as it has been optimized to worked on AWS using services like EC2, S3, DynamoDB and Lambda. 

Please put in mind that this application is not a cost-optimized way to run an application on cloud, it is just for demonstrating my knowledge and understanding in some basic AWS services.
