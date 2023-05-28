import sys
import os
import chardet

import aiofiles
import asyncio

from adif2json.adif import to_json_lines


async def read_adif(nombre_archivo):
    async with aiofiles.open(nombre_archivo, "rb") as f:
        adif = await f.read()
        result = chardet.detect(adif)
        if result["confidence"] < 0.9:
            print(f"Confidence of encoding detection is low: {result['confidence']}")
            print(
                f"Please check the file: {nombre_archivo} and provide the correct encoding."
            )
            print(f"Encoding: {result['encoding']}")
            print("trying to continue...")
        if not result["encoding"]:
            print(
                f"Please check the file: {nombre_archivo} and provide the correct encoding."
            )
            exit(1)
        adif = adif.decode(result["encoding"])
        return adif


async def read_adif_lines(nombre_archivo):
    async with aiofiles.open(nombre_archivo, "r") as f:
        async for line in f:
            yield line


async def write_json_lines(in_file, out_path):
    async with aiofiles.open(out_path, "w") as out_file:
        try:
            async for l in read_adif_lines(in_file):
                out = to_json_lines(l)
                for l in out:
                    await out_file.write(l)
            return
        except UnicodeDecodeError as e:
            print(f"Error decoding line: {e}")
    # fallback
    async with aiofiles.open(out_path, "w") as out_file:
        ad = await read_adif(in_file)
        out = to_json_lines(ad)
        for l in out:
            await out_file.write(l)


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

    asyncio.run(write_json_lines(fichero_entrada, out_path))
