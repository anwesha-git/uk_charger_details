# uk_charger_details


The python program to collect the charge points data for electric vehicles in the UK from a programmatic API and process it to extract relevant information. Then, store this processed data as a CSV file in AWS S3 for use by a microservice.

### Pre-Requisites

1. Install necessary python libraries

   ```pip install boto3, pandas```

2. Create/Choose a S3 bucket 

   1. Log in to the AWS Management Console and navigate to the S3 service.

   2. Choose a bucket from S3 console under "Buckets".

   2. For creating a new bucket, click on the "Create bucket" button and provide a unique name for the bucket.

   3. Select a region where you want to create the bucket and click on the "Create" button.

   4. Make sure the bucket S3 bucket have the correct permissions to allow the IAM user or role to perform the required operation. We can do this by checking the bucket and object permissions in the S3 dashboard.

3. Get the Access key and Secret key from AWS.

   

   1. Go to AWS Management Console and open IAM console.

   2. In the navigation pane, from "Users", choose your IAM user name

   3. From "Security credentials" tab, expand the "Access keys" section, and then choose "Create access key".

   4. To see the new access key, choose "Download .csv file". The keys will be in the "Access key ID" and "Secret access key" columns.

   5. Verify that the IAM user or role associated with the access key and secret key has the necessary permissions to perform the required S3 operation.

### About the Code:

The program is structured into three main functions:

Python code that retrieves the charge points data from the API, processes the data and writes the result to a CSV file on AWS S3. This code consists of several functions with comments explaining their purpose. It also takes the name of the S3 bucket as an argument to which they want to write the CSV file.

The ```main()``` function is the entry point of the program. It first gets the arguments like keys for AWS access and bucket details and then define the entry point, url and csv file, where the data will be stored.

```get_url()``` will get the url response and ```retrieve_charge_points_data()``` will retrieves the charge points data from the API and returns it as a JSON object after verifying the successful API status with ```check_api_status()```

```process_json_to_csv()``` processes the charge point data by extracting the relevant counts and column columns and filtering out entries with no charge device model. 

```upload_csv_to_S3()``` connects to an S3 bucket and uploads the given CSV data to the specified bucket

### Running the program:

Please use the below command to run the program

```python chargepointdetails_to_S3.py &lt;access-key> &lt;secret-key> &lt;bucket-name>```

## Observations:

1. Some post code values were being counted separately because they had different letter cases, which could lead to incorrect counting. To prevent this, I converted all post codes to uppercase before aggregating them. 
For example, the model "Raption LP50-3" had entries for post codes "TW6 2RQ" and "tw6 2rq", which were counted as separate entries until they were converted to the same uppercase format.

2. The code assumes that the access key and secret key will be extracted for the IAM user and passed as a parameter. However, if the program is executed on an EC2 instance, it can be created with an attached IAM role and the program will automatically inherit the permissions of the attached IAM role, eliminating the need to pass the access key explicitly. The script needs to be modified accordingly to reflect this.
