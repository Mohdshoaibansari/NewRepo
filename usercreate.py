import argparse
import boto3
from botocore.config import Config
import string
from random import *
import csv

def password_generate():
    
    lcharacters = string.ascii_lowercase
    ucharacters=string.ascii_uppercase
    punc= string.punctuation
    dig=string.digits

    uchars = "".join(choice(ucharacters) for x in range(randint(4, 5)))
    lchars = "".join(choice(lcharacters) for x in range(randint(4, 5)))
    dig = "".join(choice(dig) for x in range(randint(3, 4)))
    punc="".join(choice(punc) for x in range(randint(3, 4)))
    password=uchars+punc+lchars+dig
    
    return password


def session_iam():
    #session = boto3.Session(profile_name='mfa')
    session = boto3.Session()
    iamsession=session.client('iam')
    return iamsession

def Userexist(username, ):

    
    try:
        session=session_iam()
        session.get_user(UserName=username)
        return False
    except Exception as e:
        print("Creating New User")
        return True

def create_user(username):
    userexist=Userexist(username)
    created=0

    if userexist:

        try:
            session=session_iam()
            session.create_user(UserName=username)
            created=1
        except Exception as e:
            print("Issue at user creation",e)
    else:
        print("User already exist. Additing to the groups/Policies")
    
    if created==1:
        create_profile(username)
    else:
        print("User not created.")



def create_profile(username):
    passw=password_generate()

    try:
        session=session_iam()
        session.create_login_profile(UserName=username,Password=passw,PasswordResetRequired=True)
        print("Password For ",username,"is ",passw)
    except Exception as e:
        print("Issue at creating user profile",e)


def group_exit(group):

    try:
        session=session_iam()
        session.get_group(GroupName=group)
        #print("group_exit in Try")
        return True
    except:
        #print("group_exit In Except")
        return False
        


def group_addition(username,groups):
    user=username
    session=session_iam()
    notpresent=[]

    for group in groups:

        if group_exit(group):

            session.add_user_to_group(GroupName=group,UserName=user)
            #print(group)
        else:
            notpresent.append(group)
            #print(group)
    
    print('Not Added in Group', notpresent,'Please check if it exist')

def policy_exit(policy):
        try:
            session=session_iam()
            session.get_policy(PolicyArn=policy)
            return True
        except:
            return False

def policy_attach(username, policies):
    user=username
    session=session_iam()
    notpresent=[]

    for policy in policies:
        if policy_exit(policy):
            session.attach_user_policy(
                PolicyArn=policy,
                UserName=user)
        else:
            notpresent.append(policy)
    
    print ("Policies Not Attached",notpresent,"Please check if they exist")



if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # parser.add_argument('-r', '--username', action='store',
    #                     nargs=1, help='User to Add', required=True)
    # parser.add_argument('-e', '--Groups', action='store',
    #                     nargs="+",help='Please Enter Group Name', required=False)
    # parser.add_argument('-p', '--Policies', action='store',
    #                     nargs="+",help='Please Enter Policies ARN', required=False)

    # args = parser.parse_args()
    # name=args.username[0]  
    # groups=args.Groups[0].split(",")
    # policies=args.Policies[0].split(",")

    name=""
    groups=[]
    policies=[]
    with open('/Users/mohdshoaib/SharedServices/usercreate/Users.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='$')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                #print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
                name=row[0]
                groups=row[1].split(',')
                policies=row[2].split(',')


                val = input("Chose from Following for {}:\n Group:1 \n policy:2 \n Both:3\n".format(name))

                if val == "1":
                    #print("This is one")
                    create_user(name)
                    group_addition(name,groups)
                elif val=="2":
                    #print("This is Two")
                    create_user(name)
                    policy_attach(name, policies)
                elif val=="3":
                    #print("Three")
                    create_user(name)
                    group_addition(name,groups)
                    policy_attach(name, policies)
                else:
                    print("Select Valid Value")
                
                line_count += 1



##arn:aws:iam::aws:policy/AlexaForBusinessDeviceSetup
##arn:aws:iam::aws:policy/service-role/AmazonAPIGatewayPushToCloudWatchLogs