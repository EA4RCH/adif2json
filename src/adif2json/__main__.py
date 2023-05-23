import sys
import os

from adif2json.adif import to_json


def archivo_streaming(nombre_archivo, tamano_bloque=1024):
    resto = b""
    with open(nombre_archivo, "rb") as f:
        while True:
            bloque = resto + f.read(tamano_bloque)
            if not bloque:
                break
            try:
                u = bloque.decode("utf-8")
            except UnicodeDecodeError as e:
                resto = bloque[e.start :]
                bloque = bloque[: e.start]
                continue
            else:
                resto = b""
            for c in u:
                yield c
            if resto:
                yield resto.decode("utf-8", "ignore")


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

    filename = os.path.basename(fichero_entrada)
    out_path = os.path.join(carpeta_salida, f"{filename}.json")

    if os.path.isfile(out_path):
        print(f"El fichero de salida ya existe: {out_path}")
        sys.exit(1)

    with open(out_path, "w") as out_file:
        adif = archivo_streaming(fichero_entrada)
        out = to_json(adif)
        out_file.write(out)
