# -*- coding: utf-8 -*-
"""
Created on Tue Jul 22 15:49:46 2025

@author: luisf
"""

import streamlit as st
import pandas as pd
from utils import obtener_data, convertir_a_excel
from graficos import generar_grafico
from graficos import procesar_columna_encuesta_seleccion_simple
from graficos import procesar_columna_encuesta_seleccion_multiple
from graficos import procesar_columna_encuesta_texto


@st.cache_data
def fetch_and_clean_data(uploaded_file) -> pd.DataFrame:
    return obtener_data(uploaded_file)

# st.set_page_config(layout='wide')

uploaded_file = st.file_uploader("Choose a file")

if uploaded_file:
    
    df = fetch_and_clean_data(uploaded_file).reset_index()
    
    # st.dataframe(df)
    

    
    paises_options = list(df['country'].unique())
    selection = st.pills("Seleccione los Países", paises_options, selection_mode="multi")
    
    if len(selection)>0:
        statistics_df = df[df['country'].isin(selection)]
    else:
        statistics_df = df
        
    # Botón para descargar
    excel_bytes = convertir_a_excel(statistics_df)
        
    st.download_button(
        label="📥 Descargar Excel",
        data=excel_bytes,
        file_name="Informe.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    
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

    title = statistics_df.columns[13]
    data = procesar_columna_encuesta_seleccion_simple(list(statistics_df[title]))
    
    st.write(title)
    st.dataframe(data)    
    fig = generar_grafico(data, title)    
    st.pyplot(fig)
    
    
    title = statistics_df.columns[14]
    data = procesar_columna_encuesta_seleccion_simple(list(statistics_df[title]))    
    st.write(title)
    st.dataframe(data)
    fig = generar_grafico(data, title)
    st.pyplot(fig)
    
    title = statistics_df.columns[15]
    data =  procesar_columna_encuesta_seleccion_multiple(columna=list(statistics_df[title]), sep='   ')    
    st.write(title)
    st.dataframe(data)
    fig = generar_grafico(data, title)    
    st.pyplot(fig)
    
    title = statistics_df.columns[16]
    data =  procesar_columna_encuesta_seleccion_multiple(columna=list(statistics_df[title]), sep='   ')    
    st.write(title)
    st.dataframe(data)
    fig = generar_grafico(data, title)    
    st.pyplot(fig)
    
    title = statistics_df.columns[17]
    data = procesar_columna_encuesta_texto(columna=list(statistics_df[title]))
    st.markdown(body=f"# {title} \n {data}")
                                           
    
    
    

    
    


    
    
