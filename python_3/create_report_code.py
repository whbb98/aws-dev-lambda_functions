
def lambda_handler(event, context):
    return_me = {}
    return_me["msg_str"] =  "Report processing, check your phone shortly"
    return return_me

#remove this line below once you have tested locally and wish to deploy
#print(lambda_handler(None, None))
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
