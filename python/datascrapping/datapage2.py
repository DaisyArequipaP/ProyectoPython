import requests
from bs4 import BeautifulSoup
import os


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, como Gecko) Chrome/91.0.4472.124 Safari/537.36'
}


url = 'https://ivannyboutique.com/'


response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')


productos = soup.find_all('div', class_='product-description')

# Función para convertir precio a float
def convertir_precio(precio_texto):
    # Eliminar el símbolo de dólar 
    precio_texto = precio_texto.replace('$', '').replace('\xa0', '').replace('.', '').replace(',', '.')
    try:
        return float(precio_texto)
    except ValueError:
        return "Precio no encontrado"

# Crear la carpeta dataextract si no existe
output_dir = os.path.join('dataanalyzing', 'dataextract')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

with open(os.path.join(output_dir, 'Ivannyboutique.txt'), 'w', encoding='utf-8') as file:

    for producto in productos:
        # Extraer el nombre del producto
        nombre_div = producto.find('div', class_='product_name')  
        if nombre_div:
            nombre = nombre_div.text.strip()
        else:
            nombre = "Nombre no encontrado"
        
        # Extraer el precio del producto
        precio_div = producto.find('span', class_='price') 
        if precio_div:
            precio = precio_div.text.strip()
            precio = convertir_precio(precio)
        else:
            precio = "Precio no encontrado"
        
        # Salida de datos
        file.write(f'Nombre del producto: {nombre}, Precio: {precio}\n')