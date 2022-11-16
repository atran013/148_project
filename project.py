from database import db
import scapy.all as scapy
from sqlalchemy_utils import database_exists
from database import device

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
            

def main():
    if not database_exists('sqlite:///devices.db'):
        db.create_all()

    netscan()
    print(device.query.all())


if __name__ == "__main__":
    main()