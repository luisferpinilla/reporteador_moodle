# -*- coding: utf-8 -*-
"""
Created on Tue Jul 22 15:49:46 2025

@author: luisf
"""

import streamlit as st
import pandas as pd

from utils import obtener_data
from graficos import generar_grafico
from io import BytesIO



def procesar_encuesta_1(encuesta_df:pd.DataFrame)->None:
    
    titulo = encuesta_df.columns[12]
    
    pregunta_1_df = encuesta_df.groupby([titulo])[['email']].count()
    
    categorias = ["Excelente", "Bueno", "Regular", "Deficiente"]
    
    conteos = [int(pregunta_1_df.loc[x]["email"]) if x in pregunta_1_df.index else 0 for x in categorias ]
    
    data = pd.DataFrame({'Categoría':categorias, 'Conteo': conteos})
    
    return titulo, data

def procesar_encuesta_2(file:str)->None:
    
    encuesta_df = pd.read_excel(file)
    
    pregunta_1_df = encuesta_df.groupby(['(2) La metodología y la herramienta utilizada para presentar el contenido de la capacitación fue:'])[['Dirección de correo']].count()
    
    categorias = ["Excelente", "Bueno", "Regular", "Malo"]
    
    conteos = [int(pregunta_1_df.loc[x]["Dirección de correo"]) if x in pregunta_1_df.index else 0 for x in categorias ]
    
    data = pd.DataFrame({'Categoría':categorias, 'Conteo': conteos})
    
    return data


def procesar_encuesta_generica_multiple(df:pd.DataFrame, columna_id:int):
    
    encuesta_df = df.copy()
    
    columna = encuesta_df.columns[columna_id]
        
    print(columna)
    
    # Obtener las categorias
    categorias = {z:0 for z in set([y for x in list(encuesta_df[columna]) for y in x.split('   ')])}
        
    # Recorrer los registros
    for row in list(encuesta_df[columna]):
        valores = row.split('   ')
        for valor in valores:
            categorias[valor] +=1
            
    
    data = pd.DataFrame({"Categoría":k, "Conteo":v} for k,v in categorias.items())             

    return columna, data


def convertir_a_excel(df):
    output = BytesIO()
    
    usuarios_registrados_df = df[['username', 'firstname', 'lastname', 'email', 'country']].copy()
    
    evaluacion_superada_df = df[['username', 'firstname', 'lastname', 'email', 'country', 'EvaluacionSuperada']].copy()
    
    evaluacion_superada_df = evaluacion_superada_df[evaluacion_superada_df['EvaluacionSuperada']==True]
    
    evaluacion_no_superada_df = evaluacion_superada_df[evaluacion_superada_df['EvaluacionSuperada']==False]
    
    videos_df = df[['username', 'firstname', 'lastname', 'email', 'country', 'Video1', 'Video2', 'Video3']].copy()

    usuarios_sin_ingreso = df[['username', 'firstname', 'lastname', 'email', 'country']].copy()
    usuarios_sin_ingreso = usuarios_sin_ingreso[usuarios_sin_ingreso['sin_ingreso']==True]
    
    calificaciones_df = df[['username', 'firstname', 'lastname', 'email', 'country', 'Calificaicon_max']].copy()
    
    
    with pd.ExcelWriter(output) as writer:
        usuarios_registrados_df.to_excel(writer, sheet_name='Usuarios Registrados', index=False)
        evaluacion_superada_df.to_excel(writer, sheet_name='Evaluación Superada', index=False)
        evaluacion_no_superada_df.to_excel(writer, sheet_name='Evaluación N Superada', index=False)
        videos_df.to_excel(writer, sheet_name='Videos', index=False)
        usuarios_sin_ingreso.to_excel(writer, sheet_name='USuarios Sin Ingreso', index=False)
        calificaciones_df.to_excel(writer, sheet_name='Calificaciones', index=False)
        
    output.seek(0)
    return output

@st.cache_data
def fetch_and_clean_data(uploaded_file) -> pd.DataFrame:
    return obtener_data(uploaded_file)

# st.set_page_config(layout='wide')

uploaded_file = st.file_uploader("Choose a file")

if uploaded_file:
    
    df = fetch_and_clean_data(uploaded_file).reset_index()
    
    st.dataframe(df)
    
    # Botón para descargar
    excel_bytes = convertir_a_excel(df)
    
    st.download_button(
        label="📥 Descargar Excel",
        data=excel_bytes,
        file_name="Informe.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    
    
    
    paises_options = list(df['country'].unique())
    selection = st.pills("Países", paises_options, selection_mode="multi")
    
    if len(selection)>0:
        statistics_df = df[df['country'].isin(selection)]
    else:
        statistics_df = df
    
    st.title(body="Aprobación")    
    columns_metric_1,columns_metric_2, columns_metric_3 = st.columns(3, border=True)
        
    
    with columns_metric_1:    
        st.metric(label='Usuarios Registrados', value=statistics_df.shape[0])
        
    with columns_metric_2:
        data = statistics_df[~statistics_df['EvaluacionSuperada'].isna()].copy()
        data = data[data['EvaluacionSuperada']==True].shape[0]
        
        st.metric(label ='Evaluación Superada', value = data)
    
    with columns_metric_3:
        data = statistics_df[~statistics_df['EvaluacionSuperada'].isna()].copy()
        data = data[data['EvaluacionSuperada']==False].shape[0]
        
        st.metric(label ='Evaluación NO Superada', value = data)
    
    st.title(body="Videos")
    
    columns_metric_1,columns_metric_2, columns_metric_3 = st.columns(3, border=True)
    
    with columns_metric_1:    
        data = statistics_df[statistics_df['Video1']=='Finalizado'].shape[0]        
        st.metric(label ='Video 1', value = data)
        
    with columns_metric_2:
        data = statistics_df[statistics_df['Video2']=='Finalizado'].shape[0]        
        st.metric(label ='Video 2', value = data)
    
    with columns_metric_3:
        data = statistics_df[statistics_df['Video3']=='Finalizado'].shape[0]        
        st.metric(label ='Video 3', value = data)
        
    st.title(body="Otros")
    
    columns_metric_1,columns_metric_2 = st.columns(2, border=True)
    
    with columns_metric_1:    
        data = statistics_df[statistics_df['sin_ingreso']==True].shape[0]        
        st.metric(label ='Usuarios sin Ingreso', value = data)
        
    with columns_metric_2:
        data = statistics_df[statistics_df['Evaluación']!='No finalizado'].shape[0]        
        st.metric(label ='Capacitación No Finalizada', value = data)
        
    st.title(body="Encuesta")

    # st.write({x:df.columns[x] for x in range(len(df.columns))})    

    title, data = procesar_encuesta_1(df.reset_index())
    
    st.write(title)
    st.dataframe(data)
    
    fig = generar_grafico(data, title)
    
    st.pyplot(fig)
    

    
    


    
    
