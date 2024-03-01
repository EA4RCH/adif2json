import sys
import os
import argparse
import logging

import chardet

from adif2json.json import from_json_generator


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


def write_adif_file(in_file, out_path, encoding):
    """
    Read a file line by line, convert it to ADIF and write it to a file.
    Line by line is used to process big files.
    """
    with open(out_path, "w", encoding="utf-8") as out_file:
        try:
            jsonl = read_file_lines(in_file, encoding)
            adi = from_json_generator(jsonl)
            for len in adi:
                out_file.write(len)
        except UnicodeDecodeError as e:
            logging.error(f"Error decoding line: {e}")
            logging.error(f"Try with encoding: {get_encoding(in_file)}")
            logging.error("Please provide correct encoding")


def json2adif():
    """
    Main function for json2adif command line tool.
    This function is called when the json2adif command is executed.
    And is the main entry point for the program.
    This will provide, to administators, a way to convert JSONL files to ADIF
    without the need to write new scripts.
    """
    # start argument parse & validation
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

    # end argument parse & validation
    logging.info(f"Converting {args.file_path} to {out_path}")
    write_adif_file(args.file_path, out_path, args.encoding)


if __name__ == "__main__":
    json2adif()
