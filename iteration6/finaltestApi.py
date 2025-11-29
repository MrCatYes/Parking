import ssl
from time import sleep
from pymongo import MongoClient
import serial
from final import iteration6
from final import iteration1

ser = serial.Serial('COM3', 9600, timeout=1)
ser.flush()

clientEmploye = MongoClient("mongodb+srv://MrCatYes:Password123@cluster0.mkzbj.mongodb.net/Employe?"
                            "retryWrites=true&w=majority", ssl_cert_reqs=ssl.CERT_NONE)
db = clientEmploye.Parking
CollectionEmploye = db.Employe

while True:
    try:
        # number sent by thge Arduino
        number = ser.read()
        print(number)
        if number != b'':  # no data sent
            if int.from_bytes(number, byteorder='big') == 18:  # random value sent by the arduino if an object is detected

                print("Vehicule devant la barriere")

                immatriculation =  finalImage.image()
                print(immatriculation)
                personne = CollectionEmploye.find_one({"Immatriculation": immatriculation})

                if personne['Stationnement']:
                    # sending value 1 to the Arduino if parking is true
                    stationnement_byte = 1
                    print("Sending number " + str(stationnement_byte) + " to Arduino.")
                    ser.write(str(stationnement_byte).encode('utf-8'))
                    print("Stationnement autorisé")
                    print(personne['LastName'])
                    ser.write((personne['FirstName'] + ' ' +personne['LastName']).encode())


                else:
                    # sending value 0 to the Arduino if parking is false
                    stationnement_byte = 0
                    print("Sending number " + str(stationnement_byte) + " to Arduino.")
                    ser.write(str(stationnement_byte).encode('utf-8'))
                    print("Stationnement refusé")
    except:
            print('Une erreure est survenue')
            ser.write(str(0).encode('utf-8'))

#    clientEmploye.close();
# test f566bg True
# test n648ht False
