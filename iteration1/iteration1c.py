import ssl
from datetime import date, datetime

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


immatriculation = input('Veuillez entrer l\'immatriculation ')
try:
    personne = CollectionEmploye.find_one({'Immatriculation ': immatriculation.upper()})
    if personne['Stationnement']:
        print('Accès autorisé')
        CollectionEntrees.insert_one({'id': (personne['_id']), 'Date': datetime.now(),
                                      'Immatriculation': immatriculation.upper()})

    elif not personne['Stationnement']:
        print('Accès refusé')
        CollectionRefus.insert_one({'id': (personne['_id']), 'Date': datetime.now(),
                                    'Immatriculation': immatriculation})

except Exception as e:
    print('Skip')

try:
    immatriculation = input('Veuillez entrer l\'immatriculation ')
    entrees = CollectionEntrees.count_documents({'Immatriculation': immatriculation})
    personne = CollectionEmploye.find_one({'Immatriculation': immatriculation})
    print('{} {} est entré(e) {} fois'.format(personne['FirstName'], personne['LastName'], entrees))

except Exception as e:
    print('Skip')

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

choice = int(input('Pour connaitre le nombre d\'entrées par jour veuillez entrer: 1 .  \n'
                   'Pour connaitre le nombre d\'entrées par semaine veuillez entrer: 2 .  \n'
                   'Pour connaitre le nombre d\'entrées par mois veuillez entrer: 3 .  \n'
                   'Pour connaitre le nombre d\'entrées par année veuillez entrer: 4 .  \n'
                   'Pour connaitre le nombre de refus veuillez entrer: 5. \n'
                   'Pour toutes ces option veuillez entrer: 6 '))
if choice == 1:
    for x in entreesDays:
        print('Le {} {}, {} voiture(s) sont entrées dans le stationnement'
              .format(x['_id']['day'], month_str(x['_id']['month']), x['Totalcount']))

if choice == 2:
    for x in entreesWeek:
        print('La semaine {}, {} voiture(s) sont entrées dans le stationnement'.format(x['_id']['week'], x['Totalcount']))

if choice == 3:
    for x in entreesMonth:
        print('Durant le mois de {}, {} voiture(s) sont entrées dans le stationnement'
              .format(month_str(x['_id']['month']), x['Totalcount']))
if choice == 4:
    for x in entreesYear:
        print('Durant l\'année {}, {} voiture(s) sont entrées dans le stationnement'
              .format(month_str(x['_id']['year']), x['Totalcount']))

if choice == 5:
    refus = CollectionRefus.estimated_document_count()
    print('{} ont été refusé au stationnement'.format(refus))

if choice == 6:
    for a in entreesDays:
        print('Le {} {}, {} voiture(s) sont entrées dans le stationnement'
              .format(a['_id']['day'], month_str(a['_id']['month']), a['Totalcount']))
    print()

    for x in entreesWeek:
        print('La semaine {}, {} voiture(s) sont entrées dans le stationnement'.format(x['_id']['week'], x['Totalcount']))
    print()

    for y in entreesMonth:
        print('Durant le mois de {}, {} voiture(s) sont entrées dans le stationnement'
              .format(month_str(y['_id']['month']), y['Totalcount']))
    print()

    for z in entreesYear:
        print('Durant l\'année {}, {} voiture(s) sont entrées dans le stationnement'
              .format(z['_id']['year'], z['Totalcount']))
        refus = CollectionRefus.estimated_document_count()
        print('{} ont été refusé au stationnement'.format(refus))
