import boto3



def test_aws():

    session = boto3.Session()
    iamsession=session.client('iam')

    response=iamsession.get_user(UserName='Shoaib')
    print(response)
    
    
if __name__ == "__main__":
  test_aws()
  
