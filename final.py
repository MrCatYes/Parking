import ssl
from time import sleep, time
from pymongo import MongoClient
import serial
import ssl
from datetime import date, datetime

from iteration6 import iteration6a
from iteration1 import iteration1c



clientEmploye = MongoClient("mongodb+srv://MrCatYes:Password123@cluster0.mkzbj.mongodb.net/Employe?"
                            "retryWrites=true&w=majority", ssl_cert_reqs=ssl.CERT_NONE)
db = clientEmploye.Parking
CollectionEmploye = db.Employe
totalEntries = iteration1c.entreeTotal_Day()
print(totalEntries)

import os
import sys
import inspect
from alive.aliot.aliot import alive_iot as iot

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

projectId = '8df1fcc5-de2e-4433-a03a-901b28364283'

# Url pour se connecter au services du site
iot.ObjConnecteAlive.set_url("wss://alivecode.ca/iotgateway/")

# Id de votre objet connecté
my_iot = iot.ObjConnecteAlive(
    key="c159d76b-5fb2-41a9-9c77-756653e1bac2"
)

from pymongo import MongoClient

clientEmploye = MongoClient("mongodb+srv://MrCatYes:Password123@cluster0.mkzbj.mongodb.net/Employe?"
                            "retryWrites=true&w=majority", ssl_cert_reqs=ssl.CERT_NONE)
clientEntree = MongoClient("mongodb+srv://MrCatYes:Password123@cluster0.mkzbj.mongodb.net/Entrees?"
                           "retryWrites=true&w=majority", ssl_cert_reqs=ssl.CERT_NONE)
clientRefus = MongoClient("mongodb+srv://MrCatYes:Password123@cluster0.mkzbj.mongodb.net/Refus?"
                          "retryWrites=true&w=majority", ssl_cert_reqs=ssl.CERT_NONE)
db = clientEmploye.Parking
CollectionEmploye = db.Employe
CollectionEntrees = db.Entrees
CollectionRefus = db.Refus


def month_str(month_number):
    month_string = datetime.strptime(str(month_number), "%m")
    month_strin = month_string.strftime('%B')
    return month_strin


@my_iot.main_loop(1)
def main():
    entreesYear = CollectionEntrees.aggregate([
        {'$project': {'year': {'$year': "$Date"}}},
        {"$group": {"_id": {"year": "$year"}, "Totalcount": {"$sum": 1}}, },
    ])
    entreesMonth = CollectionEntrees.aggregate([

        {'$project': {'year': {'$year': "$Date"}, 'month': {'$month': '$Date'}}},
        {"$group": {"_id": {"year": "$year", 'month': '$month'}, "Totalcount": {"$sum": 1}}, },
    ])
    entreesDays = CollectionEntrees.aggregate([

        {'$project': {'year': {'$year': "$Date"}, 'month': {'$month': '$Date'}, 'day': {'$dayOfMonth': '$Date'}}},
        {"$group": {"_id": {"year": "$year", 'month': '$month', 'day': '$day'}, "Totalcount": {"$sum": 1}}, },
    ])
    entreesWeek = CollectionEntrees.aggregate([

        {'$project': {'year': {'$year': "$Date"}, 'month': {'$month': '$Date'}, 'week': {'$week': '$Date'}}},
        {"$group": {"_id": {"year": "$year", 'month': '$month', 'week': '$week'}, "Totalcount": {"$sum": 1}}, },
    ])

    for a in entreesDays:
        day = '{} '.format(a['_id']['day'])
        month = '{} '.format(month_str(a['_id']['month']))
        totalCount = '{} '.format(a['Totalcount'])
        print('Le {} {}, {} voiture(s) sont entrées dans le stationnement'
              .format(a['_id']['day'], month_str(a['_id']['month']), a['Totalcount']))
        my_iot.send_route(projectId + '/choix1',
                          {'Day': day, 'Month': month, 'TotalCount': totalCount})
        sleep(1)

    print()

    for x in entreesWeek:
        week = '{} '.format(x['_id']['week'])
        totalCount = '{} '.format(x['Totalcount'])
        print(
            'La semaine {}, {} voiture(s) sont entrées dans le stationnement'.format(x['_id']['week'],
                                                                                     x['Totalcount']))
        my_iot.send_route(projectId + '/choix2',
                          {'Week': week, 'TotalCount': totalCount})
    print()

    for y in entreesMonth:
        month = '{} '.format(month_str(y['_id']['month']))
        totalCount = '{} '.format(y['Totalcount'])
        print('Durant le mois de {}, {} voiture(s) sont entrées dans le stationnement'
              .format(month_str(y['_id']['month']), y['Totalcount']))
        my_iot.send_route(projectId + '/choix3',
                          {'Month': month, 'TotalCount': totalCount})
    print()

    for z in entreesYear:
        year = '{}'.format(z['_id']['year'])
        totalCount = '{}'.format(z['Totalcount'])

        print('Durant l\'année {}, {} voiture(s) sont entrées dans le stationnement'
              .format(z['_id']['year'], z['Totalcount']))
        my_iot.send_route(projectId + '/choix4',
                          {'Year': year, 'TotalCount': totalCount})

        refus = CollectionRefus.estimated_document_count()

        refuse = '{}'.format(refus)
        print('{} ont été refusé au stationnement'.format(refus))

        my_iot.send_route(projectId + '/choix5', {'Acces': refuse})
    ser = serial.Serial('COM3', 9600, timeout=1)
    ser.flush()
    sleep(6)
    ser.write(str(totalEntries).encode('utf-8'))
    ser.flush()
    while True:
        try:

            # number sent by the Arduino
            number = ser.read()
            print(number)

            if number != b'':  # no data sent
                if int.from_bytes(number,
                                  byteorder='big') == 18:  # random value sent by the arduino if an object is detected

                    print("Vehicule devant la barriere")

                    immatriculation = iteration6a.image()
                    print(immatriculation)
                    personne = CollectionEmploye.find_one({"Immatriculation": immatriculation.upper()})
                    if personne['Stationnement']:
                        # sending value 1 to the Arduino if parking is true
                        stationnement_byte = 'accepte'
                        print("Sending number " + str(stationnement_byte) + " to Arduino.")
                        ser.write(str(stationnement_byte).encode('utf-8'))
                        sleep(2)
                        print("Stationnement autorisé")
                        print(personne['LastName'])
                        ser.flush()
                        ser.write((personne['FirstName'] + ' ' + personne['LastName']).encode())
                        sleep(6)




                    else:
                        # sending value 0 to the Arduino if parking is false
                        stationnement_byte = 'refuse'
                        print("Sending number " + str(stationnement_byte) + " to Arduino.")
                        ser.write(str(stationnement_byte).encode('utf-8'))
                        print("Stationnement refusé")
                        sleep(3.5)

        except:
            print('Une erreure est survenue')
            ser.flush()


my_iot.begin()
# clientEmploye.close();
# test f566bg True
# test n648ht False
