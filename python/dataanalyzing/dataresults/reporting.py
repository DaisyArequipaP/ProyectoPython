import sys
import os

# Agregar el directorio 'dataanalyzing' al sys.path para que funcione mi busqueda en el directorio
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

from dataresults.decorators import manejar_excepciones, crear_directorio_si_no_existe, medir_tiempo


@medir_tiempo
@crear_directorio_si_no_existe
@manejar_excepciones
#Analisis de Mediana, media, moda, desviación estandar y Varianza
#Analisis con regresion lineal simple para validar si los datos estan dentro o fuera del promedio
def analisis_estadisticos_por_origen(df, output_dir):
    resultados = []
    comparaciones = {}

    for origen, grupo in df.groupby('Origen'):
        precios = grupo['Precio'].tolist()

        media = np.mean(precios)
        
        mediana = np.median(precios)
        
        desviacion_estandar = np.std(precios)
        
        varianza = np.var(precios)
        
        tiempo = np.arange(len(precios)).reshape(-1, 1)
        precios_np = np.array(precios).reshape(-1, 1)
        
        modelo = LinearRegression()
        modelo.fit(tiempo, precios_np)
        predicciones = modelo.predict(tiempo)
        
        plt.scatter(tiempo, precios_np, color='blue')
        plt.plot(tiempo, predicciones, color='red')
        plt.title(f'Regresión Lineal del Precio vs Tiempo ({origen})')
        plt.xlabel('Tiempo')
        plt.ylabel('Precio')
        
        # Guardar la gráfica como png
        grafico_path = os.path.join(output_dir, f'regresion_lineal_{origen}.png')
        plt.savefig(grafico_path)
        plt.close()
        
        resultados.append({
            'Origen': origen,
            'Media': media,
            'Mediana': mediana,
            'Desviación Estándar': desviacion_estandar,
            'Varianza': varianza
        })

        # Actualizar comparaciones
        comparaciones[origen] = {
            'Media': media,
            'Mediana': mediana,
            'Desviación Estándar': desviacion_estandar,
            'Varianza': varianza
        }
    
    resultados_df = pd.DataFrame(resultados)
    resultados_csv_path = os.path.join(output_dir, 'analisis_estadisticos_por_origen.csv')
    resultados_df.to_csv(resultados_csv_path, index=False)

    return comparaciones

@medir_tiempo
@crear_directorio_si_no_existe
@manejar_excepciones
def generar_reporte_comparativo(comparaciones, output_dir):
    if comparaciones is None or not comparaciones:
        print("No se encontraron comparaciones válidas.")
        return

    comparaciones_df = pd.DataFrame(columns=['Estadística', 'Cumple', 'No Cumple'])
    
    for estadistica in ['Media', 'Mediana', 'Desviación Estándar', 'Varianza']:
        if comparaciones['datapage1'][estadistica] < comparaciones['datapage2'][estadistica]:
            cumple = f'datapage1 ({comparaciones["datapage1"][estadistica]})'
            no_cumple = f'datapage2 ({comparaciones["datapage2"][estadistica]})'
        else:
            cumple = f'datapage2 ({comparaciones["datapage2"][estadistica]})'
            no_cumple = f'datapage1 ({comparaciones["datapage1"][estadistica]})'
        
        comparaciones_df = pd.concat([comparaciones_df, pd.DataFrame({
            'Estadística': [estadistica],
            'Cumple': [cumple],
            'No Cumple': [no_cumple]
        })], ignore_index=True)
    
    comparaciones_csv_path = os.path.join(output_dir, 'reporte_comparativo.csv')
    comparaciones_df.to_csv(comparaciones_csv_path, index=False)

# Función para ejecutar el análisis
@medir_tiempo
@manejar_excepciones
def main():
    # CSV generado solo del producto vestidos o vestido
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'dataload', 'datos_consolidados.csv')

    df_final = pd.read_csv(csv_path)

    df_final = df_final[df_final['Producto'].str.contains('vestido', case=False, na=False)]

    output_dir = os.path.join(os.path.dirname(__file__), '..', 'dataresults')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    comparaciones = analisis_estadisticos_por_origen(df_final, output_dir)

    # Reporte comparativo
    generar_reporte_comparativo(comparaciones, output_dir)

if __name__ == "__main__":
    main()
