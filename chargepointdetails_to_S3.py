import requests
import json
import pandas as pd
import boto3
import csv
import argparse

#Function to retrieve the charge points data from the API endpoint
def get_url (url):
    response = requests.get(url)
    return response

#Function to check the API status
def check_api_status (response):
    if response.status_code != 200:
        raise Exception("API returned status code {}. Check the API endpoint and try again!!".format(response.status_code))
    else:
        print ("API request successful!!")    
    return True
    
#Function to retrieve the JSON data from API
def retrieve_charge_points_data(response):
    if check_api_status (response):
       data = json.loads(response.content)
    return data

#Function to process the charge point data by extracting the required columns 
def process_json_to_csv(json_data):
    # Create list of dictionaries with all the required fields
    chargers = []
    for charger in json_data["ChargeDevice"]:
        if charger.get("ChargeDeviceModel"):
            chargers.append({
                "ChargeDeviceManufacturer": charger.get("ChargeDeviceManufacturer"),
                "LocationType": charger.get("LocationType"),
                "ChargeDeviceModel": charger.get("ChargeDeviceModel"),
                "PostCode": charger.get("ChargeDeviceLocation", {}).get("Address", {}).get("PostCode").upper(),
                "MonthUpdated": charger.get("DateUpdated", "")[:7],
                "Count": 1
            })
    #Create pandas dataframe
    df = pd.DataFrame(chargers)
    # Group by columns and aggregate count
    grouped = df.groupby(["ChargeDeviceManufacturer", "LocationType", "ChargeDeviceModel", "PostCode", "MonthUpdated"]).agg({"Count": "sum"}).reset_index()
    # Convert dataframe to CSV string
    #csv_string = grouped.to_csv('charger_models_UK.csv',index=False)
    csv_string = grouped.to_csv(index=False)
    return csv_string


#Function to upload the processed data to S3    
def upload_csv_to_S3(csv_data,csv_file,access_key,secret_key,bucket_name):
    #s3 = boto3.resource('s3')
    s3 = boto3.resource('s3',  aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    bucket = s3.Bucket(bucket_name)
    try:
        object = bucket.Object(csv_file)
        object.put(Body=csv_data)
        #s3.Bucket('uk-ev-charge-model-anwesha').upload_file(csv_file, csv_file)
        return True
    except Exception as exp:
        print ("The Upload Failed!! {}".format(str(exp)))

#Function to parse Arguments
def ParseArgs():
    parser=argparse.ArgumentParser()
    parser.add_argument("accesskey", help="access key to AWS")
    parser.add_argument("secretkey", help="secret key for AWS")
    parser.add_argument("bucket", help="bucket name to store the file")
    return parser.parse_args()

#Main function that orchestrates the other functions
def main():
    # Get the credential anf bucket details from user
    args=ParseArgs()
    access_key=args.accesskey
    secret_key=args.secretkey
    bucket_name=args.bucket
    #the url to extract the json
    url = 'https://chargepoints.dft.gov.uk/api/retrieve/registry/format/json'
    csv_file = 'charger_models_UK.csv'    
    print ("Retrieving the charge points data from the URL: {}".format(url))
    #Get response from API endpoint
    response = get_url (url)

    # Retrieve charge points data from API response
    charge_points_data = retrieve_charge_points_data(response)
    
    # Process the data and convert to CSV string
    if charge_points_data:
        print ("Processing the data for CSV")
        processed_csv_data = process_json_to_csv(charge_points_data)
    
    # Write the processed data to a S3 CSV file
    print ("Uploading the data to S3 Bucket {}".format(bucket_name))
    resp = upload_csv_to_S3(processed_csv_data,csv_file,access_key,secret_key,bucket_name)
    if resp:
        print ("Upload Completed Successfully!!")
    exit ()
   
if __name__ == "__main__":
    main()