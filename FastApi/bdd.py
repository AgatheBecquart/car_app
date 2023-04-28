import sqlite3
connexion = sqlite3.connect("car_predictions.db")
curseur = connexion.cursor()

# Création d'une table pour stocker les prédictions
curseur.execute('''
                CREATE TABLE IF NOT EXISTS car_predictions(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symboling INTEGER,
                    CompanyName TEXT,
                    CarModel TEXT,
                    fueltype TEXT,
                    aspiration TEXT,
                    doornumber TEXT,
                    carbody TEXT,
                    drivewheel TEXT,
                    enginelocation TEXT,
                    wheelbase FLOAT,
                    carlength FLOAT,
                    carwidth FLOAT,
                    carheight FLOAT,
                    curbweight FLOAT,
                    enginetype TEXT,
                    cylindernumber TEXT,
                    enginesize FLOAT,
                    fuelsystem TEXT,
                    boreratio FLOAT,
                    stroke FLOAT,
                    compressionratio FLOAT,
                    horsepower INTEGER,
                    peakrpm INTEGER,
                    city_L_100km FLOAT,
                    highway_L_100km FLOAT,
                    prediction INTEGER,
                    prix_reel INTEGER,
                    user_id INTEGER
                )
                ''')

curseur.execute("""
                CREATE TABLE IF NOT EXISTS user (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pseudo TEXT NOT NULL,
                    email TEXT NOT NULL,
                    mdp TEXT NOT NULL,
                    jwt TEXT
                )
                """)

connexion.commit()

connexion.close()