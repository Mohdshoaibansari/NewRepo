#!/bin/bash

#####Usage####
# $1 =  MFA Token Number
#$2 = Profile Name of Credentials File
# Script will check if sts is for mfa or other switch role.
# In case of Switch role provide Account number and role name. 

VAR="mfa"
#echo "For $1"
read -p 'Type mfa: ' mfa
read -p 'Enter your emailID:' emailid



if [[ $mfa == "mfa" ]]
then
read -p "Token Number" token
aws sts get-session-token --serial-number arn:aws:iam::826598248099:mfa/${emailid} --token-code ${token} > creds.json
else
echo "please type mfa "
fi

echo "" > credentials

echo "[$1]" >> credentials
grep AccessKeyId creds.json | sed -e 's/^[[:space:]]*//' -e "s/\"//g" -e "s/,//" -e "s/AccessKeyId/aws_access_key_id/" -e "s/:/ =/" >> credentials
grep SecretAccessKey creds.json | sed -e 's/^[[:space:]]*//' -e "s/\"//g" -e "s/,//" -e "s/SecretAccessKey/aws_secret_access_key/" -e "s/:/ =/" >> credentials
grep SessionToken creds.json | sed -e 's/^[[:space:]]*//' -e "s/\"//g" -e "s/,//" -e "s/SessionToken/aws_session_token/" -e "s/:/ =/" >> credentials

cat credentials >> ~/.aws/credentials

python3 usercreate.py
