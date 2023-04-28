from joblib import load 
from typing import Optional 
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import sqlite3
from fastapi import FastAPI, HTTPException, Request
from jose import jwt
import hashlib
import FastApi.crud as crud

app = FastAPI()

class User(BaseModel):
    pseudo: str
    email: str
    mdp: str
    jwt: str

class UserRegister(BaseModel):
    pseudo : str
    email: str
    mdp: str
    
class PrixReel(BaseModel):
    prediction_id : int
    prix_reel : int 
    
class Prediction(BaseModel):
    symboling:int
    CompanyName:object
    CarModel:object
    fueltype:object
    aspiration:object
    doornumber:object
    carbody:object
    drivewheel:object
    enginelocation:object
    wheelbase:float
    carlength:float
    carwidth:float
    carheight:float
    curbweight:float
    enginetype:object
    cylindernumber:object
    enginesize:float
    fuelsystem:object
    boreratio:float
    stroke:float
    compressionratio:float
    horsepower:int
    peakrpm:int
    city:float
    highway:float
    
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

def hasher_mdp(mdp:str) -> str:
    return hashlib.sha256(mdp.encode()).hexdigest()

def decoder_token(token:str)->dict:
    return jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)

def verifier_token(req: Request):
    token = req.headers["Authorization"]
    
@app.post("/auth/inscription")
async def inscription(user:UserRegister):
    if len(crud.get_users_by_mail(user.email)) > 0:
        raise HTTPException(status_code=403, detail="L'email fourni possède déjà un compte")
    else:
        id_user = crud.creer_utilisateur(user.pseudo, user.email, hasher_mdp(user.mdp), None)
        token = jwt.encode({
            "email" : user.email,
            "mdp" : user.mdp,
            "id" : id_user
        }, SECRET_KEY, algorithm=ALGORITHM)
        crud.update_token(id_user, token)
        return {"token" : token}

df_cleaned = pd.read_csv('carprice_cleaned.csv')

loaded_model = load('trained_pipe.joblib')

# Connexion à la base de données
conn = sqlite3.connect('car_predictions.db', check_same_thread=False)

@app.post("/predict") # local : http://127.0.0.1:8000/predict
async def predict(data : Prediction, req: Request):
    try:
        decode = decoder_token(req.headers["Authorization"])
        user_id = decode["id"]
    except:
        raise HTTPException(status_code=401, detail="Vous devez être identifié pour accéder à cet endpoint.")
    new_data = {
        "symboling": data.symboling,
        "CompanyName": data.CompanyName,
        "CarModel": data.CarModel,
        "fueltype": data.fueltype,
        "aspiration": data.aspiration,
        "doornumber": data.doornumber,
        "carbody": data.carbody,
        "drivewheel": data.drivewheel,
        "enginelocation": data.enginelocation,
        "wheelbase": data.wheelbase,
        "carlength": data.carlength,
        "carwidth": data.carwidth,
        "carheight": data.carheight,
        "curbweight": data.curbweight,
        "enginetype": data.enginetype,
        "cylindernumber": data.cylindernumber,
        "enginesize": data.enginesize,
        "fuelsystem": data.fuelsystem,
        "boreratio": data.boreratio,
        "stroke": data.stroke,
        "compressionratio": data.compressionratio,
        "horsepower": data.horsepower,
        "peakrpm": data.peakrpm,
        "city_L/100km": data.city,
        "highway_L/100km": data.highway,
        "user_id": user_id
    }
    X_pred = pd.DataFrame([new_data])
    class_idx = loaded_model.predict(X_pred)[0]
    crud.add_prediction_to_database(new_data, class_idx, user_id)
    return class_idx

@app.post("/actualiser_prediction")
async def actualiser_prediction(prix_reel: PrixReel, req: Request) -> None:
    try:
        decode = decoder_token(req.headers["Authorization"])
        user_id = decode["id"]
    except:
        raise HTTPException(status_code=401, detail="Vous devez être identifié pour accéder à cet endpoint.")
    crud.update_prix_reel(user_id, prix_reel.prediction_id, prix_reel.prix_reel)
    return {"detail": "Le prix réel de la voiture a bien été enregistré"}