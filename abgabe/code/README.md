# Assignment 6
## Mattes Barkowski - 12024366
### Interoperability - SoSe22

This Readme file describe the System and the execution of these system.
The two major parts of the system are the inventory management system and 
the correlator engine. The hole system is hosted over an flask server and is
availabe under the following address:

    http://131.130.122.25:9092/

The logic of the correlator is available under the following endpoint and 
accept POST and GET Requests:

    http://131.130.122.25:9092/api/v1/correlator

The logic of my inventory service is available under the followings endpoints
and accepts GET and PUT requests:

    http://131.130.122.25:9092/api/v1/inventory
    http://131.130.122.25:9092/api/v1/inventory/<part>
    http://131.130.122.25:9092/api/v1/inventory/<part>/<partname>

The Lager-, Bestellung-, and Status-Service are registered under the regarded Donatello
endpoint. Also the correlator is registered under Donatello. So the Donatello endpoint will trigger 
my correlator service, which creates a new cpee instance through the php script which is also
located on my server -> start_cpee.php

The current process is running under the following PID on the abgabe.cs.univie.ac.at server:

    160324

To start the process manually you first have to end the current process with the following kill command:
    
    kill -9 160324

After that you can start the python script with the follwoing command from hand:

    python3 correlator.py

If you like to start the nohup script/worker again, run the following command:

    nohup python3 correlator.py &