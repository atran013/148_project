#Referenced for general scapy usage:
#https://scapy.readthedocs.io/en/latest/usage.html
#https://scapy.readthedocs.io/en/latest/extending.html
#https://wiki.sans.blue/Tools/pdfs/ScapyCheatSheet_v0.2.pdf
from database import db
import scapy.all as scapy
from sqlalchemy_utils import database_exists
from database import device
from send_alert import send_email
from connection_monitor import monitor
from connection_monitor import IP_check
import socket as socket

def netscan(): #Andrew
    #Referenced Code: https://www.geeksforgeeks.org/network-scanning-using-scapy-module-python/
    request = scapy.ARP()

    hostname = socket.gethostname()
    IPA = socket.gethostbyname(hostname)
    parts = IPA.split(".")

    request.pdst = (parts[0] + "." + parts[1] + "." + parts[2] + ".0/24")
    broadcast = scapy.Ether()

    broadcast.dst = 'ff:ff:ff:ff:ff:ff'

    request_broadcast = broadcast/request
    clients = scapy.srp(request_broadcast, timeout = 1)[0]

    for element in clients:
        print(element[1].psrc + "  " + element[1].hwsrc)
        if(not device.query.filter_by(mac = element[1].hwsrc).first()):
            new_device = device(mac = element[1].hwsrc, ip = element[1].psrc, verified = False)
            db.session.add(new_device)
            db.session.commit()

            print("New Device Added - Mac:", element[1].hwsrc, " Ip:", element[1].psrc, " Verified:", "False\n")
            
def verify(): #Andrew
    addr = input("Please enter device's ip address:\n")

    temp = device.query.filter_by(ip = addr).first()

    if(temp):
        temp.verified = True
        db.session.commit()
        print("Device Verified - Mac:", temp.mac, " Ip:", temp.ip, "\n")
    else:
        print("Invalid Ip Address Entered\n")

def devList(): #Andrew
    temp = device.query.all()

    if(temp):
        for i in temp:
            print("Mac:", i.mac, " Ip:", i.ip, " Verified:", i.verified, "\n")
    else:
        print("There are no devices in the database.\n")

def deldb(): #Andrew
    device.query.delete()
    db.session.commit()

def sendforunverified(): #Andrew
    temp = device.query.all()

    if(temp):
        for i in temp:
            paCap(i.ip)
            send_email(i.ip)
    else:
        print("There are no devices in the database.\n")

def paCap(IPA): #Brandon
    packet = scapy.IP(src=f"{IPA}")
    scapy.wrpcap("captured.pcap",packet)
    packet.show()

def status(): #Brandon
    IPA = input("Input IP address:\n")
    IP_check(IPA)


def main(): #Andrew
    if not database_exists('sqlite:///devices.db'):
        db.create_all()

    while(True):
        option = input("Please select an option (To quit, input letter):\n1. Scan Network for Devices\n2. Send Email for all Non-Verified devices\n3. Verify Device (Given IP Address)\n4. View list of devices\n5. Check device status\n6. Delete all devices from database\n7. Main Device Status Monitor (Ctrl+C to End)\n")

        if(option == "1"):
            netscan()
        elif(option == "2"):
            sendforunverified()
        elif(option == "3"):
            verify()
        elif(option == "4"):
            devList()
        elif(option == "5"):
            status()
        elif(option == "6"):
            deldb()
        elif(option == "7"):
            host = "8.8.8.8"
            monitor(host)
        else:
            break

if __name__ == "__main__":
    main()