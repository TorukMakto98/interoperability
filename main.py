# import
import psycopg2
import names
import random
import pandas
import json
from datetime import datetime, timezone
from xml.dom import minidom

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
    client_id_list = [j for j in range(200000, 200776)]
    client_id = random.choice(client_id_list)
    # connect to database
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)

    # insert data record
    cur = conn.cursor()

    # execute insert command
    cur.execute(f"SELECT * FROM orders WHERE fk_client_Id = {client_id}")
    records = cur.fetchall()

    if records:
        print("ist was drin")
        print("Straße: ", records[0][5])
        print("Stadt: ", records[0][6])
        print("Postleitahl: ", records[0][3])
        print(records)
    else:
        print("nichts drin")
        print(records)

    # cur.execute("CREATE TABLE student (id INTEGER , name VARCHAR);")
    conn.commit()
    cur.close()

    # close connection
    conn.close()


def client_transactions():

    # connect to database
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)

    # insert data record
    cur = conn.cursor()

    # execute insert command
    cur.execute(f"CREATE TABLE client( client_Id INTEGER PRIMARY KEY,firstname VARCHAR(70),lastname VARCHAR(70),"
                f"budget FLOAT, mail_address VARCHAR(80), job_category VARCHAR(80))")
    # cur.execute("CREATE TABLE student (id INTEGER , name VARCHAR);")
    conn.commit()
    cur.close()

    # close connection
    conn.close()

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
        job_list = ["Software Engineer", "DevOps Engineer", "Teacher", "Product Manager", "Project Manager",
                    "HR Specialist"]
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
    # connect to database
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)

    # insert data record
    cur = conn.cursor()

    # execute insert command
    cur.execute(f"CREATE TABLE plastic_colors(plastic_colors_Id INTEGER PRIMARY KEY,fk_client_Id INTEGER,name VARCHAR(70),uv_resistant BOOLEAN,html_code VARCHAR,polymer_based BOOLEAN,costs_per_liter FLOAT,FOREIGN KEY (fk_client_Id) REFERENCES client(client_Id));")
    # cur.execute("CREATE TABLE student (id INTEGER , name VARCHAR);")
    conn.commit()
    cur.close()

    # close connection
    conn.close()

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


def artist_transactions():

    # connect to database
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)

    # insert data record
    cur = conn.cursor()

    # execute insert command
    cur.execute(f"CREATE TABLE artist( artist_Id INTEGER PRIMARY KEY, firstname VARCHAR, lastname VARCHAR, "
                f"age INTEGER, mail VARCHAR, hourly_fee FLOAT)")
    # cur.execute("CREATE TABLE student (id INTEGER , name VARCHAR);")
    conn.commit()
    cur.close()

    # close connection
    conn.close()

    i = 0
    artist_id_list = [j for j in range(100000, 100800)]

    while (i < 777):

        # define first- and lastnames
        firstname = names.get_first_name()
        lastname = names.get_last_name()

        #define artist Id
        artist_id = artist_id_list[i]

        # define age
        age = random.randrange(22, 50, 20)

        # connect to database
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)

        # create mail address
        mail = f"{firstname}.{lastname}@business-{lastname}.com"

        # create hourly fee
        hourly_fee_list = [12.99, 14.99, 25.99, 43.99, 120.99, 78.99, 34.99, 67.99, 54.99, 55.99, 66.99, 78.99, 121.99]
        hourly_fee = random.choice(hourly_fee_list)

        # insert data record
        cur = conn.cursor()

        # execute insert command
        cur.execute(f"INSERT INTO artist VALUES "
                    f"({artist_id}, '{firstname}', '{lastname}', {age}, '{mail}', {hourly_fee});")
        # cur.execute("CREATE TABLE student (id INTEGER , name VARCHAR);")
        conn.commit()
        cur.close()

        # close connection
        conn.close()

        # increase counter with one
        i += 1
        print(i)

        continue

    else:
        print("3d artist entity is loaded with dataset")


def sketches_transactions():

    # connect to database
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)

    # insert data record
    cur = conn.cursor()

    # execute insert command
    cur.execute(f"CREATE TABLE sketches (sketches_Id INTEGER PRIMARY KEY,fk_client_Id INTEGER,fk_artist_Id INTEGER,"
                f"figure_theme VARCHAR, created_date DATE, estimated_costs INTEGER,deadline_for_creation DATE,"
                f"gcode_file xml,FOREIGN KEY (fk_client_Id) REFERENCES client(client_id),"
                f"FOREIGN KEY (fk_artist_Id) REFERENCES artist(artist_Id))")
    # cur.execute("CREATE TABLE student (id INTEGER , name VARCHAR);")
    conn.commit()
    cur.close()

    # close connection
    conn.close()
    i = 0
    sketches_id_list = [j for j in range(300000, 300800)]
    artist_id_list = [j for j in range(100000, 100776)]
    client_id_list = [j for j in range(200000, 200776)]
    #date_time = datetime.now(timezone.utc)
    figure_theme_list = ["action figure", "car", "sword", "weapon", "plane", "building", "tool"]
    xml_file_id_list = [j for j in range(900000, 900800)]

    while (i < 777):
        # define sketches id
        sketches_id = sketches_id_list[i]
        # define created date & deadline

        # define artist id
        artist_id = random.choice(artist_id_list)

        # define client id
        client_id = random.choice(client_id_list)

        # define figure theme
        figure_theme = random.choice(figure_theme_list)

        # define estimated costs
        estimated_costs = random.randrange(100, 10000, 25)

        time_list = pandas.date_range(start="2018-09-09", end="2022-02-02")
        time = random.choice(time_list)

        # define xml file id
        xml_file_id = xml_file_id_list[i]
        # create gcode xml
        root = minidom.Document()

        xml = root.createElement('files')
        root.appendChild(xml)

        doc = root.createElement('file')
        doc.setAttribute('id', f"{xml_file_id}")
        xml.appendChild(doc)

        formatChild = root.createElement('format')
        formatChild.setAttribute('type',
                                 f"{random.choice(['gcode', 'AMF', 'OBJ', '3MF'])}")
        doc.appendChild(formatChild)

        sizeChild = root.createElement('size')
        sizeText = root.createTextNode(f"{random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])}")
        sizeChild.setAttribute('memory_unit',
                               f"{random.choice(['Kilobyte', 'Megabyte', 'Gigabyte', 'Terabyte', 'Petabyte'])}")
        sizeChild.appendChild(sizeText)
        doc.appendChild(sizeChild)

        xml_str = root.toprettyxml(indent="\t")

        # connect to database
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)

        # insert data record
        cur = conn.cursor()

        # execute insert command
        cur.execute('INSERT INTO sketches VALUES (%s , %s, %s, %s , %s, %s, %s, %s )',
                    (sketches_id, client_id, artist_id, figure_theme, time, estimated_costs, "2022-04-23", xml_str))

        # cur.execute("CREATE TABLE student (id INTEGER , name VARCHAR);")
        conn.commit()
        cur.close()

        # close connection
        conn.close()

        # increase counter with one
        i += 1
        print(i)

        continue

    else:
        print("sketches entity is loaded with data set")


def order_transactions():
    # connect to database
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)

    # insert data record
    cur = conn.cursor()

    # execute insert command
    cur.execute(f"CREATE TABLE orders (order_Id INTEGER PRIMARY KEY,fk_client_Id INTEGER,order_value INTEGER,"
                f"postcode INTEGER,payment_information json,street VARCHAR,city VARCHAR,"
                f"FOREIGN KEY (fk_client_Id) REFERENCES client(client_id))")
    # cur.execute("CREATE TABLE student (id INTEGER , name VARCHAR);")
    conn.commit()
    cur.close()

    # close connection
    conn.close()

    i = 0
    order_id_list = [j for j in range(400000, 400800)]
    client_id_list = [j for j in range(200000, 200776)]

    while (i < 777):
        # define sketches id
        order_id = order_id_list[i]

        # define order value
        order_value = random.randrange(10, 1000, 13)

        # define client id
        client_id = random.choice(client_id_list)
        # query for checking if client id already exists in db
        # connect to database
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)

        # insert data record
        cur = conn.cursor()

        # execute insert command
        cur.execute(f"SELECT * FROM orders WHERE fk_client_Id = {client_id}")
        records = cur.fetchall()

        # cur.execute("CREATE TABLE student (id INTEGER , name VARCHAR);")
        conn.commit()
        cur.close()

        # close connection
        conn.close()

        # if yes get the address data and put it into the insert command and the json element
        if records:
            postcode = records[0][3]
            city = records[0][6]
            street = records[0][5]

        else:
            # define postcode
            postcode = random.choice([1010, 1020, 1030, 1040, 1050, 1060, 1070, 1080, 1090, 1100, 1110, 1120, 1130, 1140,
                                      1150, 1160, 1170, 1180, 1190, 1200, 1210, 1220])

            # define street names
            street_prefix = ["Döblinger", "Hauptmann", "Dynamo", "Hoffenheim", "Österreich", "Kärntner", "Millstätter",
                             "Deli", "Hardt", "Pukorny", "Dresdner", "Berliner", "Hamburger", "Schalker", "Energie"]
            street_mid = ["straße", "weg", "gasse", "platz", "wall", "grund"]
            street_nr = random.randrange(1, 100, 1)
            street = random.choice(street_prefix)+random.choice(street_mid)+str(f" {street_nr}")

            # define city
            city = random.choice(["Wien", "Graz", "St.Pölten", "Linz", "Salzburg", "Innsbruck", "Klagenfurt", "Villach"])

        # define payment information
        payment_method = random.choice(["PayPal", "CreditCard", "Klarna", "Billing", "Cash", "Installment"])
        billing_country = random.choice(["Austria", "Germany", "Switzerland", "Denmark", "France", "Italy", "Poland"])

        payment_information = {
            "information": {
                "payment": {
                    "method": payment_method,
                    "value": order_value,
                    "billing_country": billing_country
                }
            }
        }

        payment_information = json.dumps(payment_information)

        # connect to database
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)

        # insert data record
        cur = conn.cursor()

        # execute insert command
        cur.execute('INSERT INTO orders VALUES (%s , %s, %s, %s , %s, %s, %s )',
                    (order_id, client_id, order_value, postcode, payment_information, street, city))

        # cur.execute("CREATE TABLE student (id INTEGER , name VARCHAR);")
        conn.commit()
        cur.close()

        # close connection
        conn.close()

        # increase counter with one
        i += 1
        print(i)

        continue

    else:
        print("order entity is loaded with data set")


def printer_transactions():
    # connect to database
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)

    # insert data record
    cur = conn.cursor()

    # execute insert command
    cur.execute(f"            CREATE TABLE printers (printer_Id INTEGER PRIMARY KEY,fk_client_Id INTEGER,"
                f"printer_name VARCHAR,wlan BOOLEAN,category VARCHAR,year_of_creation INTEGER,supplier json,"
                f"FOREIGN KEY (fk_client_Id) REFERENCES client(client_id))")
    # cur.execute("CREATE TABLE student (id INTEGER , name VARCHAR);")
    conn.commit()
    cur.close()

    # close connection
    conn.close()

    i = 0
    printer_id_list = [j for j in range(600000, 600800)]
    client_id_list = [j for j in range(200000, 200776)]
    printer_name_prefix = ["HXC-", "XS-", "XER-", "DYN-", "KOL-", "JUSQ-", "PRI-", "X21-", "SSDQ-", "AQW-", "SSC-","A-"]
    printer_name_mid = ["LIGHT-", "SA122-", "K90-", "PRINTE21-", "LKG0-", "L32-", "KOL12-", "91", "H2", "ÖPO2", "D2-"]
    printer_name_suffix = ["PRINTER", "CUS", "ZUG", "XEROX", "SAMSUNG", "HP", "KYOCERA", "LITE", "ELTIE", "FINA"]

    while (i < 777):
        # define order id
        printer = printer_id_list[i]

        # define client id
        client_id = random.choice(client_id_list)

        # define printer name
        printer_name = random.choice(printer_name_prefix)+\
                       random.choice(printer_name_mid)+\
                       random.choice(printer_name_suffix)

        # define WLAN status
        wlan = random.choice([True, False])

        # define printer category
        category = random.choice(["Huge Workstation", "Normal Workstation", "Small Workstation", "Normal Printer"])

        # define year of creation
        year_of_creation = random.choice(["2021", "2020", "2019", "2018", "2017", "2014", "2013", "2010", "2009", "2007"])

        # define supplier information
        supplier_name = random.choice(["Media Supply", "Printer Experts", "Amazon Local", "MediaMarket", "CyberExpert"])
        street_prefix = ["Doeblinger", "Hauptmann", "Dynamo", "Hoffenheim", "Oesterreich", "Kärntner", "Millstaetter",
                         "Deli", "Hardt", "Pukorny", "Dresdner", "Berliner", "Hamburger", "Schalker", "Energie"]
        street_mid = ["straße", "weg", "gasse", "platz", "wall", "grund"]
        street_nr = random.randrange(1, 100, 1)
        street = random.choice(street_prefix)+random.choice(street_mid)+str(f" {street_nr}")
        city = random.choice(["Wien", "Graz", "St.Poelten", "Linz", "Salzburg", "Innsbruck", "Klagenfurt", "Villach"])
        country = random.choice(["Austria", "Germany", "Switzerland", "Denmark", "France", "Italy", "Poland"])

        supplier = {
            "supplier_information": {
                "name": supplier_name,
                "address": {
                    "city": city,
                    "street": street,
                    "country": country
                }
            }
        }

        supplier = json.dumps(supplier)

        # connect to database
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)

        # insert data record
        cur = conn.cursor()

        # execute insert command
        cur.execute('INSERT INTO printers VALUES (%s , %s, %s, %s , %s, %s, %s )',
                    (printer, client_id, printer_name, wlan, category, year_of_creation, supplier))

        # cur.execute("CREATE TABLE student (id INTEGER , name VARCHAR);")
        conn.commit()
        cur.close()

        # close connection
        conn.close()

        # increase counter with one
        i += 1
        print(i)

        continue
    else:
        print("printer entity is loaded with dataset")


def print_job_transactions():
    # connect to database
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)

    # insert data record
    cur = conn.cursor()

    # execute insert command
    cur.execute(f"            CREATE TABLE print_job (print_job_Id INTEGER PRIMARY KEY,fk_printer_Id INTEGER,"
                f"waiting_list_position INTEGER,current_heat INTEGER,printing_costs INTEGER,status VARCHAR,stl_file xml,"
                f"processing_time INTEGER,FOREIGN KEY (fk_printer_Id) REFERENCES printers(printer_Id))")
    # cur.execute("CREATE TABLE student (id INTEGER , name VARCHAR);")
    conn.commit()
    cur.close()

    # close connection
    conn.close()

    i = 0
    print_job_id_list = [j for j in range(700000, 700800)]
    printer_id_list = [j for j in range(600000, 600776)]
    while (i < 777):
        # define print job id
        print_job_id = print_job_id_list[i]

        # define printer id
        printer_id = random.choice(printer_id_list)

        # define waiting list position
        waiting_list_position = random.randrange(1,100,1)

        # define current heat
        current_heat = random.randrange(40, 119, 2)

        # define total printing costs
        printing_costs = random.randrange(100, 2500, 20)

        # define status
        status = random.choice(["not started", "in progress", "failed", "finished"])

        # define processing time
        processing_time = random.randrange(15, 300, 3)

        # define stl file information
        root = minidom.Document()

        xml = root.createElement('files')
        root.appendChild(xml)

        doc = root.createElement('file')
        xml.appendChild(doc)

        formatChild = root.createElement('format')
        formatChild.setAttribute('type',"STL")
        doc.appendChild(formatChild)

        sizeChild = root.createElement('size')
        sizeChild.setAttribute('memory_unit',
                               f"{random.choice(['Kilobyte', 'Megabyte', 'Gigabyte', 'Terabyte', 'Petabyte'])}")
        doc.appendChild(sizeChild)

        processingTimeChild = root.createElement('processing_time')
        processingTimeChild.setAttribute('time', f"{processing_time}")
        doc.appendChild(processingTimeChild)

        xml_str = root.toprettyxml(indent="\t")

        # connect to database
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)

        # insert data record
        cur = conn.cursor()

        # execute insert command
        cur.execute('INSERT INTO print_job VALUES (%s , %s, %s, %s , %s, %s, %s, %s )',
                    (print_job_id, printer_id, waiting_list_position, current_heat, printing_costs, status, xml_str, processing_time))

        # cur.execute("CREATE TABLE student (id INTEGER , name VARCHAR);")
        conn.commit()
        cur.close()

        # close connection
        conn.close()

        # increase counter with one
        i += 1
        print(i)

        continue
    else:
        print("print job entity is loaded with dataset")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # testing() --> for testing functions and logics
    client_transactions()
    plastic_colors_transactions()
    artist_transactions()
    sketches_transactions()
    order_transactions()
    printer_transactions()
    print_job_transactions()