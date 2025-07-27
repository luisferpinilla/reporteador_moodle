# -*- coding: utf-8 -*-
"""
Created on Tue Jul 22 21:17:52 2025

@author: luisf
"""

import matplotlib.pyplot as plt
import pandas as pd


def procesar_columna_encuesta_seleccion_simple(columna:list) -> pd.DataFrame:
    
    clean_columna = [x  for x in columna if type(x)== str]
    
    clean_columna = set(clean_columna) 
    
    # Obtener las categorias
    categorias = {x:0 for x in clean_columna}
        
    # Recorrer los registros
    for row in columna:
        if type(row)== str:
            categorias[row] +=1
            
    
    data = pd.DataFrame({"Categoria":k, "Conteo":v} for k,v in categorias.items())             

    return data


def procesar_columna_encuesta_seleccion_multiple(columna:list, sep:str) -> pd.DataFrame:
    
    categorias = dict()
        
            
    for row in columna:
        for categoria in row.split('   '):
            if categoria in categorias.keys():
                categorias[categoria] += 1
            else:
                categorias[categoria] = 1
            
    data = pd.DataFrame({"Categoria":k, "Conteo":v} for k,v in categorias.items())             

    return data


def procesar_columna_encuesta_texto(columna:list)-> str:    
   
    clean_columna = [f"- {str(x).strip()}"  for x in columna if type(x)== str]
    
    return "\n\n".join(clean_columna)


def generar_grafico(data: pd.DataFrame, title:str):
    # Simulación de tus datos
    data['Porcentaje'] = data['Conteo'] / data['Conteo'].sum() * 100

    # Orden invertido para que "Excelente" quede arriba como en tu gráfico
    data = data.iloc[::-1]

    # Gráfico
    fig, ax = plt.subplots(figsize=(8, 4))

    # Barras
    bars = ax.barh(data['Categoria'], data['Conteo'], color='gray')

    # Etiquetas circulares con número y porcentaje
    for bar, count, pct in zip(bars, data['Conteo'], data['Porcentaje']):
        if count > 0:
            ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height() / 2,
                    f"{int(count)}\n{pct:.1f}%",
                    va='center', ha='center',
                    bbox=dict(boxstyle="circle,pad=0.5",
                              fc='#1f4e79', ec='none'),
                    color='white', fontsize=10, fontweight='bold')

    # Estilo limpio
    ax.set_facecolor('#f2f2f2')
    fig.patch.set_facecolor('#f2f2f2')
    ax.tick_params(left=False, bottom=False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.set_xticks([])

    # Título
    ax.set_title(title, loc='left', fontsize=11)

    plt.tight_layout()
    
    return fig