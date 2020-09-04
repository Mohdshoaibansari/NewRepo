import test
import csv



if __name__ == "__main__":

    run= test.Usercreate()
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

                name=row[0]
                try:
                    groups=row[1].split(',')
                    run.create_user(name)
                    run.group_addition(name,groups)
                except IndexError:
                    groups=[]
                try:
                    policies=row[2].split(',')
                    run.create_user(name)
                    run.policy_attach(name, policies)
                except IndexError:
                    policies=[]
