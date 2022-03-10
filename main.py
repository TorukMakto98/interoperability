# import
import psycopg2
import names
import randominfo as rnd
import random

# environmental variables
DB_NAME = "postgres"
DB_HOST = "localhost"
DB_USER = "mbarkows"
DB_PASSWORD = "password"


def name_generator():

    # creating first- & lastnames
    firstname = names.get_first_name()
    lastname = names.get_last_name()

    print("firstname: ", firstname)
    print("lastname: ", lastname)


def client_transactions():
    i = 0
    Id = [j for j in range(200000, 200800)]

    while (i < 778):
        # creating first- & lastnames
        firstname = names.get_first_name()
        lastname = names.get_last_name()

        # creating random mails
        mail = f"{firstname}.{lastname}@gmail.com"

        # creating random budget
        budget = random.randrange(100, 1500, 50)

        # creating random jobs
        job_list = ["Software Engineer", "DevOps Engineer", "Teacher", "Product Manager", "Project Manager", "HR Specialist"]
        job = random.choice(job_list)

        # creating random client_Id
        client_Id = Id[i]

        # connect to database
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)

        # insert data record
        cur = conn.cursor()

        # execute insert command
        cur.execute(f"INSERT INTO client VALUES ({client_Id}, '{firstname}', '{lastname}', {budget}, '{job}', '{mail}');")
        #cur.execute("CREATE TABLE student (id INTEGER , name VARCHAR);")
        conn.commit()
        cur.close()

        # close connection
        conn.close()
        i += 1
        print(i)

        continue

    else:
        return print("fertig")



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    client_transactions()
    #name_generator()