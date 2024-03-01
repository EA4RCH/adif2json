import json
import logging
import sys
import os
import argparse

import chardet

from adif2json.adif import to_json_lines


# TODO: filemagic? it seems to be a better option
def get_encoding(file_path):
    """
    Sometimes the encoding is not utf-8, so we need to detect it,
    if fails.
    """
    with open(file_path, "rb") as f:
        logging.info(f"Detecting encoding for file {file_path}")
        rawdata = f.read()
    encoding = chardet.detect(rawdata)["encoding"]
    logging.info(f"Detected encoding: {encoding}")
    return encoding


def read_file_lines(nombre_archivo, encoding):
    """
    Read a file line by line, just like a generator,
    so we can process big files.
    """
    with open(nombre_archivo, "r", encoding=encoding) as f:
        logging.info(f"Reading file {nombre_archivo} with encoding {encoding}")
        for line in f.readlines():
            yield line


def write_json_lines(in_file, out_path, encoding, meta):
    """
    Read a file line by line, convert it to JSONL and write it to a file.
    """
    with open(out_path, "w", encoding="utf-8") as out_file:
        try:
            adif = read_file_lines(in_file, encoding)
            out = to_json_lines(adif, meta)
            lines = 0
            logging.debug(f"Writing to {out_path}")
            for lin in out:
                lines += 1
                logging.debug(f"Writing line {lines}")
                out_file.write(lin)
            logging.info(f"Written {lines} lines to {out_path}")
        except UnicodeDecodeError as e:
            logging.error(f"Error decoding line: {e}")
            logging.error(f"Try with encoding: {get_encoding(in_file)}")
            logging.error("Please provide correct encoding")


def adif2json():
    """
    Main function for adif2json command line tool.
    This function is called when the adif2json command is executed.
    And is the main entry point for the program.
    This will provide, to administators, a way to convert ADIF files to JSONL
    without the need to write new scripts.
    """
    # start argument parse & validation
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

    if not os.path.isfile(args.file_path):
        print(f"El archivo {args.file_path} no existe")
        sys.exit(1)

    if not os.path.isdir(args.folder_path):
        print(f"La carpeta {args.folder_path} no existe")
        sys.exit(1)

    filename = os.path.basename(args.file_path)
    log_path = os.path.join(args.folder_path, f"{filename}.log")
    hand = logging.FileHandler(log_path, mode="w", encoding="utf-8")
    if args.verbose:
        hand.setLevel(logging.DEBUG)
    else:
        hand.setLevel(logging.ERROR)
    logger = logging.getLogger()
    logger.addHandler(hand)

    if not os.path.isfile(f"{args.file_path}.meta"):
        logging.warning(f"El archivo {args.file_path}.meta no existe")
        logging.warning("Se asingaran valores por defecto")
        meta = {
            "type": "hunter",
        }
    else:
        try:
            meta = json.load(open(f"{args.file_path}.meta"))
        except json.decoder.JSONDecodeError as e:
            logging.error(f"Error leyendo el archivo de metadatos: {e}")
            sys.exit(1)

    out_path = os.path.join(args.folder_path, f"{filename}.jsonl")

    if os.path.isfile(out_path):
        logging.error(f"El fichero de salida ya existe: {out_path}")
        sys.exit(1)

    # end argument parse & validation
    logging.info(f"Converting {args.file_path} to {out_path}")
    write_json_lines(args.file_path, out_path, args.encoding, meta)


def main():
    adif2json() 


if __name__ == "__main__":
    adif2json()
