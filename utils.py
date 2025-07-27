# -*- coding: utf-8 -*-
"""
Created on Tue Jul 22 18:43:47 2025

@author: luisf
"""

import zipfile
import pandas as pd
from io import BytesIO

def obtener_archivos(file:str)->list:

    with zipfile.ZipFile(file, 'r') as zip_ref:
        archivos = [f for f in zip_ref.namelist() if not f.endswith('/')]
    
    return archivos


def obtener_excel_desde_zip(ruta_zip:str, nombre_archivo:str)->pd.DataFrame:
    
    with zipfile.ZipFile(ruta_zip, 'r') as zip_ref:
        with zip_ref.open(nombre_archivo) as archivo_excel:
            df = pd.read_excel(archivo_excel)
    
    return df
    
    
# ruta_zip = "C:\\Users\\luisf\\Downloads\\datos-informes-paises.zip"

def obtener_usuarios_sin_ingreso(ruta_zip:str)->list:
    
    # Buscar todos los archivos que aplican
    ruta = 'datos-informes-paises/usuarios-sin-ingreso/'
    archivos = [x for x in obtener_archivos(ruta_zip) if str(x).startswith(ruta)]
    
    # Obtener los dataframe de cada archivo
    datos = list()
    
    with zipfile.ZipFile(ruta_zip, 'r') as zip_ref:
        for nombre_archivo in archivos:
            with zip_ref.open(nombre_archivo) as archivo_excel:
                df = pd.read_excel(archivo_excel)
                datos.append(df)

    df = pd.concat(datos) 
    
    df = df.drop_duplicates()
    
    return df
    
    
def obtener_encuestas_usuario(ruta_zip:str)->pd.DataFrame:
    # Buscar todos los archivos que aplican
    ruta = 'datos-informes-paises/encuesta/'
    archivos = [x for x in obtener_archivos(ruta_zip) if str(x).startswith(ruta)]

    # Obtener los dataframe de cada archivo
    datos = list()
    
    with zipfile.ZipFile(ruta_zip, 'r') as zip_ref:
        for nombre_archivo in archivos:
            with zip_ref.open(nombre_archivo) as archivo_excel:
                df = pd.read_excel(archivo_excel)
                datos.append(df)

    df = pd.concat(datos) 
    
    df.drop(columns=['Nombre completo del usuario', 'Grupos', 'Fecha'], inplace=True)
    
    df.rename(columns={"Dirección de correo":"email"}, inplace=True)

    return df


def estatus_aprobacion(conteoIntentos:int, calificacion_max:int,  maxConteo=3, umbral_aprobacion=7)->bool:
    
    if calificacion_max >= umbral_aprobacion:
        return True
    
    if conteoIntentos >=maxConteo:
        return False
    
    return None



def obtener_evaluaciones(ruta_zip:str)->pd.DataFrame:
    # Buscar todos los archivos que aplican
    ruta = 'datos-informes-paises/evaluaciones/'
    archivos = [x for x in obtener_archivos(ruta_zip) if str(x).startswith(ruta)]
    
    # Obtener los dataframe de cada archivo
    datos = list()
    
    with zipfile.ZipFile(ruta_zip, 'r') as zip_ref:
        for nombre_archivo in archivos:
            with zip_ref.open(nombre_archivo) as archivo_excel:
                df = pd.read_excel(archivo_excel)
                datos.append(df)

    df = pd.concat(datos) 
    
    df.rename(columns={'Dirección de correo': 'email', 'Calificación/10,00': 'Calificación'}, inplace=True)
    
    df = df[['email', 'Calificación']].copy()
    
    df = df[df['Calificación']!='-'].copy()
    
    df['Calificación'] = df['Calificación'].apply(lambda x: float(str(x).replace(",", ".")))
    
    df = df.groupby('email').agg({'Calificación': ['count', 'max']})
    
    df.columns = ['_'.join(col) for col in df.columns]
    
    # Convertir en tabla no indexada
    df.reset_index(inplace=True)
    
    df['EvaluacionSuperada'] = df['Calificación_max'].apply(lambda x: estatus_aprobacion(conteoIntentos=x['Calificación_count'], 
                                                                                         calificacion_max=x['Calificación_max']))
    
    return df


def obtener_progreso(ruta_zip:str)->pd.DataFrame:
    # Buscar todos los archivos que aplican
    ruta = 'datos-informes-paises/actividades/'
    archivos = [x for x in obtener_archivos(ruta_zip) if str(x).startswith(ruta)]
    
    # Obtener los dataframe de cada archivo
    datos = list()
    
    renamer = {'Unnamed: 0': 'Unnamed: 0',
     'Dirección de correo': 'email',
     'Video Sesión 1': 'Video Sesión 1',
     'Unnamed: 3': 'Unnamed: 3',
     'Video Sesión 2 (Panamá)': 'Video Sesión 2',
     'Unnamed: 5': 'Unnamed: 5',
     'Video Sesión 3 (Panamá)': 'Video Sesión 3',
     'Unnamed: 7': 'Unnamed: 7',
     'Evaluación (Panamá)': 'Evaluación',
     'Unnamed: 9': 'Unnamed: 9',
     'Video Sesión 2 (Ecuador)': 'Video Sesión 2',
     'Video Sesión 3 (Ecuador)': 'Video Sesión 3',
     'Evaluación (Ecuador)': 'Evaluación',
     'Video Sesión 2 (Honduras)': 'Video Sesión 2',
     'Video Sesión 3 (Honduras)': 'Video Sesión 3',
     'Evaluación (Honduras)': 'Evaluación',
     'Video Sesión 2 (El Salvador)': 'Video Sesión 2',
     'Video Sesión 3 (El Salvador)': 'Video Sesión 3',
     'Evaluación (El Salvador)': 'Evaluación',
     'Video Sesión 2 (República Dominicana)': 'Video Sesión 2',
     'Video Sesión 3 (República Dominicana)': 'Video Sesión 3',
     'Evaluación (República Dominicana)': 'Evaluación',
     'Video Sesión 2 (Guatemala)': 'Video Sesión 2',
     'Video Sesión 3 (Guatemala)': 'Video Sesión 3',
     'Evaluación (Guatemala)': 'Evaluación',
     'Video Sesión 2 (Costa Rica)': 'Video Sesión 2',
     'Video Sesión 3 (Costa Rica)': 'Video Sesión 3',
     'Evaluación (Costa Rica)': 'Evaluación',
     'Video Sesión 2 (Nicaragua)': 'Video Sesión 2',
     'Video Sesión 3 (Nicaragua)': 'Video Sesión 3',
     'Evaluación (Nicaragua)': 'Evaluación'}
    
    with zipfile.ZipFile(ruta_zip, 'r') as zip_ref:
        for nombre_archivo in archivos:
            with zip_ref.open(nombre_archivo) as archivo_excel:
                df = pd.read_csv(archivo_excel, sep='\t', encoding='utf-16-le')
                df = df.rename(columns=renamer)
                datos.append(df)

    df = pd.concat(datos) 
    
    df.drop(columns=[x for x in df.columns if str(x).startswith("Unnamed")], inplace=True)
    
    # Seleccionar solo las filas relevantes
    df = df[['email', 'Video Sesión 1', 'Video Sesión 2', 'Video Sesión 3', 'Evaluación']]

    df.rename(columns={
        'Dirección de correo': 'email',
        'Video Sesión 1': 'Video1',
        'Video Sesión 2': 'Video2',
        'Video Sesión 3': 'Video3',
        'Evaluación (Panamá)': 'Evaluación'}, inplace=True)
    
    return df

def obtener_data(ruta_zip:str)->pd.DataFrame:
    users_path = 'datos-informes-paises/usuarios-totales/usuarios-totales-front-office.xlsx'
    teste_users_path = 'datos-informes-paises/usuarios-prueba/usuarios-prueba.xlsx'
    
    users_df = obtener_excel_desde_zip(ruta_zip, users_path)
    test_df = obtener_excel_desde_zip(ruta_zip, teste_users_path)
    sin_ingreso_df = obtener_usuarios_sin_ingreso(ruta_zip=ruta_zip)
    encuesta_df = obtener_encuestas_usuario(ruta_zip=ruta_zip)
    evaluaciones_df = obtener_evaluaciones(ruta_zip=ruta_zip)
    progreso_df = obtener_progreso(ruta_zip=ruta_zip)
    
    # Remover usuarios de prueba
    users_df = users_df[~users_df['email'].isin(test_df['email'])].copy()
    
    # Agregar columna de sin ingreso
    users_df['sin_ingreso'] =  users_df['email'].isin(sin_ingreso_df['email'])
    
    # Agregar columnas de encuesta
    users_df = pd.merge(left=users_df, left_on='email', right=encuesta_df, right_on='email', how='left')
    
    # Agregar columnas de evaluaciones
    users_df = pd.merge(left=users_df, left_on='email', right=evaluaciones_df, right_on='email', how='left')
    
    # Agregar informe de progreso
    users_df = pd.merge(left=users_df, left_on='email', right=progreso_df, right_on='email', how='left')
    
    # Mayúsculas en city
    users_df['city'] = users_df['city'].apply(lambda x: str(x).upper())
    
    # convertir email en index
    users_df.set_index('email', inplace=True)
   
    
    return users_df


def convertir_a_excel(df):
    output = BytesIO()
    
    usuarios_registrados_df = df[['username', 'firstname', 'lastname', 'email', 'country']].copy()
    
    evaluacion_superada_df = df[['username', 'firstname', 'lastname', 'email', 'country', 'EvaluacionSuperada']].copy()
    
    evaluacion_superada_df = evaluacion_superada_df[evaluacion_superada_df['EvaluacionSuperada']==True]
    
    evaluacion_no_superada_df = evaluacion_superada_df[evaluacion_superada_df['EvaluacionSuperada']==False]
    
    videos_df = df[['username', 'firstname', 'lastname', 'email', 'country', 'Video1', 'Video2', 'Video3']].copy()

    usuarios_sin_ingreso = df[['username', 'firstname', 'lastname', 'email', 'country', 'sin_ingreso']].copy()
    usuarios_sin_ingreso = usuarios_sin_ingreso[usuarios_sin_ingreso['sin_ingreso']==True].drop(columns=['sin_ingreso'])
    
    # capacidation_no_finalizada_df = df.copy()
    
    calificaciones_df = df[['username', 'firstname', 'lastname', 'email', 'country', 'Calificación_max']].copy()
    calificaciones_df = calificaciones_df[~calificaciones_df['Calificación_max'].isna()].rename(columns={'Calificación_max':'Calificación'}) 
    
    
    with pd.ExcelWriter(output) as writer:
        usuarios_registrados_df.to_excel(writer, sheet_name='Usuarios Registrados', index=False)
        evaluacion_superada_df.to_excel(writer, sheet_name='Evaluación Superada', index=False)
        evaluacion_no_superada_df.to_excel(writer, sheet_name='Evaluación No Superada', index=False)
        videos_df.to_excel(writer, sheet_name='Videos', index=False)
        usuarios_sin_ingreso.to_excel(writer, sheet_name='Usuarios Sin Ingreso', index=False)
        calificaciones_df.to_excel(writer, sheet_name='Calificaciones', index=False)
        
    output.seek(0)
    
    return output
    
 