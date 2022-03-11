# import
import psycopg2
import names
import random

# environmental variables (mac)
# DB_NAME = "postgres"
# DB_HOST = "localhost"
# DB_USER = "mbarkows"
# DB_PASSWORD = "password"

# environmental variables (windows)
DB_NAME = "postgres"
DB_HOST = "localhost"
DB_USER = "postgres"
DB_PASSWORD = "postgres"


def testing():
    plastic_colors_dict = [["PowderBlue", "#CD853F"], ["PaleVioletRed", "#DB7093"], ["PapayaWhip", "#FFEFD5"],
                            ["RebeccaPurple", "#663399"], ["SeaGreen", "#2E8B57"], ["MidnightBlue", "#191970"],
                            ["Moccasin", "#FFE4B5"], ["MediumAquaMarine", "#66CDAA"], ["LightCoral", "#F08080"],
                            ["DarkOliveGreen", "#556B2F"], ["DarkOrange", "#FF8C00"], ["Crimson", "#DC143C"]]

    random_entry = random.choice(plastic_colors_dict)

    print(random_entry[0])
    print(random_entry[1])
    plastic_color_prefix = ["Ocean", "Light", "Goose", "East", "West", "North", "South", "Austrian", " Exotic", "Coco"]
    plastic_color_suffixes = ["Tight", "Taint", "Star", "Heavy", "Thick", "Elastic", "Warm"]

    print(random.choice(plastic_color_prefix) + random_entry[0] + random.choice(plastic_color_suffixes))


def client_transactions():
    i = 0
    id = [j for j in range(200000, 200800)]

    while (i < 777):
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
        client_id = id[i]

        # connect to database
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)

        # insert data record
        cur = conn.cursor()

        # execute insert command
        cur.execute(f"INSERT INTO client VALUES ({client_id}, '{firstname}', '{lastname}', {budget}, '{job}', '{mail}');")
        #cur.execute("CREATE TABLE student (id INTEGER , name VARCHAR);")
        conn.commit()
        cur.close()

        # close connection
        conn.close()

        # add 1 to i
        i += 1
        print(i)

        continue

    else:
        return print("client entity is loaded with data set")


def plastic_colors_transactions():

    i = 0
    client_id_list = [j for j in range(200000, 200776)]
    plastic_colors_id_list = [j for j in range(500000, 500800)]
    plastic_colors_list = [["PowderBlue", "#CD853F", 16.99], ["PaleVioletRed", "#DB7093", 14.99], ["PapayaWhip", "#FFEFD5", 25.99],
                            ["RebeccaPurple", "#663399", 111.99], ["SeaGreen", "#2E8B57",45.99], ["MidnightBlue", "#191970", 21.99],
                            ["Moccasin", "#FFE4B5", 25.99], ["MediumAquaMarine", "#66CDAA", 17.99], ["LightCoral", "#F08080", 18.99],
                            ["DarkOliveGreen", "#556B2F", 32.99], ["DarkOrange", "#FF8C00", 39.99], ["Crimson", "#DC143C", 24.99]]
    plastic_color_prefix = ["Ocean", "Light", "Goose", "East", "West", "North", "South", "Austrian", "Exotic", "Coco"]
    plastic_color_suffixes = ["Tight", "Taint", "Star", "Heavy", "Thick", "Elastic", "Warm"]



    while (i < 777):

        # define plastic colors id
        plastic_colors_id = plastic_colors_id_list[i]

        # define foreign key client_id
        client_id = random.choice(client_id_list)

        # get random color from list
        plastic_color_selection = random.choice(plastic_colors_list)

        # create color name
        plastic_color = random.choice(plastic_color_prefix) + plastic_color_selection[0] + random.choice(plastic_color_suffixes)

        # define uv resistant
        uv_resistant = random.choice([True, False])

        # define polymer based
        polymer_based = random.choice([True, False])

        # connect to database
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)

        # insert data record
        cur = conn.cursor()
        # execute insert command
        cur.execute(f"INSERT INTO plastic_colors VALUES ({plastic_colors_id}, {client_id}, '{plastic_color}', {uv_resistant}, '{plastic_color_selection[1]}', '{polymer_based}', {plastic_color_selection[2]});")
        # cur.execute("CREATE TABLE student (id INTEGER , name VARCHAR);")
        conn.commit()
        cur.close()

        # close connection
        conn.close()

        # add 1 to i
        i += 1
        print(i)

        continue

    else:
        print("plastic colors entity is loaded with data set")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #client_transactions()
    plastic_colors_transactions()
    #testing()
