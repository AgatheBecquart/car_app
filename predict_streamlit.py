import streamlit as st 
import pandas as pd 
import pickle

df = pd.read_csv('carprice_cleaned.csv')

## Ouvrir le modèle avec pickle
with open('trained_pipeline.pkl', 'rb') as f:
    model = pickle.load(f)

st.title("Estimation de la valeur d'une voiture : ")

st.write('Entrez les caractéristiques de la voiture pour obtenir une estimation de son prix.')

symboling = st.slider('Classement de sécurité (de -3 à 3)', min_value=int(df['symboling'].min()), max_value=int(df['symboling'].max()), value=int(df['symboling'].mean()), step=1)
CompanyName = st.selectbox('Nom de la compagnie', df['CompanyName'].unique())
filtered_df = df[df['CompanyName'] == CompanyName]
CarModel = st.selectbox('Modèle de voiture', filtered_df['CarModel'].unique())
fueltype = st.radio('Type de carburant', df['fueltype'].unique())
aspiration = st.radio('Aspiration', df['aspiration'].unique())
doornumber = st.radio('Nombre de portes', df['doornumber'].unique())
carbody = st.selectbox('Type de carrosserie', df['carbody'].unique())
drivewheel = st.selectbox('Type de transmission', df['drivewheel'].unique())
enginelocation = st.radio('Emplacement du moteur', ('front', 'rear'))
wheelbase = st.slider('Empattement', min_value=df['wheelbase'].min(), max_value=df['wheelbase'].max(), value=float(df['wheelbase'].mean()), step=0.1)
carlength = st.slider('Longueur de la voiture', min_value=df['carlength'].min(), max_value=df['carlength'].max(), value=float(df['carlength'].mean()), step=0.1)
carwidth = st.slider('Largeur de la voiture', min_value=df['carwidth'].min(), max_value=df['carwidth'].max(), value=float(df['carwidth'].mean()), step=0.1)
carheight = st.slider('Hauteur de la voiture', min_value=df['carheight'].min(), max_value=df['carheight'].max(), value=float(df['carheight'].mean()), step=0.1)
curbweight = st.slider('Poids à vide de la voiture', min_value=df['curbweight'].min(), max_value=df['curbweight'].max(), value=float(df['curbweight'].mean()), step=10.0)
enginetype = st.selectbox('Type de moteur', df['enginetype'].unique())
cylindernumber = st.selectbox('Nombre de cylindres', df['cylindernumber'].unique())
enginesize = st.slider('Taille du moteur', min_value=df['enginesize'].min(), max_value=df['enginesize'].max(), value=float(df['enginesize'].mean()), step=1.0)
fuelsystem = st.selectbox('Système de carburant', df['fuelsystem'].unique())
boreratio = st.slider('Rapport d\'alésage', min_value=df['boreratio'].min(), max_value=df['boreratio'].max(), value=float(df['boreratio'].mean()), step=0.1)
stroke = st.slider('Course du moteur', min_value=df['stroke'].min(), max_value=df['stroke'].max(), value=float(df['stroke'].mean()), step=0.0001)
compressionratio = st.slider('Taux de compression', min_value=df['compressionratio'].min(), max_value=df['compressionratio'].max(), value=float(df['compressionratio'].mean()), step=0.1)
horsepower = st.slider('Puissance du moteur', min_value=int(df['horsepower'].min()), max_value=int(df['horsepower'].max()), value=int(df['horsepower'].mean()), step=1)
peakrpm = st.slider('RPM de pointe', min_value=3000, max_value=7000, value=4500, step=100)
citympg = st.slider('Consommation en ville (MPG)', min_value=0.0, max_value=20.0, value=10.0, step=0.1)
highwaympg = st.slider("Consommation sur l'autoroute (MPG)", min_value=0.0, max_value=20.0, value=10.0, step=0.1)

feature_values = [symboling, CompanyName, CarModel, fueltype, aspiration, doornumber, carbody, drivewheel, enginelocation, wheelbase, carlength, carwidth, carheight, curbweight, enginetype, cylindernumber, enginesize, fuelsystem, boreratio, stroke, compressionratio, horsepower, peakrpm, citympg, highwaympg]

X = df.drop(['price', "car_ID", "CarName"], axis=1)
feature_names = X.columns.tolist()
X_pred = pd.DataFrame([feature_values], columns=feature_names)


# Prédire la qualité du vin
prediction = model.predict(X_pred)


if st.button('Valider'):
    st.write(f'La prix estimé pour cette voiture est {round(prediction[0])}.')