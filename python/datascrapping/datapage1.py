import requests
from bs4 import BeautifulSoup
import os

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, como Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

url = 'https://spiritmodaec.sumerlabs.com/'

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

productos = soup.find_all('a', class_='_productCard3Wrapper_pz21j_1')
output_dir = os.path.join('dataanalyzing', 'dataextract')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Abrir un archivo para escribir los resultados
with open(os.path.join(output_dir, 'Spiritmoda.txt'), 'w', encoding='utf-8') as file:
    for producto in productos:
        # Extraer el nombre del producto
        nombre_div = producto.find('div', class_='_name_pz21j_21')
        if nombre_div:
            nombre = nombre_div.text.strip()
        else:
            nombre = "Nombre no encontrado"
        
        # Extraer el precio del producto y  Convertir el precio a float para análisis numérico
        precio_div = producto.find('div', class_='_value_pz21j_24')
        if precio_div:
            precio = precio_div.text.strip().replace('$', '')
            
            try:
                precio = float(precio)
            except ValueError:
                precio = "Precio no encontrado"
        else:
            precio = "Precio no encontrado"
        
        # Salida de datos
        file.write(f'Nombre del producto: {nombre}, Precio: {precio}\n')