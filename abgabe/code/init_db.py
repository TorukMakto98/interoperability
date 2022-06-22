import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())


cur = connection.cursor()

cur.execute("INSERT INTO cpee_requests (Cpee_Callback_id, created, Cpee_Callback_url,Cpee_Activity, Cpee_uuid, Cpee_instance, Process_finished, pid) VALUES (?, ?, ?, ?, ?, ?, ?,?)",
            ('22134af2SX324adf2312341as', '10.12.2022', 'spödolkjavhasökljhvn', 'a21', 'jlköasdfgköjlasdfkjlö3240312j', '2341', 0, "asÄDLKFHJÜASODIGFÖLSDF")
            )

cur.execute("INSERT INTO production_requests (pid, created, completion,progress_state) VALUES (?, ?, ?, ?)",
            ('22134af2SX324adf2312341as', '10.12.2022', 50, "INTERMEDIATE")
            )
connection.commit()
connection.close()