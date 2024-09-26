import os
from datetime import datetime
import json
import sys
from shutil import rmtree


"""
Weslin Barahona
"""

#Obtencion del directorio actual donde se encuentra ejecutando el archivos
#Directorio de archivos a escanear
actual_Path = os.getcwd()
base_Path = sys.argv[1]
#Directorio de archivo fileTypes.json
files_Types_File = "./fileType.json"
try:
    if type(sys.argv[2]) == str:
        files_Types_File = sys.argv[2]
        print(files_Types_File)
except Exception as e:
    print(e)
    
#Proceso para leer un archivo json, parsearlo a dicccionario
json_Data_File = open(files_Types_File,'r') 
data = json.load(json_Data_File)
json_Data_File.close()
#Asignacion de la data a variable
extensiones_comunes = data["extensiones_comunes"]

def add_file_Type(fileExtension:str,filePath:str) -> bool:
    file = open(filePath,"w")
    extensiones_comunes.append(fileExtension)
    print(extensiones_comunes)
    json.dump({"extensiones_comunes":extensiones_comunes},file)
    file.close()
    return True


def scan_File_Documents_From_Path(path=base_Path,delTime:int=30) -> list[str]:
    """
    (str)path
    -> Full path of directory to scan files/Direccion completa al directorio a escanear\n
    (int)delTime
    -> Time limite to use to delete files in directory/Tiempo limite a usar para borrar archivos en directorio\n
    (list)returns
    -> returns a list of all the files that excedess the time limite and can be remove/retorna una lista de todos los archivos que exceden el limite de tiempo y puede ser removidos\n
    """

    #Archivos lista para almacenar nomsbres de archivos que pasaron el tiempo especifico y seran borrados
    archivos = []
    #present_Time almacena el tiempo actual con el cual realiza la comparacion
    present_Time = datetime.now()
    #try except para cambiar de ubicacion 
    try:

        os.chdir(path)
    except Exception as e:
        print("no existe el lugar\n")
        raise e

    #elementos guarda una lista con los nombres de todos los archivos y directorios dentro de la ubicacion actual
    elementos = os.listdir("./")
    #Paso por cada uno de los nombres  
    for elemento in elementos:
        
        #Obtencion de la ultima fecha de acceso o uso del archivo sin formatear
        #time_Diference es la diferencia de los entre el tiempo actual y la ultima vez del acceso 
        #se hace uso del datetime.fromtimestamp() para estructurar el tiempo de forma que sea operable 
        last_Acces_Time_raw = os.path.getctime(elemento)
        last_Acces_Time_proces = datetime.fromtimestamp(last_Acces_Time_raw)
        time_Diference = present_Time - last_Acces_Time_proces
        
        #Impresion en pantalla de la informacion de diferencia entre tiempo actual y ultimo acceso 
        #strftime usado para darle un formato especifico 
        print (last_Acces_Time_proces.strftime(f'{elemento}\nSu ultimo acceso fue en \nFecha ==> %Y-%m-%d \nHora ==> %H:%M'))
        print (f'ha pasado un tiempo de: { time_Diference.days } dias y {time_Diference.seconds // (60*60)} horas desde su ultimo acceso',end="\n\n")


        if time_Diference.days >= delTime:
            archivos.append(elemento)
    return archivos

def delete_List_Files_From_Path(arreglo:list[str],path=base_Path) -> None:
    """
    Function to delete files from a list of names and a path/Funcion para borrar archivos de una lista de nombres y una direccion
    """
    try:
        for archivo in arreglo:
            if os.path.isfile(archivo) == True:
                os.remove(path+archivo)
            else:
                rmtree(archivo)

    except Exception as e:
        print(f'error con el borrado de archivos')
        raise e
       
    



def main():
    archivos_A_Borrar = scan_File_Documents_From_Path()
    print(f"se borraran los siguientes {len(archivos_A_Borrar)} archivos y/o directorios: \n {archivos_A_Borrar}")
    respuesta = input("Desea continuar Y/N:\t")
    if respuesta.upper() in ["YES","Y","S","SI"]:
        delete_List_Files_From_Path(archivos_A_Borrar,base_Path)
    else:
        print(f'No se borraran los archivos')



if __name__ == "__main__":
    main()
    #Todo
    #add process for dir
    #make it recursive 
    #make use of avoid selection file


 

