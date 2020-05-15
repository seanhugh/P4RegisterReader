#!/usr/bin/env python


# Import Necessary Packages
from p4utils.utils.topology import Topology
from p4utils.utils.sswitch_API import SimpleSwitchAPI
import sys
import os
import time
import signal
from threading import Event
from p4utils.utils.topology import Topology

# Utility Functions
# Borrowed from: https://stackoverflow.com/questions/1265665/how-can-i-check-if-a-string-represents-an-int-without-using-try-except
def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def ContainsWhiteSpace(s):
    return(' ' in s)

def getRegisterNameWidth():
    # Does file exist?
    f = open("registerData.txt", "r")
    file_contents = f.read()
    data = (file_contents.split(" "))
    return(data)


# Script for dynamic register name and size
def existsRegisterName():
    # Does file exist?
    if (os.path.isfile('registerData.txt')):
        f = open("registerData.txt", "r")
        file_contents = f.read()

        data = (file_contents.split(" "))

        print("Register Name: " + data[0])
        print("Register Size: " + data[1])

        if len(data) == 2:
            return True
    return False

# Script for dynamic register name and size
def writeRegisterName():
    loopMe = True

    print("")
    print("Please enter the register name and size below:")

    while(loopMe):

        # Get input values
        write_value = ''
        registerName = str(raw_input("Enter register name: "))

        if(ContainsWhiteSpace(registerName)):
            print("ERROR. Register name cannot contain spaces")

        else:

            while(loopMe):

                registerSize = str(raw_input("Enter register size (int): "))

                if(not ContainsWhiteSpace(registerSize)):

                    if(RepresentsInt(registerSize)):
                        loopMe = False
                    else:
                        print("ERROR. Register size must be an integer")
                else:
                    print("ERROR. Register size cannot contain spaces")


    # Write out values
    f = open("registerData.txt", "w")
    f.write(registerName + " " + registerSize)

f_qlen = {}

def handler(signum, frame):
    for link in f_qlen:
        f_qlen[link].close()
    sys.exit("exit...")

class ReadCounters(object):
    # initialize register reader
    def __init__(self, sw_name):
        self.topo = Topology(db="./topology.db")
        self.sw_name = sw_name
        self.thrift_port = self.topo.get_thrift_port(sw_name)
        self.controller = SimpleSwitchAPI(self.thrift_port)

    def get_qlen(self):
        packets = []

        data = getRegisterNameWidth()
        registerWidth = int(data[1])
        registerName = data[0]

        for i in range(0, registerWidth):
            packets.append(self.controller.register_read(registerName, i))
        return (packets)

# def writeRegisterName():
#     with open("filename.txt", "r")

if __name__ == "__main__":

    # ======================= Gets the user input... If their usage is wrong, print the instructions ====================

    if len(sys.argv) != 2:
        print """\
        Welcome to the P4 Register Reader :)

        USAGE:

        **** prints a single switch's register values ****
        python p4registerreader.py [SWITCH NAME]  

        **** prints all switch's register values ****
        python p4registerreader.py a

        **** update the name of the register you are reading **** 
        python p4registerreader.py u

        """
        sys.exit(0)

    else:

        # Input is correct, so we will decide which action to take
        actionType = sys.argv[1]

        if (actionType != "u"):

            # 1) Make sure we have a register name
            if(not existsRegisterName()):
                writeRegisterName()

            # Set the switch values

            if(actionType == "a"):

                topo = Topology(db="./topology.db")

                # Get all the switches
                switches = topo.get_p4switches().keys()

            else:
                switches = [actionType] # Just the inputted switch
            
            # Read the bloom filter and output the register for each of these switches
            signal.signal(signal.SIGINT, handler)

            # We write data into files for each link
            for switch in switches:
                
                # Get the register value
                handler = ReadCounters(switch)
                res = handler.get_qlen()
                print("========================")
                print("SWITCH NAME: " + switch)
                print("Register Data:")
                print(res)
                print("")

        else:
            writeRegisterName()
