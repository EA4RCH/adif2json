# Instalación

Para instalar `adif2json`, necesitas tener instalado Python y pip, el gestor de paquetes de Python. Si aún no los tienes instalados, puedes encontrar las instrucciones de instalación en las páginas oficiales de [Python](https://www.python.org/) y [pip](https://pip.pypa.io/en/stable/installing/).

Una vez que tienes Python y pip, puedes instalar `adif2json` directamente desde su repositorio en GitHub utilizando pip.

Sigue estos pasos para instalar `adif2json`:

1. Abre una terminal.

2. Escribe el siguiente comando para instalar `adif2json` y presiona `Enter`:

    ```bash
    pip install git+https://github.com/CesarGallego/adif2json.git
    ```

    Este comando le dice a pip que instale el paquete directamente desde el repositorio de GitHub.

3. Una vez que la instalación se haya completado, puedes verificar que `adif2json` se instaló correctamente ejecutando el siguiente comando:

    ```bash
    adif2json --help
    ```

    Deberías ver un mensaje de ayuda con información sobre cómo usar `adif2json`.

¡Eso es todo! Ahora deberías tener `adif2json` instalado en tu sistema y estar listo para usarlo para convertir archivos ADIF a JSON.

Nota: Puede que necesites ejecutar estos comandos con privilegios de administrador, dependiendo de tu configuración de Python y pip. En sistemas Unix, puedes hacer esto anteponiendo `sudo` a los comandos. En Windows, abre la terminal como administrador.

# Cómo usar `adif2json`

## Descripción

El script `adif2json` toma un fichero ADIF (Amateur Data Interchange Format) como entrada y genera un fichero JSON como salida. El fichero de entrada debe ser un archivo existente, y el lugar donde se guardará el archivo de salida es una carpeta existente. Si el archivo de salida ya existe en la carpeta especificada, el script se detendrá para evitar sobrescribir archivos existentes.

## Uso

Para usar el script `adif2json`, necesitas tener instalado Python y ejecutarlo desde la línea de comandos.

El comando de ejecución es `adif2json`, seguido por dos argumentos:

- `<fichero_entrada>`: La ruta al archivo ADIF que deseas convertir a JSON.
- `<carpeta_salida>`: La ruta a la carpeta donde deseas guardar el archivo JSON de salida.

Por ejemplo:

```bash
adif2json mi_archivo.adif /ruta/a/mi/carpeta
```

Este comando intentará convertir `mi_archivo.adif` a formato JSON y guardará el archivo resultante en `/ruta/a/mi/carpeta`.

Por favor, asegúrate de que tanto el archivo de entrada como la carpeta de salida existen antes de ejecutar el script. Además, si el archivo de salida ya existe, el script no se ejecutará para evitar sobrescribir archivos existentes.

Nota: Asegúrate de tener los permisos adecuados para leer el archivo de entrada y para escribir en la carpeta de salida.

# Objetivos del proyecto adif2json

El proyecto `adif2json` tiene como objetivo proporcionar una forma simple y efectiva de convertir archivos en formato Amateur Data Interchange Format (ADIF) a formato JSON y viceversa. Los principales objetivos del proyecto incluyen:

- **Conversión de ADIF a JSON:** El objetivo principal de este proyecto es convertir archivos ADIF a formato JSON. Esta característica permite a los usuarios transformar archivos ADIF a un formato más versátil y ampliamente utilizado.

- **Recuperación de JSON a ADIF:** Además de convertir archivos ADIF a JSON, `adif2json` también tiene como objetivo proporcionar la capacidad de recuperar el archivo ADIF original a partir del archivo JSON generado.

- **Verificación de la Correctitud del Formato:** El proyecto garantiza que el proceso de conversión entre ADIF y JSON respeta el formato correcto de ambos tipos de archivos.

## Limitaciones del proyecto adif2json

Aunque el proyecto `adif2json` está diseñado para manejar conversiones entre formatos ADIF y JSON, es importante señalar sus limitaciones:

- **No se realiza Validación de Datos:** `adif2json` no valida los datos contenidos en los archivos. Su función principal es convertir los formatos de archivo, no verificar la corrección de los datos.

- **No se realiza Conversión a Otros Formatos de Archivo de Radioaficionados:** El proyecto está específicamente diseñado para manejar archivos ADIF y JSON. No admite la conversión desde o hacia otros formatos de archivo utilizados en la radioafición.

- **No Repara ni Modifica Archivos ADIF:** `adif2json` no proporciona la funcionalidad de reparar o modificar archivos ADIF. Es únicamente una herramienta de conversión.

Al entender estos objetivos y limitaciones, los usuarios pueden utilizar de manera efectiva `adif2json` para sus necesidades de conversión de archivos ADIF y JSON.
