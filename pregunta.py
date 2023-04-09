"""
Ingestión de datos - Reporte de clusteres
-----------------------------------------------------------------------------------------

Construya un dataframe de Pandas a partir del archivo 'clusters_report.txt', teniendo en
cuenta que los nombres de las columnas deben ser en minusculas, reemplazando los espacios
por guiones bajos; y que las palabras clave deben estar separadas por coma y con un solo 
espacio entre palabra y palabra.


"""
import pandas as pd
import re

def ingest_data():

    # Se abre el archivo y se toman las dos primeras filas para crear el encabezado en una lista
    file = "clusters_report.txt"
    archivo = []
    txt = []

    texto = open(file, mode='r')
    archivo.append(texto.readline())
    archivo.append(texto.readline())

    # Separamos cada linea como una lista de ancho fijo y se reemplazan los valores de cr1
    for idx, i in enumerate(archivo):
        archivo[idx] = ([i[:9], i[9:25].replace("\n",''), i[25:41].replace("\n",''), i[41:].replace("\n",'')])

    #Se juntan las filas 0 y 1 para formar encabezado compuesto
    archivo[0] = list(zip(archivo[0], archivo[1]))

    #Se elimina la fila 1 que ya se junto con la 0
    archivo.pop(1)

    #Se juntan las tuplas de cada columna como cadena de texto para titulo de columna. Se limpian espacios en blanco múltiples con split() y join reemplazandolos por '_'. Se hace lowercase
    for idx, x in enumerate(archivo[0]):
        archivo[0][idx] = '_'.join(''.join(x).split()).lower()

    #Se leen 2 líneas 'sobrantes'
    texto.readline()
    texto.readline()

    #Se lee y se cierra el resto del archivo
    cra = texto.read()
    texto.close()

    #Se reemplazan multiples espacios en blanco por uno solo
    cra = ' '.join(''.join(cra).split())

    #Separa el texto en elementos de lista, partiendo por el caracter '.'
    cra = cra.split('.')

    #Se elimina la última fila que es sobrante
    cra.pop()

    #Se crean variables para solventar problema de filas 6 y 7 que no se separan por no tener punto al final del 6
    aux1 = []
    aux2 = []

    aux1 = re.split('([o][l][ ])+',cra[5])[0] + re.split('([o][l][ ])+',cra[5])[1]
    aux2 = re.split('([o][l][ ])+',cra[5])[2]

    cra[5] = aux1
    cra.insert(6, aux2)

    #Se llena la lista con listas de cada fila del archivo, partidas por el caracter '%'
    for i in cra:
        txt.append(i.split('%')[0].replace(',','.').split()+[i.split('%')[1].strip()])

    #Se crea el DataFrame a partir de la lista de listas y con nombres de columnas
    df = pd.DataFrame(txt)
    df.columns = archivo[0]
    df['cluster'] = pd.to_numeric(df['cluster'])
    df['cantidad_de_palabras_clave'] = pd.to_numeric(df['cantidad_de_palabras_clave'])
    df['porcentaje_de_palabras_clave'] = pd.to_numeric(df['porcentaje_de_palabras_clave'])

    return df
