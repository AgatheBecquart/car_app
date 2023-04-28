from fastapi import HTTPException
from jose import JWTError, jwt
from jose import jwt
import sqlite3


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

def creer_utilisateur(pseudo:str, email:str, mdp:str, jwt:str) -> int:
    """ 
        Cette fonction prend en entrée le pseudo, l'email, le mot de passe et le jeton JWT d'un 
        utilisateur et crée un nouvel enregistrement dans la table "user" de la base de données 
        "car_predictions.db". Elle renvoie l'ID de l'utilisateur créé.
    """
    connexion = sqlite3.connect("car_predictions.db")
    curseur = connexion.cursor()
    curseur.execute("INSERT INTO user VALUES (NULL, ?, ?, ?, ?)", (pseudo, email, mdp, jwt))
    id_user = curseur.lastrowid
    connexion.commit()
    return id_user  

# Fonction pour ajouter une prédiction dans la base de données
def add_prediction_to_database(data, prediction, user_id):
    connexion = sqlite3.connect("car_predictions.db")
    curseur = connexion.cursor()
    curseur.execute("""INSERT INTO car_predictions
                    (symboling, CompanyName, CarModel, fueltype, aspiration, doornumber, carbody, drivewheel, enginelocation, wheelbase,
                    carlength, carwidth, carheight, curbweight, enginetype, cylindernumber, enginesize, fuelsystem, boreratio, stroke,
                    compressionratio, horsepower, peakrpm, city_L_100km, highway_L_100km, prediction, user_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                  (data['symboling'], data['CompanyName'], data['CarModel'], data['fueltype'], data['aspiration'], data['doornumber'],
                   data['carbody'], data['drivewheel'], data['enginelocation'], data['wheelbase'], data['carlength'], data['carwidth'],
                   data['carheight'], data['curbweight'], data['enginetype'], data['cylindernumber'], data['enginesize'], data['fuelsystem'],
                   data['boreratio'], data['stroke'], data['compressionratio'], data['horsepower'], data['peakrpm'], data['city_L/100km'], data['highway_L/100km'],
                   prediction, user_id))
    connexion.commit()

def modifier_utilisateur(id:int, pseudo:str, email:str, mdp:str)-> None:
    """
        Cette fonction prend en entrée l'ID d'un utilisateur ainsi que le nouveau pseudo, l'email et le mot de 
        passe associés. Elle met à jour l'enregistrement correspondant dans la table "user" de la base de données.
    """
    connexion = sqlite3.connect("car_predictions.db")
    curseur = connexion.cursor()
    curseur.execute("UPDATE user SET pseudo=?, email=?, mdp=? WHERE id=?", (pseudo, email, mdp, id))
    connexion.commit()


def supprimer_utilisateur(id:int)-> None:
    """ 
        Cette fonction prend en entrée l'ID d'un utilisateur et supprime l'enregistrement correspondant dans la table
        "user" de la base de données.
    """
    connexion = sqlite3.connect("car_predictions.db")
    curseur = connexion.cursor()
    curseur.execute("DELETE FROM user WHERE id=?", (id,))
    connexion.commit()
    

def update_prix_reel(user_id, prediction_id, prix_reel):
    connexion = sqlite3.connect("car_predictions.db")
    curseur = connexion.cursor()
    curseur.execute("SELECT * FROM car_predictions WHERE user_id = ? AND id = ? AND prix_reel IS NULL", (user_id, prediction_id))
    prediction = curseur.fetchone()
    if prediction:
        curseur.execute("""
            UPDATE car_predictions 
            SET prix_reel = ? 
            WHERE user_id = ? AND id = ? AND prix_reel IS NULL
            """,
            (prix_reel, user_id, prediction_id))
        connexion.commit()
    else:
        print("Erreur : Aucune prédiction trouvée pour cet utilisateur et cette prédiction.")
        
def update_token(id, token:str)->None:
    """
        Cette fonction prend en entrée l'ID d'un utilisateur et un nouveau jeton JWT et met à jour l'enregistrement correspondant dans la table "user"
        de la base de données "car_predictions.db". 
    """
    connexion = sqlite3.connect("car_predictions.db")
    curseur = connexion.cursor()
    curseur.execute("UPDATE user SET jwt = ? WHERE id=?",(token, id))
    connexion.commit()
    connexion.close()
    