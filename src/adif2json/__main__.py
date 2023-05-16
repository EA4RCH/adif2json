import sys
import os

from adif2json.adif import to_json

def adif2json():
    if len(sys.argv) != 3:
        print("Uso: adif2json <fichero_entrada> <carpeta_salida>")
        sys.exit(1)

    fichero_entrada, carpeta_salida = sys.argv[1], sys.argv[2]

    if not os.path.isfile(fichero_entrada):
        print(f"No se encuentra el fichero de entrada: {fichero_entrada}")
        sys.exit(1)

    if not os.path.isdir(carpeta_salida):
        print(f"No se encuentra la carpeta de salida: {carpeta_salida}")
        sys.exit(1)


    with open(fichero_entrada, "r") as in_file, open(os.path.join(carpeta_salida, f"{fichero_entrada}.json"), "w") as out_file:
        adif = in_file.read()
        out = to_json(adif)
        out_file.write(out)
