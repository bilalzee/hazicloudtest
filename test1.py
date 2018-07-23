import boto3
import json
import datetime
import psycopg2
conn = psycopg2.connect("host=<endpoint url variable> dbname=<variable> user=<variable> password=<variable>")






ROLE_ARN = 'arn:aws:iam::<account ID>:role/Ec2ReadOnly'
#session_name='secback'
#ROLE_ARN=str(sys.argv[1])
#session_name=str(sys.argv[2])
mysession='abc'

def aws_session(role_arn=None, session_name='my_session'):
    """
    If role_arn is given assumes a role and returns boto3 session
    otherwise return a regular session with the current IAM user/role
    """
    if role_arn:
        aws_token = boto3.client('sts')
        #clientid=client.get_caller_identity()
        #print(clientid)
        response = aws_token.assume_role(RoleArn=role_arn, RoleSessionName=session_name)
        #print(response['Credentials']['Expiration'])
        #print(response['AssumedRoleUser']['Arn'])
        #print(response['AssumedRoleUser']['AssumedRoleId'])
        session = boto3.Session(
            aws_access_key_id=response['Credentials']['AccessKeyId'],
            aws_secret_access_key=response['Credentials']['SecretAccessKey'],
            aws_session_token=response['Credentials']['SessionToken'])
        return session
    else:
        return boto3.Session()


def describe_ec2():
    new_customer_session = aws_session(role_arn=ROLE_ARN, session_name=mysession)
    customer_ec2_client=new_customer_session.client('ec2',region_name='eu-west-1')
    customer_ec2_describe=customer_ec2_client.describe_instances()
    print(type(customer_ec2_describe))
    #cur = conn.cursor()
    #cur.execute("INSERT INTO ec2 (info) VALUES ", (customer_ec2_describe))
    #conn.commit()
    return customer_ec2_describe

def fixtime(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    raise TypeError("Unknown type")

test1=describe_ec2()
test=json.dumps(test1,default=fixtime)
cur = conn.cursor()
#cur.execute("INSERT INTO ec2 (info) VALUES",(test))
sql="""INSERT into ec2 (info) VALUES (\'{}\');""".format(test)
print(sql)
cur.execute(sql)
conn.commit()
    















 