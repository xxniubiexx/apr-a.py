# Programa: apr-py
# Autor: NooBDll
# Descripción: Este programa realiza una exploración de una red especificada en notación CIDR,
# realizando un ping a cada dirección IP en el rango y luego consultando la tabla ARP para obtener
# la dirección MAC y el tipo de dispositivo correspondiente. Si el ping es exitoso, se registra el 
# nombre del host, la dirección MAC y el tipo de dispositivo en un archivo de Excel.
# Licencia: MIT License
# Copyright (c) 2023 NooBDll
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ----------------------------------------------------------
import pandas as pd
import subprocess
import time  # importar el módulo time para usar sleep
import ipaddress  # importar el módulo ipaddress para manejar direcciones IP y rangos CIDR
import socket  # importar el módulo socket para obtener el nombre de host
from tqdm import tqdm  # importar la barra de progreso tqdm

# Pedir al usuario que ingrese un rango de direcciones IP en notación CIDR
cidr_range = input("Por favor, introduce un rango de direcciones IP en notación CIDR (por ejemplo, 192.168.0.0/24): ")

# Generar una lista de direcciones IP a partir del rango CIDR
ips = ipaddress.ip_network(cidr_range)
ip_list = [str(ip) for ip in ips]

# Listas para almacenar los resultados del comando arp
successful_ips = []
mac_results = []
type_results = []
hostnames = []

# Hacer ping y ejecutar arp para cada IP
for ip in tqdm(ip_list, desc="Procesando IPs", unit="IP"):
    try:
        subprocess.run(['ping', '-n', '1', '-w', '500', ip], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        time.sleep(2)  # esperar 2 segundos

        result = subprocess.run(['arp', '-a', ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)

        # Parsear la salida del comando arp y buscar la IP
        mac = ''
        type_ = ''
        hostname = ''
        lines = result.stdout.splitlines()
        for line in lines:
            parts = line.split()
            if len(parts) >= 3 and parts[0].strip() == ip:
                mac = parts[1]
                type_ = parts[2]
                try:
                    hostname = socket.getfqdn(ip)
                except Exception:
                    hostname = 'Error al obtener el nombre del host'
                break
        if mac == '' or type_ == '' or hostname == '':
            print(f"Datos incompletos para {ip}: MAC = {mac}, Tipo = {type_}, Nombre del host = {hostname}")

        # Agregar la IP a la lista de IPs exitosas y sus correspondientes resultados a las listas
        successful_ips.append(ip)
        hostnames.append(hostname)
        mac_results.append(mac)
        type_results.append(type_)
    except subprocess.CalledProcessError:
        print(f"Error al procesar {ip}")
        continue  # continuar con la siguiente IP sin agregar nada a las listas de resultados

# Crear un DataFrame a partir de la lista de IPs exitosas
df = pd.DataFrame({
    'Direcciones': successful_ips,
    'Nombre del host': hostnames,
    'Dirección física': mac_results,
    'Tipo': type_results
})

# Escribir el DataFrame a un nuevo archivo de Excel
df.to_excel('resultado.xlsx', index=False)
