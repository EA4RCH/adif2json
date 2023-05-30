import sys
import os
import argparse
import chardet

from adif2json.adif import to_json_lines


# TODO: filemagic?
def get_encoding(file_path):
    with open(file_path, "rb") as f:
        rawdata = f.read()
    return chardet.detect(rawdata)["encoding"]


def read_adif_lines(nombre_archivo, encoding):
    with open(nombre_archivo, "r", encoding=encoding) as f:
        return f.readlines()


def write_json_lines(in_file, out_path, encoding):
    with open(out_path, "w") as out_file:
        try:
            for lines in read_adif_lines(in_file, encoding):
                out = to_json_lines(lines)
                for jsline in out:
                    out_file.write(jsline)
            return
        except UnicodeDecodeError as e:
            print(f"Error decoding line: {e}")
            print(f"Maybe you should try with encoding: {get_encoding(in_file)}")
            print("Please provide correct encoding")


def adif2json():
    # Crear el analizador de argumentos
    parser = argparse.ArgumentParser(description='ADIF to JSONL converter')

    # Añadir el argumento opcional para encoding con valor por defecto 'utf-8'
    parser.add_argument('--encoding', type=str, default='utf-8',
                        help='El encoding del archivo')

    parser.add_argument('file_path', type=str,
                        help='La ruta del archivo a procesar')

    parser.add_argument('folder_path', type=str,
                        help='La ruta de la carpeta de destino')

    # Analizar los argumentos
    args = parser.parse_args()

    # Comprobar si los archivos y carpetas existen
    if not os.path.isfile(args.file_path):
        print(f"El archivo {args.file_path} no existe")
        return

    if not os.path.isdir(args.folder_path):
        print(f"La carpeta {args.folder_path} no existe")
        return

    filename = os.path.basename(args.file_path)
    out_path = os.path.join(args.folder_path, f"{filename}.jsonl")

    if os.path.isfile(out_path):
        print(f"El fichero de salida ya existe: {out_path}")
        sys.exit(1)

    write_json_lines(args.file_path, out_path, args.encoding)
