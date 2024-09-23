import os
from datetime import datetime
import json
import sys


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
json_Data_File = open("fileType.json",'r') 
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


def obtener_Extension(fileName:str) -> str:
    """
    Function with the objetive of recive a file name and return his extension
    it works bases on the last "." of the text 
    
    Exception case!
    if the dir uses "." in it's name this will cause to be check as file
    """
    position = fileName.rfind(".")
    if position == -1:
        return "NotFile"
    return fileName[position:]

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


        #Comprobacion mediante la funcion obtener_Extension si la extension del archivo esta presente
        #En caso de estar entra y se añade a la lista de archvos caso contrario se verifica si es un directorio y si tampoco se define como deconocido
        if obtener_Extension(elemento) in extensiones_comunes:
            if time_Diference.days >= delTime:
                archivos.append(elemento)
        elif obtener_Extension(elemento) == "NotFile":
            continue 
        else:
            print(f'El elemento {elemento} no es ni directorio ni un archivo conocido ',end="")
            response = input("Va a querer agregar el archivo a la lista de extensiones Yes/No: ")
            if response.upper() in ["YES","Y","SI"]:
                add_file_Type(obtener_Extension(elemento),files_Types_File)
            else:
                continue
    return archivos

def delete_List_Files_From_Path(arreglo:list[str],path=base_Path) -> None:
    """
    Function to delete files from a list of names and a path/Funcion para borrar archivos de una lista de nombres y una direccion
    """
    try:
        for archivo in arreglo:
            os.remove(base_Path+archivo)
    except Exception as e:
        print(f'error con el borrado de archivos')
        raise e
       
    



def main():
    archivos_A_Borrar = scan_File_Documents_From_Path()
    print(f"se borraran los siguientes archivos: \n {archivos_A_Borrar}")
    respuesta = input("Desea continuar Y/N:\t")
    if respuesta.upper() in ["YES","Y","S","SI"]:
        delete_List_Files_From_Path(archivos_A_Borrar,base_Path)
    else:
        print(f'No se borraran los {len(archivos_A_Borrar)} archivos')
    #add_file_Type(".lua","./fileType.json")



if __name__ == "__main__":
    main()
    #Todo
    #add process for dir
    #make it recursive 
    #make use of avoid selection file


 

