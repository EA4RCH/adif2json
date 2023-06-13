# Instalación

Para instalar `adif2json`, necesitas tener instalado Python y pip, el gestor de paquetes de Python. Si aún no los tienes instalados, puedes encontrar las instrucciones de instalación en las páginas oficiales de [Python](https://www.python.org/) y [pip](https://pip.pypa.io/en/stable/installing/).

Además, es recomendable usar un entorno virtual de Python (virtualenv) para evitar conflictos de dependencias entre diferentes proyectos de Python en tu sistema.

A continuación, te explicamos cómo crear un virtualenv e instalar `adif2json` dentro de este:

1. Abre una terminal.

2. Instala `virtualenv` si aún no lo tienes. Para esto, escribe el siguiente comando y presiona `Enter`:

    ```bash
    pip install virtualenv
    ```

   Ten en cuenta que si tienes Python 3.5 o superior el módulo virtualenv ahora viene incluido de serie.
   
3. Crea un nuevo virtualenv en la ubicación que prefieras utilizando el siguiente comando:

    ```bash
    python -m venv /ruta/a/mi/virtualenv
    ```

    Esto creará un nuevo virtualenv en la ruta `/ruta/a/mi/virtualenv`. Puedes cambiar esta ruta a la ubicación que prefieras.

4. Activa el virtualenv que acabas de crear:

    En sistemas Unix o MacOS, usa el siguiente comando:

    ```bash
    source /ruta/a/mi/virtualenv/bin/activate
    ```

    En Windows, usa el siguiente comando:

    ```bash
    \ruta\a\mi\virtualenv\Scripts\activate
    ```

    Deberías ver que el prompt de tu terminal cambia para mostrar el nombre del virtualenv que acabas de activar.

5. Una vez activado el virtualenv, instala `adif2json` directamente desde su repositorio en GitHub utilizando pip con el siguiente comando:

    ```bash
    pip install git+https://github.com/CesarGallego/adif2json.git
    ```

    Este comando le dice a pip que instale el paquete directamente desde el repositorio de GitHub.

6. Una vez que la instalación se haya completado, puedes verificar que `adif2json` se instaló correctamente ejecutando el siguiente comando:

    ```bash
    adif2json --help
    ```

    Deberías ver un mensaje de ayuda con información sobre cómo usar `adif2json`.

¡Eso es todo! Ahora deberías tener `adif2json` instalado en tu virtualenv y estar listo para usarlo para convertir archivos ADIF a JSON.

Recuerda que cada vez que quieras usar `adif2json`, debes activar primero el virtualenv en el que lo instalaste. Cuando termines de usarlo, puedes desactivar el virtualenv con el comando `deactivate`.

Nota: La ruta `/ruta/a/mi/virtualenv` es un ejemplo. Debes reemplazarla con la ruta donde deseas crear tu virtualenv.

# Cómo usar `adif2json`

## Descripción

El script `adif2json` toma un fichero ADIF (Amateur Data Interchange Format) como entrada y genera un fichero JSON como salida. El fichero de entrada debe ser un archivo existente, y el lugar donde se guardará el archivo de salida es una carpeta existente. Si el archivo de salida ya existe en la carpeta especificada, el script se detendrá para evitar sobrescribir archivos existentes.

## Uso

Para usar el script `

adif2json`, necesitas tener instalado Python y ejecutarlo desde la línea de comandos.

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

En el caso de que sea necesario puedes agregar los metadatos que quieras a las filas del fichero de salida. Para esto solo necesitas poner un fichero con el mismo nombre que el fichero de entrada, pero con la extensión .meta.

Estos metadatos se pueden utilizar para agregar información y usarla en otros programas, como en la carga para un diploma o similar. El fichero meta es un fichero JSON, y su contenido será agregado a todos los qsos que se generen en el campo `_meta`.

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
