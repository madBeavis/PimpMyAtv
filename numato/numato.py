import sys
import telnetlib
import time
import re
from argparse import ArgumentParser
from enum import Enum, unique
from codecs import encode


@unique
class Separator(Enum):
    Plain = 0
    Comma = 1
    Space = 2


###################################
# functions
###################################
def connectToDevice(DeviceIPAddress):
    # Wait for login prompt from device and enter user name when prompted
    telnet_obj.read_until(b"login")
    telnet_obj.read_until(b"Name: ")
    telnet_obj.write(user.encode('ascii') + b"\r\n")

    # Wait for password prompt and enter password when prompted by device
    telnet_obj.read_until(b"Password: ")
    telnet_obj.write(password.encode('ascii') + b"\r\n")

    # Wait for device response
    log_result = telnet_obj.read_until(b"successfully\r\n")
    telnet_obj.read_until(b">")

    # Check if login attempt was successful
    if b"successfully" in log_result:
        return True
    elif "denied" in log_result:
        return False


# power off a list of devices
def powerOffDevices(devices, delay, wait, silent=False):
    i = 1
    count_devices = len(devices)

    for this_device in devices:
        if not silent:
            print("Powering off device " + this_device)

        telnet_obj.write(("relay off " + this_device + "\r\n").encode())
        time.sleep(wait)

        # Empty the input buffer
        telnet_obj.read_until(b">")

        if count_devices > 1 and not silent:
            progressBar(i, count_devices, 32)
            i += 1;

        time.sleep(delay)

    if not silent:
        print('\n')  # new line for progress bar
    return True, devices


# power on a list of devices


def powerOnDevices(devices, delay, wait, silent=False):
    i = 1
    count_devices = len(devices)

    for device_on in devices:
        if not silent:
            print("Powering on device " + device_on)

        telnet_obj.write(("relay on " + device_on + "\r\n").encode())
        time.sleep(wait)

        # Empty the input buffer
        telnet_obj.read_until(b">")

        if count_devices > 1 and not silent:
            progressBar(i, count_devices, 32)
            i += 1;

        time.sleep(delay)

    if not silent:
        print('\n')  # new line for progress bar
    return True, devices


# power cycle a list of devices


def powerCycleDevices(devices, delay, wait, silent=False):
    if not silent:
        print("Powering cycling devices " + devices)

    i = 1
    count_devices = len(devices)

    for device_cycle in devices:
        # power off device
        telnet_obj.write(("relay off " + device_cycle + "\r\n").encode())
        time.sleep(wait)

        telnet_obj.write(("relay on " + device_cycle + "\r\n").encode())
        time.sleep(wait)

        # Empty the input buffer
        ret = telnet_obj.read_until(b">")

        if count_devices > 1 and not silent:
            progressBar(i, count_devices, 32)
            i += 1;

        time.sleep(delay)

    if not silent:
        print('\n')  # new line for progress bar
    return True, devices


# reset the relay module


def resetRelayModule():
    telnet_obj.write(b"reset\r\n")
    return "\nReset successfully\n"


def getRelayStatusAll():
    """Retrieve and print whole relay status"""

    # Send Command
    telnet_obj.write(b"relay readall\r\n")
    time.sleep(1)

    # Read Relay Status
    response = telnet_obj.read_until(b">")
    power_values_hex = response.decode()[:-2]

    power_values = bin(int(power_values_hex, 16))[2:].zfill(32)[::-1]

    return power_values


def getRelayStatus(devices, delay):

    # Send Command
    telnet_obj.write(b"relay readall\r\n")
    time.sleep(delay)

    # Read Relay Status
    response = telnet_obj.read_until(b">")
    power_values_hex = response.decode()[:-2]

    power_values = bin(int(power_values_hex, 16))[2:].zfill(32)[::-1]
    return_power_values = ''

    for this_device_status in devices:
        ordinal = ord(this_device_status)
        if ordinal <= 57:
            index = ordinal - 48
        else:
            index = ordinal - 65 + 10

        return_power_values = return_power_values + power_values[index]

    return return_power_values


def fixUpDeviceNames(devices):
    device_list = ""

    # remove quotation marks in case user enclosed
    devices = devices.replace('"', '').replace("'", '')

    # check for flag for all devices
    if 'Z' in devices.upper():
        return "0123456789ABCDEFGHIJKLMNOPQRSTUV", Separator.Plain

    # check different types of ways we seperate
    if ',' in devices:  # check if comma separated for relays
        list_of_devices = devices.split(',')

        for this_device in list_of_devices:
            if this_device == "":
                print("Empty device specified, so it will be ignored\n")
            elif int(this_device) < 0:
                print("Device below zero specified, so it will be ignored\n")
            elif int(this_device) < 32:
                if int(this_device) > 9:
                    device_list = device_list + chr(55 + int(this_device))
                else:
                    device_list = device_list + this_device
            else:
                print("Device above 31 specified, so it will be ignored\n")

        # exit as we are done
        return device_list, Separator.Comma
    elif ' ' in devices:
        list_of_devices = devices.split(' ')

        for this_device in list_of_devices:
            if this_device == "":
                print("Empty device specified, so it will be ignored\n")
            elif int(this_device) < 0:
                print("Device below zero specified, so it will be ignored\n")
            elif int(this_device) < 32:
                if int(this_device) > 9:
                    device_list = device_list + chr(55 + int(this_device))
                else:
                    device_list = device_list + this_device
            else:
                print("Device above 31 specified, so it will be ignored\n")

        # exit as we are done
        return device_list, Separator.Comma

    # check for numato naming convention for relays
    for this_character in devices.upper():
        if re.match("[0-9]|[A-V]", this_character):
            device_list += this_character
        else:
            print("Invalid character in devices, allowed range of 0-9 and A-V\n")
            exit(0)

    return device_list, Separator.Plain;


def fixUpPowerOptions(power_options):
    option_list = ""

    # remove quotation marks in case user enclosed
    power_options = power_options.replace('"', '').replace("'", '')

    if ',' in power_options:
        list_of_poweroptions = power_options.split(',')

        for this_option in list_of_poweroptions:
            option_list = option_list + this_option

        return option_list, Separator.Comma
    elif ' ' in power_options:
        list_of_poweroptions = power_options.split(' ')

        for this_option in list_of_poweroptions:
            option_list = option_list + this_option

        return option_list, Separator.Space
    else:
        return power_options, Separator.Plain


def progressBar(value, endvalue, bar_length=32):
    percent = float(value) / endvalue
    arrow = '-' * int(round(percent * bar_length) - 1) + '>'
    spaces = ' ' * (bar_length - len(arrow))

    sys.stdout.write("\rPercent: [{0}] {1}%".format(arrow + spaces, int(round(percent * 100))))
    sys.stdout.flush()


#########################################################################################
#                                    Main entry                                         #
#########################################################################################

# This code works with python3 and above
# Check the python version
if sys.version_info[0] < 3:
    raise Exception("Python version 3.x required")

# Setup arguments
parser = ArgumentParser()

group1 = parser.add_mutually_exclusive_group()
group1.add_argument("-ak", "--all_kill", action="store_true", dest='kill_all',
                    help="Turn off all devices")
group1.add_argument("-ao", "--all_on", action="store_true", dest='all_on',
                    help="Turn on all devices")
group1.add_argument("-pca", "--all_power_cycle", action="store_true", dest='power_cycle_all',
                    help="Power cycle devices all devices, i.e. off then on")
group1.add_argument("-pc", "--power_cycle", action="store_true", dest='power_cycle',
                    help="Power cycle devices, i.e. off then on")
group1.add_argument("-r", "--reset", action="store_true", dest='reset',
                    help="Reset the relay module")
group1.add_argument("-s", "--status", dest="status", action="store_true",
                    help="Query the status of devices")
group1.add_argument("-po", "--power_options", dest="power_options", type=str,
                    help="Power options to use for specified devices.  Use 0 for off, 1 for on and 3 for power cycle "
                         "(off then on)")

parser.add_argument("-d", "--devices", dest="devices", type=str,
                    help="Devices to utilize in operation.  Use Z for all devices.")
parser.add_argument("-dy", "--delay", type=float, dest="delay", default=0.1,
                    help="Delay to add between device operations in seconds, default = 0.1")
parser.add_argument("-w", "--wait", type=float, dest="wait",
                    help="Delay to wait after commands, default = 0.2, must be greater than 0.1", default=0.2)
parser.add_argument("-ip", "--ip_address", type=str, dest='ip_address',
                    help="IP address of relay board", default="192.168.8.5")
parser.add_argument("-off", "--off_first", dest='off_first',
                    help="Power off all devices before turning on devices")
parser.add_argument('-si', '--silent', dest='silent', help='Suppress feedback from program', action='store_true')
parser.add_argument('-ti', '--timeout', dest='timeout', help='Timeout for telnet connection, default=5', type=int, default=5)
parser.add_argument('-port', '--port', dest='port', help='Port to use for telnet connection, default=23', type=int, default=23)
parser.add_argument('-user', '--username', dest='username', help='Username to log into board with, default=admin', type=str, default ='admin')
parser.add_argument('-pwd', '--password', dest='password', help='Password to log into board with, default=admin', type=str, default='admin')

args = parser.parse_args()

# Setup device and login info
DeviceIP = args.ip_address  # Device IP address
user = args.username  # Device Telnet user name
password = args.password # Device Telnet password

# checks for options to run
if args.devices is None and args.status is not None:
    # test for status checking of devices
    print("Provide a device list to check the status of devices\n")

# clean up devices
my_devices = ""
my_devices_is_comma_delimited = Separator.Plain

if args.devices is not None:
    my_devices, my_devices_is_comma_delimited = fixUpDeviceNames(args.devices)

# clean up power options
my_power_options = ""
my_power_options_is_comma_delimited = Separator.Plain
if args.power_options is not None:
    my_power_options, my_power_options_is_comma_delimited = fixUpPowerOptions(args.power_options)

    # loop through power options and test for valid values
    for character in args.power_options:
        if not re.match("[013]", character):
            print(
                "Invalid character in power_options, allowed range of off=0, on=1 and powercycle=3\n")
            exit(0)

if my_devices_is_comma_delimited != my_power_options_is_comma_delimited:
    print('Delimiter used in power and devices must be the same!')
    exit(0)

# check for mismatch in power options and devices
if args.devices is not None and args.power_options is not None:
    # Test that length of devices matches power options
    if len(my_devices) != len(my_power_options):
        print("Length of devices does not match power options\n")
        exit(0)

# Create a new TELNET object
telnet_obj = telnetlib.Telnet(host=DeviceIP, timeout=args.timeout, port=args.port)

# Connect to the device using credentials provided
if connectToDevice(DeviceIP):
    print("\nLogged in successfully... Connected to device", DeviceIP, "\n")

    if args.reset:  # reset relay module
        resetRelayModule()

    elif args.kill_all:  # kill power to all relays
        devices_to_kill = fixUpDeviceNames('Z')
        powerOffDevices(devices=devices_to_kill, delay=args.delay, wait=args.wait, silent=args.silent)

    elif args.all_on:  # power on all devices
        devices_on = fixUpDeviceNames('Z')

        if args.off_first:
            powerOffDevices(devices=devices_on, delay=args.delay, wait=args.wait, silent=args.silent)

        powerOnDevices(devices=devices_on, delay=args.delay, wait=args.wait, silent=args.silent)

    elif args.power_cycle_all:  # power cycle all devices that are currently on
        devices_to_power_cycle = getRelayStatus(fixUpDeviceNames('Z')[0])

        for device_to_power_cycle in devices_to_power_cycle:
            if device_to_power_cycle == '1':
                powerCycleDevices(devices=device_to_power_cycle, delay=args.delay, wait=args.wait, silent=args.silent)

    elif my_devices != "" and args.power_cycle:  # power cycle specified devices
        # power cycle devices
        powerCycleDevices(devices=my_devices, delay=args.delay, wait=args.wait, silent=args.silent)

    elif args.power_cycle and args.devices is None:
        devices_status = fixUpDeviceNames('Z')

        # loop through status, write the
        char_pos = 55
        devices_to_cycle = ''
        for this_device in devices_status:
            if this_device == '1':
                devices_to_cycle = devices_to_cycle + ascii(char_pos)

            char_pos += 1  # increment pointer to character

        powerCycleDevices(devices=devices_to_cycle, delay=args.delay, wait=args.wait, silent=args.silent)

    # apply power options
    elif my_power_options != "" and my_devices != "":
        # loop through devices and set their power option
        i = 0
        for device in my_devices:
            power_character = my_power_options[i]

            if power_character == '0':
                powerOffDevices(devices=device, delay=args.delay, wait=args.wait, silent=args.silent)
            elif power_character == '1':
                powerOnDevices(devices=device, delay=args.delay, wait=args.wait, silent=args.silent)
            elif power_character == '3':
                powerCycleDevices(devices=device, delay=args.delay, wait=args.wait, silent=args.silent)

            i += 1

    elif args.status and args.devices is None:
        devices = fixUpDeviceNames('Z')[0]
        returnValue = getRelayStatus(devices, delay=args.delay)

        print("Power Status for Device(s)")
        print('Devices: ' + devices)
        print('Status:  ' + returnValue)
        print("")

        exit(returnValue)

    elif args.status and my_devices != "":
        returnValue = getRelayStatus(my_devices, delay=args.delay)

        print("Power Status for Device(s)")
        print("Devices:  " + my_devices)
        print("Status:   " + returnValue)
        print("")

        exit(returnValue)
else:
    print("Login failed!!!! Please check login credentials or Device IP Address\n")
    telnet_obj.close()
    exit(0)
