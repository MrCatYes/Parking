# Projet Parking  - Iteration 4
# Maxime Gagnière - e1967067
# Annia Moussaoui - e1749122
# Malik Chaoui    - e1922179


import ssl

# Import dependencies
import cv2  # This is the OpenCV Python library
import matplotlib.pyplot as plt
import requests
from pymongo import MongoClient


def image():
    clientEmploye = MongoClient("mongodb+srv://MrCatYes:Password123@cluster0.mkzbj.mongodb.net/Employe?"
                                "retryWrites=true&w=majority", ssl_cert_reqs=ssl.CERT_NONE)
    webcam = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Number which capture webcam in my machine
    # try either VideoCapture(0) or (1) based on your camera availability
    # in my desktop it works with (1)
    check, frame = webcam.read()
    cv2.imwrite(filename=r'saved_img.jpg', img=frame)

    db = clientEmploye.Parking
    CollectionEmploye = db.Employe

    carplate_img = cv2.imread('saved_img.jpg')
    plt.subplot(1, 1, 1)
    plt.imshow(carplate_img)
    plt.title("Morph")
    plt.show()

    regions = ['mx', 'us-ca']  # Change to your country
    with open('./saved_img.jpg', 'rb') as fp:
        response = requests.post(
            'https://api.platerecognizer.com/v1/plate-reader/',
            verify=False,
            data=dict(regions=regions),  # Optional
            files=dict(upload=fp),
            headers={'Authorization': 'Token f15f40a4964fa0c579e12bd784a3ef5c391d8c1e'})
        data = response.json()
        immatriculation = data['results'][0]['plate']

    try:

        personne = CollectionEmploye.find_one({"Immatriculation": immatriculation.upper()})
        print('l\'employé: {} {}'.format(personne['FirstName'], personne['LastName']))
        print('access: {}'.format(personne['Stationnement']))
    except:
        print('L\'immatriculation {} n\'est pas enregistrée'.format(immatriculation))

    cv2.destroyAllWindows()

    return immatriculation


