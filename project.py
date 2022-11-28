from database import db
import scapy.all as scapy
from sqlalchemy_utils import database_exists
from database import device
from send_alert import send_email

def netscan():
    request = scapy.ARP()

    request.pdst = '192.168.1.1/24'
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
            
def verify():
    addr = input("Please enter device's ip address (11 char) or mac address (17 char):\n")

    if(len(addr) == 11):
        temp = device.query.filter_by(ip = addr).first()

        if(temp):
            temp.verified = True
            db.session.commit()
            print("Device Verified - Mac:", temp.mac, " Ip:", temp.ip, "\n")
        else:
            print("Invalid Ip Address Entered\n")
    elif(len(addr) == 17):
        temp = device.query.filter_by(mac = addr).first()

        if(temp):
            temp.verified = True
            db.session.commit()
            print("Device Verified - Mac:", temp.mac, " Ip:", temp.ip, "\n")
        else:
            print("Invalid Mac Address Entered\n")
    else:
        print('Invalid Address Entered\n')

def devList():
    temp = device.query.all()

    if(temp):
        for i in temp:
            print("Mac:", i.mac, " Ip:", i.ip, " Verified:", i.verified, "\n")
    else:
        print("There are no devices in the database.\n")

def deldb():
    device.query.delete()
    db.session.commit()

def paCap(IPA):
    #packets = sniff(filter="ether host 00:a3:8e:23:ae:8b")
    packet = scapy.IP(src=f"{IPA}")
    scapy.wrpcap("captured.pcap",packet)
    packet.show()


def main():
    if not database_exists('sqlite:///devices.db'):
        db.create_all()
    IPA = "192.168.1.0" #PLACEHOLDER
    while(True):
        option = input("Please select an option (To quit, input anything else):\n1. Scan Network for Devices\n2. Send Email for all non-verified devices\n3. Verify Device (Given ip address or mac address)\n4. View list of devices\n5. Delete all devices from database\n6. Packet capture test\n")

        if(option == "1"):
            netscan()
        elif(option == "2"):
            send_email(IPA)
        elif(option == "3"):
            verify()
        elif(option == "4"):
            devList()
        elif(option == "5"):
            deldb()
        elif(option == "6"):
            paCap(IPA)
        else:
            break

if __name__ == "__main__":
    main()