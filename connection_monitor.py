import os
import sys
import socket
import datetime
import time

FILE = os.path.join(os.getcwd(), "networkinfo.log")

def ping(host):
	try:
		socket.setdefaulttimeout(3)

		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		port = 53

		server_address = (host, port)
		s.connect(server_address)

	except OSError as error:
		return False

	else:
		s.close()
		return True


def calculate_time(start, stop):

	difference = stop - start
	seconds = float(str(difference.total_seconds()))
	return str(datetime.timedelta(seconds=seconds)).split(".")[0]


def first_check(host):

	if ping(host):
		live = "\n--------CONNECTION SUCCESSFUL--------\n"
		print(live)
		connection_acquired_time = datetime.datetime.now()
		acquiring_message = "Online:            " + \
			str(connection_acquired_time).split(".")[0]
		print(acquiring_message)

		with open(FILE, "a") as file:
		
			file.write(live)
			file.write(acquiring_message)

		return True

	else:
		not_live = "\n--------CONNECTION FAILED--------\n"
		print(not_live)

		with open(FILE, "a") as file:
		
			file.write(not_live)
		return False

def IP_check(host): #Brandon
	print(host)
	if ping(host):
		live = "--DEVICE ONLINE---\n"
		print(live)

		return True

	else:
		not_live = "--DEVICE OFFLINE--\n"
		print(not_live)
  
		return False


def monitor(host):
	monitor_start_time = datetime.datetime.now()
	monitoring_date_time = "Monitoring Starts: " + \
		str(monitor_start_time).split(".")[0]

	if first_check(host):
		print(monitoring_date_time)

	else:
		while True:
		
			if not ping(host):
				
				time.sleep(1)
			else:
				
				first_check(host)
				print(monitoring_date_time)
				break

	with open(FILE, "a") as file:
	
		file.write("\n")
		file.write(monitoring_date_time + "\n")

	while True:
	
		if ping(host):
			
			time.sleep(5)

		else:
			down_time = datetime.datetime.now()
			fail_msg = "Offline at:        " + str(down_time).split(".")[0]
			print(fail_msg)

			with open(FILE, "a") as file:
				file.write(fail_msg + "\n")

			while not ping(host):
			
				time.sleep(1)

			up_time = datetime.datetime.now()
			
			uptime_message = "Reconnected:       " + str(up_time).split(".")[0]

			down_time = calculate_time(down_time, up_time)
			unavailablity_time = "Down-Time:         " + down_time

			print(uptime_message)
			print(unavailablity_time)

			with open(FILE, "a") as file:
				
				file.write(uptime_message + "\n")
				file.write(unavailablity_time + "\n")

#monitor()
