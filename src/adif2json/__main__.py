import sys
import os
import argparse
import logging

import chardet

from adif2json.adif import to_json_lines
from adif2json.json import from_json_generator


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


# TODO: rename, this function is not about adif at all
def read_adif_lines(nombre_archivo, encoding):
    with open(nombre_archivo, "r", encoding=encoding) as f:
        logging.info(f"Reading file {nombre_archivo} with encoding {encoding}")
        for line in f.readlines():
            yield line


def write_json_lines(in_file, out_path, encoding):
    with open(out_path, "w", encoding="utf-8") as out_file:
        try:
            adif = read_adif_lines(in_file, encoding)
            out = to_json_lines(adif)
            lines = 0
            logging.debug(f"Writing to {out_path}")
            for l in out:
                lines += 1
                logging.debug(f"Writing line {lines}")
                out_file.write(l)
            logging.info(f"Written {lines} lines to {out_path}")
        except UnicodeDecodeError as e:
            logging.error(f"Error decoding line: {e}")
            logging.error(f"Try with encoding: {get_encoding(in_file)}")
            logging.error("Please provide correct encoding")


def adif2json():
    parser = argparse.ArgumentParser(description="ADIF to JSONL converter")
    parser.add_argument(
        "--encoding", type=str, default="utf-8", help="El encoding del archivo"
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Activa los logs")
    parser.add_argument("file_path", type=str, help="La ruta del archivo a procesar")
    parser.add_argument(
        "folder_path", type=str, help="La ruta de la carpeta de destino"
    )
    args = parser.parse_args()

    logging.StreamHandler(sys.stdout)
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
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

    logging.info(f"Converting {args.file_path} to {out_path}")
    write_json_lines(args.file_path, out_path, args.encoding)


def write_adif_file(in_file, out_path, encoding):
    with open(out_path, "w", encoding="utf-8") as out_file:
        try:
            jsonl = read_adif_lines(in_file, encoding)
            adi = from_json_generator(jsonl)
            for l in adi:
                out_file.write(l)
        except UnicodeDecodeError as e:
            logging.error(f"Error decoding line: {e}")
            logging.error(f"Try with encoding: {get_encoding(in_file)}")
            logging.error("Please provide correct encoding")


def json2adif():
    parser = argparse.ArgumentParser(description="JSONL to ADIF converter")
    parser.add_argument(
        "--encoding", type=str, default="utf-8", help="El encoding del archivo"
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Activa los logs")
    parser.add_argument("file_path", type=str, help="La ruta del archivo a procesar")
    parser.add_argument(
        "folder_path", type=str, help="La ruta de la carpeta de destino"
    )

    args = parser.parse_args()

    logging.StreamHandler(sys.stdout)
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.ERROR)

    if not os.path.isfile(args.file_path):
        logging.error(f"El archivo {args.file_path} no existe")
        sys.exit(1)

    if not os.path.isdir(args.folder_path):
        logging.error(f"La carpeta {args.folder_path} no existe")
        sys.exit(1)

    filename = os.path.basename(args.file_path)
    out_path = os.path.join(args.folder_path, f"{filename}.adif")

    if os.path.isfile(out_path):
        logging.error(f"El fichero de salida ya existe: {out_path}")
        sys.exit(1)

    logging.info(f"Converting {args.file_path} to {out_path}")
    write_adif_file(args.file_path, out_path, args.encoding)
