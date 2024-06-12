import pandas as pd
import os

def transformar_a_dataframe(archivo_scraping, origen):
    productos = []
    precios = []

    with open(archivo_scraping, 'r', encoding='utf-8') as file:
        for line in file:
            if "Nombre del producto:" in line:
                nombre = line.split('Nombre del producto:')[1].split(', Precio:')[0].strip()
                precio = line.split('Precio:')[1].strip()
                try:
                    precio = float(precio)
                except ValueError:
                    precio = None
                productos.append(nombre)
                precios.append(precio)

    df = pd.DataFrame({
        'Producto': productos,
        'Precio': precios,
        'Origen': [origen] * len(productos)
    })
    
    return df

# Guardar DataFrame en un archivo CSV
def guardar_dataframe(df, nombre_archivo):
    df.to_csv(nombre_archivo, index=False)

# Función para ñimpiar mi archivo de lo que tenga "Nombre no encontrado"
def eliminar_nombres_no_encontrados(df):
    df = df[df['Producto'] != 'Nombre no encontrado']
    return df

# Función para homologar mis datos
def formatear_datos(df):
    df['Producto'] = df['Producto'].str.lower()
    df['Precio'] = df['Precio'].apply(lambda x: round(x, 2) if isinstance(x, float) else x)
    return df

# Directorio base (directorio del archivo actual)
base_dir = os.path.dirname(os.path.abspath(__file__))
archivo_scraping1 = os.path.join(base_dir, '..', 'dataextract', 'Spiritmoda.txt') 
archivo_scraping2 = os.path.join(base_dir, '..', 'dataextract', 'Ivannyboutique.txt')  

df1 = transformar_a_dataframe(archivo_scraping1, 'datapage1')
df2 = transformar_a_dataframe(archivo_scraping2, 'datapage2')

# Concatenar los dos datos diferenciandolos por su origen: datapage1 o datapage2
df_final = pd.concat([df1, df2], ignore_index=True)

# Validacion que no hayan nombres no encontrados
df_final = eliminar_nombres_no_encontrados(df_final)

# Validacion de homologacion de datos
df_final = formatear_datos(df_final)

# Crear la carpeta dataload si no existe
output_dir = os.path.join(base_dir, '..', 'dataload')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Guardar el DataFrame final en un archivo CSV
guardar_dataframe(df_final, os.path.join(output_dir, 'datos_consolidados.csv'))
