#!/usr/bin/python
import sys, os, time, shutil

#
#adif2JSON: Lee fichero .adif y genera JSON, solo con las etiquetas deseadas.
#

LISTA_TAGS = [ 'CALL', 'QSO_DATE', 'TIME_ON', 'BAND', 'FREQ', 'CONTEST_ID', 'MODE', 'RST_SENT', 'RST_RCVD' ]

TABULADOR = "\t"

def main(argv):

    num_records = 0
    
    #------------------------------------------------------------------------------------------------
    # Reading arguments
    #------------------------------------------------------------------------------------------------
    if (len(sys.argv) < 2):
        print ("uso: " + sys.argv[0] + " <.adi>")
        sys.exit()

    #------------------------------------------------------------------------------------------------
    #Open file for reading
    #------------------------------------------------------------------------------------------------
    sourceFile = sys.argv[1]
    fd_in = open(sourceFile, "r", encoding="cp437", errors='ignore')
    if (fd_in == 0):
        print("#Error: no se puede abrir fichero para lectura.. " + sourceFile)
        sys.exit()
  
    #Leo fichero y lo cierro
    lineas = fd_in.readlines()
    fd_in.close()
    
    if len(lineas) <= 0:
        print("#Error: .adi esta vacio");
        sys.exit()        

    #------------------------------------------------------------------------------------------------
    #Open file for writing
    #------------------------------------------------------------------------------------------------
    targetFile = sourceFile
    targetFile = targetFile.replace(".adif", ".json", 1)
    targetFile = targetFile.replace(".adi", ".json", 1)
    fd_out = open(targetFile, "w")
    if (fd_out == 0):
        print("#Error: no se puede abrir fichero para escritura.. " + targetFile)
        sys.exit()


    #Abro corchete para comienzo del archivo JSON
    output_buffer = "[\n"

    #Procesamos linea a linea
    for linea in lineas:

        diccionario = {}
        procesar_registros = False

        #Elimino saltos de linea y espacios en blanco
        linea = linea.strip()

        #Busco primer registro para comenzar con el proceso de registros
        if linea.find("CALL:") >= 0:
            procesar_registros = True

        if procesar_registros:
        
            if len(linea) == 0:
                continue

            #Troceo por '<'
            tokens = linea.split('<')

            #Construyo diccionario (clave, valor) con las etiquetas elegidas
            for tk in tokens:
                #Troceo por '>'
                lista = tk.split('>')

                #Elimino primer elemento vacio
                lista = lista[0:]

                #Troceamos por ':' para obtener primer elemento
                clave = lista[0].split(':')

                #Si la clave esta en lista de etiquetas deseadas, la meto en el diccionario
                if clave[0] in LISTA_TAGS:
                    diccionario[lista[0]] = lista[1].strip()

            #Obtengo listado de claves ordenadas
            lista_claves_ordenada = sorted(diccionario.keys())

            #Abrimos llave para escribir el registro
            output_buffer += "{0}{1}\n".format(TABULADOR,'{')

            #Escribimos los atributos del registro cada uno en una linea
            for k in lista_claves_ordenada:
                output_buffer += "{0}{0}\"{1}\": \"{2}\",\n".format(TABULADOR, k, diccionario[k])

            #Eliminamos la ',' del ultimo registro y cerramos llave de registro
            output_buffer = output_buffer[:-2]
            output_buffer += "\n{0}{1},\n".format(TABULADOR,'}')
            
            num_records += 1


    #Eliminamos ultima ',' y cerramos con ']' el archivo JSON
    if num_records > 0:
        output_buffer = output_buffer[:-2]
        output_buffer += "\n"
    
    #Cerramos JSON, escribimos buffer en disco y cerramos fichero
    output_buffer += "]\n"
    fd_out.write(output_buffer)
    fd_out.close()
    
    print("Se han exportado {0} registros..".format(num_records))

    #Salimos del programa
    sys.exit()



if __name__ == "__main__":
    main(sys.argv[1:])