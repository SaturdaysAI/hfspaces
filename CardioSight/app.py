import gradio as gr
import pandas as pd
from joblib import load

def cardio(age,gender,ap_hi,ap_lo,cholesterol,gluc,smoke,alco,active,height,weight):
    model = load('cardiosight.joblib')
    df = pd.DataFrame.from_dict(
        {
            "age": [age*365],
            "gender":[0 if gender=='Male' else 1],
            "ap_hi": [ap_hi],
            "ap_lo": [ap_lo],
            "cholesterol": [cholesterol + 1],
            "gluc": [gluc + 1],
            "smoke":[1 if smoke=='Yes' else 0],
            "alco": [1 if alco=='Yes' else 0],
            "active": [1 if active=='Yes' else 0],
            "newvalues_height": [height],
            "newvalues_weight": [weight],
            "New_values_BMI": weight/((height/100)**2),
            
        }
    )
       
    pred = model.predict(df)[0]
    if pred==1:
      predicted="Tiene un riesgo alto de sufrir problemas cardiovasculares"
    else:
      predicted="Su riesgo de sufrir problemas cardiovasculares es muy bajo. Siga así."
    return "Su IMC es de "+str(round(df['New_values_BMI'][0], 2))+'. '+predicted
    
iface = gr.Interface(
    cardio,
    [
        gr.Slider(1,99,label="Age"),
        gr.Dropdown(choices=['Male', 'Female'], label='Gender', value='Female'),
        gr.Slider(10,250,label="Diastolic Preassure"),
        gr.Slider(10,250,label="Sistolic Preassure"),
        gr.Radio(["Normal","High","Very High"],type="index",label="Cholesterol"),
        gr.Radio(["Normal","High","Very High"],type="index",label="Glucosa Level"),
        gr.Dropdown(choices=['Yes', 'No'], label='Smoke', value='No'),
        gr.Dropdown(choices=['Yes', 'No'], label='Alcohol', value='No'),
        gr.Dropdown(choices=['Yes', 'No'], label='Active', value='Yes'),
        gr.Slider(30,220,label="Height in cm"),
        gr.Slider(10,300,label="Weight in Kg"),
    ],

    "text",
    examples=[
        [20,'Male',110,60,"Normal","Normal",'No','No','Yes',168,60],
        [30,'Female',120,70,"High","High",'No','Yes','Yes',143,70],
        [40,'Male',130,80,"Very High","Very High",'Yes','Yes','No',185,80],
        [50,'Female',140,90,"Normal","High",'Yes','No','No',165,90],
        [60,'Male',150,100,"High","Very High",'No','No','Yes',175,100],
        [70,'Female',160,90,"Very High","Normal",'Yes','Yes','No',185,110],
    ],
    title = 'Calculadora de Riesgo Cardiovascular mediante Inteligencia Artificial',
    description = 'Duplicación del proyecto de CARDIOSIGHT. He cambiado los botones tipo check por dropdown y calculado el IMC a partir de la altura y el peso. Más información: https://saturdays.ai/2022/03/16/cardiosight-machine-learning-para-calcular-riesgo-cardiovascular/'
)

iface.launch()