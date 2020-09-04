#import argparse
import boto3
from botocore.config import Config
import string
from random import *

class Usercreate:
    ####
    def password_generate(self):
        
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


    def session_iam(self):
        session = boto3.Session(profile_name='mohd')
        #session = boto3.Session()
        iamsession=session.client('iam')
        return iamsession

    def Userexist(self,username ):
        try:
            session=self.session_iam()
            session.get_user(UserName=username)
            return False
        except Exception as e:
            print("Creating New User")
            return True

    def create_user(self,username):
        userexist=self.Userexist(username)
        created=0

        if userexist:

            try:
                session=self.session_iam()
                session.create_user(UserName=username)
                created=1
            except Exception as e:
                print("Issue at user creation",e)
        else:
            print("User already exist. Additing to the groups/Policies")
        
        if created==1:
            self.create_profile(username)
        else:
            print("User not created.")



    def create_profile(self,username):
        passw=self.password_generate()

        try:
            session=self.session_iam()
            session.create_login_profile(UserName=username,Password=passw,PasswordResetRequired=True)
            print("Password For ",username,"is ",passw)
        except Exception as e:
            print("Issue at creating user profile",e)


    def group_exit(self, group):

        try:
            session=self.session_iam()
            session.get_group(GroupName=group)
            #print("group_exit in Try")
            return True
        except:
            #print("group_exit In Except")
            return False
            


    def group_addition(self,username,groups):
        user=username
        session=self.session_iam()
        notpresent=[]

        for group in groups:

            if self.group_exit(group):

                session.add_user_to_group(GroupName=group,UserName=user)
                #print(group)
            else:
                notpresent.append(group)
                #print(group)
        
        print('Not Added in Group', notpresent,'Please check if it exist')

    def policy_exit(self,policy):
            try:
                session=self.session_iam()
                session.get_policy(PolicyArn=policy)
                return True
            except:
                return False

    def policy_attach(self,username, policies):
        user=username
        session=self.session_iam()
        notpresent=[]

        for policy in policies:
            if self.policy_exit(policy):
                session.attach_user_policy(
                    PolicyArn=policy,
                    UserName=user)
            else:
                notpresent.append(policy)
        
        print ("Policies Not Attached",notpresent,"Please check if they exist")

