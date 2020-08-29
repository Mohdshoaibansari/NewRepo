import boto3
import csv

if __name__ == "__main__":

    name=""
    groups=[]
    policies=[]
    with open('Users.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='$')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                #print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
                name=row[0]
                try:
                    groups=row[1].split(',')
                    policies=row[2].split(',')
                except IndexError:
                    groups=[]
                try:
                    policies=row[2].split(',')
                except IndexError:
                    policies=[]
                
                    
                print(name,groups,policies)
                line_count += 1
