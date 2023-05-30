# apr-a.py network scanner


Este programa explora una red utilizando las direcciones IP proporcionadas por el usuario en la notación CIDR. Para cada dirección IP en el rango proporcionado, el programa realiza lo siguiente:

Ejecuta un comando ping para verificar la conectividad con esa dirección IP.
Si el ping es exitoso, ejecuta el comando arp -a para obtener información de la tabla ARP que contiene la dirección MAC y el tipo de dispositivo correspondiente a la dirección IP.
Además, se utiliza el método socket.getfqdn() para obtener el nombre de host asociado con la dirección IP.
Todo esto se hace en un ciclo for, y por cada dirección IP exitosa, la información se agrega a las listas correspondientes.
Al final, todas estas listas se combinan en un DataFrame de pandas que luego se escribe en un archivo de Excel.
El programa también utiliza la biblioteca tqdm para mostrar una barra de progreso mientras se procesan las direcciones IP.



This program explores a network using the IP addresses provided by the user in CIDR notation. For each IP address in the given range, the program does the following:

It runs a ping command to check the connectivity with that IP address.
If the ping is successful, it runs the arp -a command to get information from the ARP table that contains the MAC address and the type of device corresponding to the IP address.
In addition, it uses the socket.getfqdn() method to get the hostname associated with the IP address.
All of this is done in a for loop, and for each successful IP address, the information is added to the corresponding lists.
At the end, all these lists are combined into a pandas DataFrame which is then written to an Excel file.
The program also uses the tqdm library to display a progress bar while the IP addresses are being processed.
