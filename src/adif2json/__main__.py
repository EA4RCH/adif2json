import sys
import os
import argparse
import logging


import chardet


from adif2json.adif import to_json_lines


# TODO: filemagic?
def get_encoding(file_path):
    with open(file_path, "rb") as f:
        logging.info(f"Detecting encoding for file {file_path}")
        rawdata = f.read()
    encoding = chardet.detect(rawdata)["encoding"]
    logging.info(f"Detected encoding: {encoding}")
    return encoding


def read_adif(nombre_archivo, encoding):
    with open(nombre_archivo, "r", encoding=encoding) as f:
        logging.info(f"Reading file {nombre_archivo} with encoding {encoding}")
        return f.read()


def write_json_lines(in_file, out_path, encoding):
    with open(out_path, "w") as out_file:
        try:
            adif = read_adif(in_file, encoding)
            logging.info(f"Readed {len(adif)} characters from {in_file}")
            out = to_json_lines(adif)
            logging.info(f"Writing {len(out)} characters to {out_path}")
            out_file.write(out)
        except UnicodeDecodeError as e:
            logging.error(f"Error decoding line: {e}")
            logging.error(f"Try with encoding: {get_encoding(in_file)}")
            logging.error("Please provide correct encoding")


def adif2json():
    # Crear el analizador de argumentos
    parser = argparse.ArgumentParser(description='ADIF to JSONL converter')

    # Añadir el argumento opcional para encoding con valor por defecto 'utf-8'
    parser.add_argument('--encoding', type=str, default='utf-8',
                        help='El encoding del archivo')

    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Activa los logs')

    parser.add_argument('file_path', type=str,
                        help='La ruta del archivo a procesar')

    parser.add_argument('folder_path', type=str,
                        help='La ruta de la carpeta de destino')

    # Analizar los argumentos
    args = parser.parse_args()

    logging.StreamHandler(sys.stdout)
    if args.verbose:
        logging.getLogger().setLevel(logging.INFO)
    else:
        logging.getLogger().setLevel(logging.ERROR)

    if not os.path.isfile(args.file_path):
        logging.error(f"El archivo {args.file_path} no existe")
        sys.exit(1)

    if not os.path.isdir(args.folder_path):
        logging.error(f"La carpeta {args.folder_path} no existe")
        sys.exit(1)

    filename = os.path.basename(args.file_path)
    out_path = os.path.join(args.folder_path, f"{filename}.jsonl")

    if os.path.isfile(out_path):
        logging.error(f"El fichero de salida ya existe: {out_path}")
        sys.exit(1)

    logging.info(f"Converting {args.file_path} to {out_path} with encoding {args.encoding}")
    write_json_lines(args.file_path, out_path, args.encoding)
