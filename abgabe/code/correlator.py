"""
Author: Mattes Barkowski
Assignment: 6
Module: Interoperability
"""

# basic packages
from cmath import log
from email.mime import application
from http.client import responses
import json
from pickle import NONE
import random
import time
import calendar

import requests
import io
import sys
import re
import sqlite3

# flask related packages
from flask import Flask, render_template
from flask import request
from flask_mail import Mail, Message
from flask import Response
# from flask_cors import CORS, cross_origin

# import xml related packages
import xml.etree.ElementTree as ET
from lxml import etree

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('database.db')
    return conn


@app.route('/api/v1/inventory')
def get_inventory():
    file = open("json_files/inventory.json")

    data = json.load(file)

    return app.response_class(json.dumps(data, indent=2), mimetype='application/json')


@app.route('/api/v1/inventory/<part>')
def get_inventory_part(part):
    file = open("json_files/inventory.json")

    data = json.load(file)[f"{part}"]

    return app.response_class(json.dumps(data, indent=2), mimetype='application/json')


@app.route('/api/v1/inventory/<part>/<partname>', methods=["GET", "PUT"])
def get_inventory_partname(part, partname):
    if request.method == "GET":
        filename = "json_files/inventory.json"

        with open(filename, "r") as file:
            data = json.load(file)[f"{part}"][f"{partname}"]
            resp = {"amount": data}
            file.close()

        return app.response_class(json.dumps(resp, indent=2), mimetype='application/json')

    if request.method == "PUT":

        new_amount = request.form['amount']

        filename = "json_files/inventory.json"

        with open(filename, "r") as file:
            data = json.load(file)
            data_entry = data[f"{part}"]
            file.close()

        data_entry.pop(f"{partname}")
        data_entry[f'{partname}'] = int(new_amount)

        with open(filename, "w") as file:
            json.dump(data, file)
            file.close()

        with open(filename, "r") as file:
            resp = json.load(file)
            file.close()

        return app.response_class(resp, mimetype='application/json')

    else:

        return app.response_class(status=400)


@app.route('/api/v1/inventory', methods=["POST"])
def post_inventory():
    request_body = request.json
    filename = "json_files/inventory.json"

    with open(filename, "r") as file:
        data = json.load(file)

    data[f"{request_body['part']}"] = {}

    with open(filename, "w") as file:
        json.dump(data, file)

    resp = open(filename, "r")

    return app.response_class(resp, mimetype='application/json')


@app.route('/api/v1/inventory/<part>', methods=["POST"])
def post_inventory_part(part):
    request_body = request.json
    filename = "json_files/inventory.json"

    with open(filename, "r") as file:
        data = json.load(file)
        data_entry = data[f"{part}"]

    data_entry[f"{request_body['partname']}"] = request_body['quantity']

    data[f"{part}"] = data_entry

    with open(filename, "w") as file:
        json.dump(data, file)

    resp = open(filename, "r")

    return app.response_class(resp, mimetype='application/json')


# http://131.130.122.25:9092/api/v1/inventory?part=mainboard
@app.route('/api/v1/inventory', methods=["PATCH"])
def patch_inventory_part():
    request_body = request.json
    part_arg = request.args.get("part")

    print("part_arg: ", part_arg)
    filename = "json_files/inventory.json"

    with open(filename, "r") as file:
        data = json.load(file)
        data_entry = data[f"{part_arg}"]

    data.pop(f"{part_arg}")

    data[f"{request_body['new_part']}"] = data_entry

    with open(filename, "w") as file:
        json.dump(data, file)

    resp = open(filename, "r")

    return app.response_class(resp, mimetype='application/json')


# http://131.130.122.25:9092/api/v1/inventory/mainboard?partname=Gigabyte GA-A320M-S2H
@app.route('/api/v1/inventory/<part>', methods=["PATCH"])
def patch_inventory_parts(part):
    part_arg = request.args.get("partname")
    request_body = request.json
    new_partname = bool(request_body.get("new_partname"))
    quantity = bool(request_body.get("quantity"))

    print("Request Body: ", request_body)

    print("part_arg: ", part_arg)

    filename = "json_files/inventory.json"

    with open(filename, "r") as file:
        data = json.load(file)
        data_entry = data[f"{part}"]

    if new_partname is True and quantity is False:
        quantity = data_entry[f"{part_arg}"]
        data_entry.pop(f"{part_arg}")
        data_entry[f'{request_body["new_partname"]}'] = quantity

        with open(filename, "w") as file:
            json.dump(data, file)

        resp = open(filename, "r")

        return app.response_class(resp, mimetype='application/json')

    if quantity is True and new_partname is False:
        data_entry[f'{part_arg}'] = request_body["quantity"]

        with open(filename, "w") as file:
            json.dump(data, file)

        resp = open(filename, "r")

        return app.response_class(resp, mimetype='application/json')

    if quantity is True and new_partname is True:
        data_entry.pop(f"{part_arg}")
        data_entry[f'{request_body["new_partname"]}'] = request_body["quantity"]

        with open(filename, "w") as file:
            json.dump(data, file)

        resp = open(filename, "r")

        return app.response_class(resp, mimetype='application/json')


@app.route('/api/v1/createorder')
def create_order():
    cpu_arr = ["AMD-Ryzen-5-5600X", "Intel-Core-i7-12700K", "AMD-Ryzen-7-5800X", "AMD-Ryzen-9-5900X"]

    cpu_cool_arr = ["Cooler-Master-Hyper-212-RGB-Black-Edition", "Noctua-NH-D15", "Noctua-NH-L9",
                    "NZXT-Kraken-Z-3", "Corsair-iCUE-H115i-Elite-Capellix"]

    mainb_arr = ["Gigabyte-GA-A320M-S2H", "Asus-Prime-A320M-K", "Asrock-B450M-Steel-Legend", "MSI-Z390-A-Pro"]

    ram_arr = ["G.Skill-RipJaws-V-DDR4-3600MHz", "DDR4-Corsair-3600MHz-Vengeance-RGB-PRO-SL",
               "DDR4-Kingston-3600MHz-Fury-Beast-RGB", "DDR4-Corsair-3600MHz-Vengeance"]

    response = {
        f"{random.choice(cpu_arr)}": random.randint(1, 10),
        f"{random.choice(cpu_cool_arr)}": random.randint(1, 10),
        f"{random.choice(mainb_arr)}": random.randint(1, 10),
        f"{random.choice(ram_arr)}": random.randint(1, 10)
    }

    return app.response_class(json.dumps(response, indent=2), mimetype='application/json')


@app.route('/api/v1/progress')
def get_process():
    file = open("json_files/progress.json")

    data = json.load(file)

    return app.response_class(json.dumps(data, indent=3), mimetype='application/json')


@app.route('/api/v1/progress/<step>')
def get_process_type(step):
    step_bool = bool(step)

    if step_bool is True:

        file = open("json_files/progress.json")

        data = json.load(file)

        data = data[int(step)]

        return app.response_class(json.dumps(data, indent=2), mimetype='application/json')

    else:

        file = open("json_files/progress.json")

        data = json.load(file)

        return app.response_class(json.dumps(data, indent=3), mimetype='application/json')


'''
Here follows the logic of the Correlator Engine

Input:

Output:
'''


@app.route('/api/v1/correlator', methods=["POST", "GET"])
def correlator():
    process_ = bool(False)
    header = request.headers

    if header.get('Content-Id') == "UsbC4Eva":
        print("Erfolgreich in CPEE Instance Erstellung reingegangen")
        request_body = request.json
        request_form = request.form

        first_key = list(request_body.keys())[0]
        second_key = list(request_body.keys())[1]
        third_key = list(request_body.keys())[2]
        fourth_key = list(request_body.keys())[3]

        xmlstr = f'''<testset xmlns="http://cpee.org/ns/properties/2.0">
              <executionhandler>ruby</executionhandler>
              <dataelements/>
              <endpoints>
                <teil1>http://131.130.122.25:9092/api/v1/inventory/cpus/{first_key}</teil1>
                <timeout>http://gruppe.wst.univie.ac.at/~mangler/services/timeout.php</timeout>
                <teil2>http://131.130.122.25:9092/api/v1/inventory/cpu_coolers/{second_key}</teil2>
                <teil3>http://131.130.122.25:9092/api/v1/inventory/mainboards/{third_key}</teil3>
                <teil4>http://131.130.122.25:9092/api/v1/inventory/ram/{fourth_key}</teil4>
                <progress>http://131.130.122.25:9092/api/v1/progress</progress>
                <correlation>http://131.130.122.25:9092/api/v1/correlator</correlation>
                <produzieren>http://cpee.org:9350</produzieren>
              </endpoints>
              <attributes>
                <info>IOP Production - a12024366</info>
                <modeltype>CPEE</modeltype>
                <theme>preset</theme>
              </attributes>
              <description>
                <description xmlns="http://cpee.org/ns/description/1.0">
                  <manipulate id="man">
                    data.pid = Digest::MD5.hexdigest(Kernel::rand().to_s)
                  </manipulate>
                  <parallel wait="-1" cancel="last">
                    <parallel_branch pass="" local="">
                      <call id="a11" endpoint="teil1">
                        <parameters>
                          <label>amount part1</label>
                          <method>:get</method>
                          <arguments/>
                          <_context_data_analysis>
                            <probes/>
                            <ips/>
                          </_context_data_analysis>
                          <report>
                            <url/>
                          </report>
                        </parameters>
                        <code>
                          <prepare/>
                          <finalize output="result">data.teil1 = result["amount"] - 1</finalize>
                          <update output="result"/>
                          <rescue output="result"/>
                        </code>
                        <annotations>
                          <_timing>
                            <_timing_weight/>
                            <_timing_avg/>
                            <explanations/>
                          </_timing>
                          <_notes>
                            <_notes_general/>
                          </_notes>
                        </annotations>
                        <input/>
                        <output/>
                        <implementation>
                          <description/>
                        </implementation>
                        <code>
                          <description/>
                        </code>
                      </call>
                      <call id="a21" endpoint="teil1">
                        <parameters>
                          <label>set amount part1</label>
                          <method>:put</method>
                          <arguments>
                            <amount>!data.teil1</amount>
                          </arguments>
                          <_context_data_analysis>
                            <probes/>
                            <ips/>
                          </_context_data_analysis>
                          <report>
                            <url/>
                          </report>
                        </parameters>
                        <code>
                          <prepare/>
                          <finalize output="result"/>
                          <update output="result"/>
                          <rescue output="result"/>
                        </code>
                        <annotations>
                          <_timing>
                            <_timing_weight/>
                            <_timing_avg/>
                            <explanations/>
                          </_timing>
                          <_notes>
                            <_notes_general/>
                          </_notes>
                        </annotations>
                        <input/>
                        <output/>
                        <implementation>
                          <description/>
                        </implementation>
                        <code>
                          <description/>
                        </code>
                      </call>
                    </parallel_branch>
                    <parallel_branch pass="" local="">
                      <call id="a12" endpoint="teil2">
                        <parameters>
                          <label>amount part2</label>
                          <method>:get</method>
                          <arguments/>
                          <_context_data_analysis>
                            <probes/>
                            <ips/>
                          </_context_data_analysis>
                          <report>
                            <url/>
                          </report>
                        </parameters>
                        <code>
                          <prepare/>
                          <finalize output="result">data.teil2 = result["amount"] - 1</finalize>
                          <update output="result"/>
                          <rescue output="result"/>
                        </code>
                        <annotations>
                          <_timing>
                            <_timing_weight/>
                            <_timing_avg/>
                            <explanations/>
                          </_timing>
                          <_notes>
                            <_notes_general/>
                          </_notes>
                        </annotations>
                        <input/>
                        <output/>
                        <implementation>
                          <description/>
                        </implementation>
                        <code>
                          <description/>
                        </code>
                      </call>
                      <call id="a22" endpoint="teil2">
                        <parameters>
                          <label>set amount part2</label>
                          <method>:put</method>
                          <arguments>
                            <amount>!data.teil2</amount>
                          </arguments>
                          <_context_data_analysis>
                            <probes/>
                            <ips/>
                          </_context_data_analysis>
                          <report>
                            <url/>
                          </report>
                        </parameters>
                        <code>
                          <prepare/>
                          <finalize output="result"/>
                          <update output="result"/>
                          <rescue output="result"/>
                        </code>
                        <annotations>
                          <_timing>
                            <_timing_weight/>
                            <_timing_avg/>
                            <explanations/>
                          </_timing>
                          <_notes>
                            <_notes_general/>
                          </_notes>
                        </annotations>
                        <input/>
                        <output/>
                        <implementation>
                          <description/>
                        </implementation>
                        <code>
                          <description/>
                        </code>
                      </call>
                    </parallel_branch>
                    <parallel_branch pass="" local="">
                      <call id="a13" endpoint="teil3">
                        <parameters>
                          <label>amount part3</label>
                          <method>:get</method>
                          <arguments/>
                          <_context_data_analysis>
                            <probes/>
                            <ips/>
                          </_context_data_analysis>
                          <report>
                            <url/>
                          </report>
                        </parameters>
                        <code>
                          <prepare/>
                          <finalize output="result">data.teil3 = result["amount"] - 1</finalize>
                          <update output="result"/>
                          <rescue output="result"/>
                        </code>
                        <annotations>
                          <_timing>
                            <_timing_weight/>
                            <_timing_avg/>
                            <explanations/>
                          </_timing>
                          <_notes>
                            <_notes_general/>
                          </_notes>
                        </annotations>
                        <input/>
                        <output/>
                        <implementation>
                          <description/>
                        </implementation>
                        <code>
                          <description/>
                        </code>
                      </call>
                      <call id="a23" endpoint="teil3">
                        <parameters>
                          <label>set amount part3</label>
                          <method>:put</method>
                          <arguments>
                            <amount>!data.teil3</amount>
                          </arguments>
                          <_context_data_analysis>
                            <probes/>
                            <ips/>
                          </_context_data_analysis>
                          <report>
                            <url/>
                          </report>
                        </parameters>
                        <code>
                          <prepare/>
                          <finalize output="result"/>
                          <update output="result"/>
                          <rescue output="result"/>
                        </code>
                        <annotations>
                          <_timing>
                            <_timing_weight/>
                            <_timing_avg/>
                            <explanations/>
                          </_timing>
                          <_notes>
                            <_notes_general/>
                          </_notes>
                        </annotations>
                        <input/>
                        <output/>
                        <implementation>
                          <description/>
                        </implementation>
                        <code>
                          <description/>
                        </code>
                      </call>
                    </parallel_branch>
                    <parallel_branch pass="" local="">
                      <call id="a14" endpoint="teil4">
                        <parameters>
                          <label>amount part4</label>
                          <method>:get</method>
                          <arguments/>
                          <_context_data_analysis>
                            <probes/>
                            <ips/>
                          </_context_data_analysis>
                          <report>
                            <url/>
                          </report>
                        </parameters>
                        <code>
                          <prepare/>
                          <finalize output="result">data.teil4 = result["amount"] - 1</finalize>
                          <update output="result"/>
                          <rescue output="result"/>
                        </code>
                        <annotations>
                          <_timing>
                            <_timing_weight/>
                            <_timing_avg/>
                            <explanations/>
                          </_timing>
                          <_notes>
                            <_notes_general/>
                          </_notes>
                        </annotations>
                        <input/>
                        <output/>
                        <implementation>
                          <description/>
                        </implementation>
                        <code>
                          <description/>
                        </code>
                      </call>
                      <call id="a24" endpoint="teil4">
                        <parameters>
                          <label>set amount part4</label>
                          <method>:put</method>
                          <arguments>
                            <amount>!data.teil4 </amount>
                          </arguments>
                          <_context_data_analysis>
                            <probes/>
                            <ips/>
                          </_context_data_analysis>
                          <report>
                            <url/>
                          </report>
                        </parameters>
                        <code>
                          <prepare/>
                          <finalize output="result"/>
                          <update output="result"/>
                          <rescue output="result"/>
                        </code>
                        <annotations>
                          <_timing>
                            <_timing_weight/>
                            <_timing_avg/>
                            <explanations/>
                          </_timing>
                          <_notes>
                            <_notes_general/>
                          </_notes>
                        </annotations>
                        <input/>
                        <output/>
                        <implementation>
                          <description/>
                        </implementation>
                        <code>
                          <description/>
                        </code>
                      </call>
                    </parallel_branch>
                  </parallel>
                  <call id="a3" endpoint="produzieren">
                    <parameters>
                      <label>produce part</label>
                      <method>:post</method>
                      <arguments>
                        <delegate>!endpoints.progress</delegate>
                        <async>!endpoints.correlation</async>
                        <pid>!data.pid</pid>
                      </arguments>
                      <_context_data_analysis>
                        <probes/>
                        <ips/>
                      </_context_data_analysis>
                      <report>
                        <url/>
                      </report>
                    </parameters>
                    <code>
                      <prepare/>
                      <finalize output="result"/>
                      <update output="result"/>
                      <rescue output="result"/>
                    </code>
                    <annotations>
                      <_timing>
                        <_timing_weight/>
                        <_timing_avg/>
                        <explanations/>
                      </_timing>
                      <_notes>
                        <_notes_general/>
                      </_notes>
                    </annotations>
                    <input/>
                    <output/>
                    <implementation>
                      <description/>
                    </implementation>
                    <code>
                      <description/>
                    </code>
                  </call>
                  <loop mode="pre_test" condition="data.progress != 'FINITO'">
                    <call id="a4" endpoint="correlation">
                      <parameters>
                        <label>wait for progress</label>
                        <method>:post</method>
                        <arguments>
                          <pid>!data.pid</pid>
                        </arguments>
                        <_context_data_analysis>
                          <probes/>
                          <ips/>
                        </_context_data_analysis>
                        <report>
                          <url/>
                        </report>
                      </parameters>
                      <code>
                        <prepare/>
                        <finalize output="result">p result;data.progress = result["progress"]</finalize>
                        <update output="result"/>
                        <rescue output="result"/>
                      </code>
                      <annotations>
                        <_timing>
                          <_timing_weight/>
                          <_timing_avg/>
                          <explanations/>
                        </_timing>
                        <_notes>
                          <_notes_general/>
                        </_notes>
                      </annotations>
                      <input/>
                      <output/>
                      <implementation>
                        <description/>
                      </implementation>
                      <code>
                        <description/>
                      </code>
                    </call>
                  </loop>
                </description>
              </description>
              <transformation>
                <description type="copy"/>
                <dataelements type="none"/>
                <endpoints type="none"/>
              </transformation>
            </testset>
                '''

        xml_file = open("production.xml", "w")
        xml_file.write(xmlstr)
        xml_file.close()

        header_data = str(header)
        body_data = str(request_body)

        body_data += header_data
        # set timestamp
        gmtime_ = time.gmtime()
        timestamp = calendar.timegm(gmtime_)

        with open("logs/log.txt", "a") as file:
            file.write("\n############# Request from Donatello ############\n")
            file.write(f"\n{body_data}\n")
            process_ = bool(True)
            file.close()

        if process_:
            url = "https://wwwlab.cs.univie.ac.at/~mattesb98/iop22-6/start_cpee.php"

            # send get request to cpee
            requests.get(url)

        return "Correlator works so far"

    if header.get('Content-Id') is None:
        print("Im inside the one and only endpoint")
        # collect data from cpee request
        callback_id = header["Cpee-Callback-Id"]
        gmtime_ = time.gmtime()
        timestamp = calendar.timegm(gmtime_)
        callback_url = header["Cpee-Callback"]
        cpee_activity = header["Cpee-Activity"]
        cpee_uuid = header["Cpee-Instance-Uuid"]
        cpee_instance = header["Cpee-Instance"]
        pid = request.form.get("pid")

        print(header)
        filename = "logs/log.txt"

        # set timestamp
        gmtime_ = time.gmtime()
        timestamp = calendar.timegm(gmtime_)

        # log data body
        # log_data = {
        #     "callback_id": callback_id,
        #     "callback_url": callback_url,
        #     "cpee_activity": cpee_activity,
        #     "cpee_uuid": cpee_uuid,
        #     "cpee_instance": cpee_instance,
        #     "pid": pid
        # }

        log_data = f"\nCallback-Id: {callback_id}, Callback-url: {callback_url}, Cpee-Activity: {cpee_activity}, " \
                   f"Cpee-activity: {cpee_activity}, Cpee-uuid:{cpee_uuid}, Cpee-Instance: {cpee_instance}, " \
                   f"PID: {pid} \n"

        with open(filename, "a") as o:
            o.write("\n############# Request from CPEE ############\n")
            o.write(log_data)
            o.close()

        # write collected cpee data into database
        process_finished = random.randint(0, 1)

        # create insert command to db
        connection = get_db_connection()
        cur = connection.cursor()
        cur.execute(
            "INSERT INTO cpee_requests (Cpee_Callback_id, created, Cpee_Callback_url,Cpee_Activity, Cpee_uuid, Cpee_instance, Process_finished, pid) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
            f"{callback_id}", f"{timestamp}", f"{callback_url}", f"{cpee_activity}", f"{cpee_uuid}", f"{cpee_instance}",
            int(process_finished), f"{pid}")
        )

        connection.commit()
        connection.close()

        # check if the process is finished -> request on production table
        conn = get_db_connection()
        cursor = conn.cursor()
        finito_check = []
        progress_state = cursor.execute(f"SELECT progress_state FROM production_requests WHERE pid='{pid}'").fetchall()
        conn.close()
        print("- Requested progress states: ", progress_state)
        print("- Single progress state: ", progress_state)

        # iterate over list of progress states
        for i in progress_state:
            finito_check.append(json.dumps(i))

        print("CHECK ARRAY 1 and type: ", finito_check, type(finito_check))
        com_string = '["FINITO"]'

        if com_string in finito_check:
            print("Production is finished")
            # callback holen von der aktuellsten und zugehörigen CPEE instance
            # check if the process is finished -> request on production table
            test_arr = []
            conn = get_db_connection()
            cursor = conn.cursor()
            callback = cursor.execute(
                f"SELECT Cpee_Callback_url, created FROM cpee_requests WHERE pid='{pid}' ORDER BY created DESC LIMIT 1").fetchall()
            conn.close()

            for l in callback:
                test_arr.append(json.dumps(l))

            print("test arr: ", test_arr)

            string_without_brackets = re.sub(r"[\[\]]", '', test_arr[0])
            callback_url_request = string_without_brackets.split(",")[0]
            callback_url_request = callback_url_request.replace('"', '')
            print("Callback URL String: ",callback_url_request)
            #callback_url_request = callback_url_request[:-1]
            callback_url_request = str(callback_url_request)
            # define response body
            response_body = {
                "progress" : 'FINITO'
            }

            # define header
            cpee_header = {
                'Content-Type': 'application/json',
                'CPEE-CALLBACK': 'true'
            }

            #requests.put(callback_url_request, json=json.dumps(response_body), headers=cpee_header)
            #time.sleep(2.3)
            #sys.exit()
            #return ""
            return app.response_class(json.dumps(response_body), mimetype="application/json")

        else:
            print("Production not finished")
            response_body = {
                "progress": "INTERMEDIATE"
            }

            cpee_header = {
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate',
                'Content-type': 'application/json',
            }
            time.sleep(3.3)
            return app.response_class(json.dumps(response_body), mimetype="application/json")

    if header.get('Content-Id') == "producing":

        print("Producing Anfrage ist erfolgreich eingegangen/verarbeitet worden")
        request_body = request.json
        print("- Producing Request Body: ", request_body)
        progress_state = request_body.get("progress")
        completion = request_body.get("completion")
        pid = request_body.get("pid")
        gmtime_ = time.gmtime()
        timestamp = calendar.timegm(gmtime_)

        # log_data = {
        #     "progress": progress_state,
        #     "completion": completion,
        #     "pid": pid,
        #     "content-id": header.get('Content-Id')
        # }

        log_data = f"\nProgress: {progress_state}, Completion: {completion}, PID: {pid}, " \
                   f"Content-Id: {header.get('Content-Id')}\n"

        filename = "logs/log.txt"

        with open(filename, "a") as op:
            op.write("\n############# Request from Producing ############\n")
            op.write(log_data)
            op.close()

        # create insert command to production table
        connection = get_db_connection()
        cur = connection.cursor()
        cur.execute("INSERT INTO production_requests (pid, created, completion,progress_state) VALUES (?, ?, ?, ?)",
                    (f"{pid}", f"{timestamp}", int(completion), f"{progress_state}"))

        connection.commit()
        connection.close()
        # if progress_state == "FINITO":
        #
        #     cpee_header = {
        #         'Accept': '*/*',
        #         'Accept-Encoding': 'gzip, deflate',
        #         'Content-type': 'application/json',
        #     }
        #
        #     callback_url = inform_cpee(pid)
        #     requests.put(callback_url, json={"progress": progress_state}, headers=cpee_header)
        #
        #     # check if the process is finished -> request on production table
        #     conn = get_db_connection()
        #     cursor = conn.cursor()
        #     production_data = cursor.execute(f"SELECT * FROM production_requests WHERE pid='{pid}'").fetchall()
        #     cpee_data = cursor.execute(f"SELECT * FROM cpee_requests WHERE pid='{pid}'").fetchall()
        #     conn.close()
        #
        #     print("- Production Table Data: ", json.dumps(production_data))
        #     print("- Cpee Table Data: ", json.dumps(cpee_data))

        return "works"


def inform_cpee(pid):
    conn = get_db_connection()
    cursor = conn.cursor()

    posts = cursor.execute(f"SELECT Cpee_Callback_url FROM cpee_requests WHERE pid='{pid}'").fetchall()
    conn.close()

    return posts[0][0]


@app.route("/test", methods=["GET", "POST"])
def test():
    header = request.headers
    print(header)

    gmtime_ = time.gmtime()
    timestamp = calendar.timegm(gmtime_)
    print(f"Anfrage kommt rein{timestamp}")

    response_header = {
        'CPEE-CALLBACK': 'true'
    }

    # requests.put(callback_url, json={"receive_product": received_product}, headers=cpee_header)

    return "Piss ins gesicht"
    # return app.response_class(headers=response_header)


@app.route("/show_db/<db>", methods=["GET"])
def get_db_content(db):
    conn = get_db_connection()
    cursor = conn.cursor()
    resp = []
    if db == "production_requests":
        posts = cursor.execute('SELECT * FROM production_requests').fetchall()
        conn.close()
        for i in posts:
            resp.append(json.dumps(i))

    if db == "cpee_requests":
        posts = cursor.execute('SELECT * FROM cpee_requests').fetchall()
        conn.close()
        for i in posts:
            resp.append(json.dumps(i))

    return app.response_class(json.dumps(resp, indent=2), mimetype="application/json")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9092)