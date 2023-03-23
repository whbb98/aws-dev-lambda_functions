import boto3
import subprocess

client = boto3.client('lambda', region_name='us-east-1')
ROLE = '<FMI_1>'
BUCKET = subprocess.getoutput('aws s3api list-buckets --query "Buckets[].Name" | grep s3bucket | tr -d "," | xargs')

response = client.create_function(
    FunctionName='create_report',
    Runtime='python3.8',
    Role=ROLE,
    Handler='create_report_code.lambda_handler',
    Code={
        'S3Bucket': BUCKET,
        'S3Key': 'create_report_code.zip'
    }

)

print ("DONE")

"""
Copyright @2021 [Amazon Web Services] [AWS]
    
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
