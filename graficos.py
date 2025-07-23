# -*- coding: utf-8 -*-
"""
Created on Tue Jul 22 21:17:52 2025

@author: luisf
"""

import matplotlib.pyplot as plt
import pandas as pd


def generar_grafico(data: pd.DataFrame, title:str):
    # Simulación de tus datos
    data['Porcentaje'] = data['Conteo'] / data['Conteo'].sum() * 100

    # Orden invertido para que "Excelente" quede arriba como en tu gráfico
    data = data.iloc[::-1]

    # Gráfico
    fig, ax = plt.subplots(figsize=(8, 4))

    # Barras
    bars = ax.barh(data['Categoría'], data['Conteo'], color='gray')

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