#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# Import Python library
from flask import Flask, jsonify
from nornir import InitNornir
from nornir.plugins.tasks import networking


app = Flask(__name__)

def to_json(results):
    return jsonify({host: result[0].result for host, result in results.items()})

@app.route('/')
def index():

    # Device parameters
    h = {'my_device': {'hostname': "192.168.0.100", 'username': "cisco", 'password': "cisco", 'port': 22, 'platform': 'ios'}}

    # Initialization of the Nornir object
    nr = InitNornir(inventory={"plugin": "nornir.plugins.inventory.simple.SimpleInventory", "options": {"hosts": h}})

    # Command to send to the device
    my_cli_command = "show version"

    # Get result of the command
    result = nr.run(task=networking.napalm_cli, commands=[my_cli_command])

    # Extract result command from the dictionary
    a = result[list(result.keys())[0]][0].result.get(my_cli_command)

    # replace "\n" with "<BR>" for HTML return to the line
    b = a.replace("\n","<BR>")

    # HTML page
    my_return = "<!DOCTYPE html><html><head></head><body><h1>Command:</h1><BR>" + my_cli_command + "<BR><BR><P>" + b + "<BR><BR></P></body></html>"

    return my_return


# Main function call
if __name__ == '__main__':
    app.run(debug=True)


