from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='adif2json',
    version='0.1',
    description='Una herramienta para convertir archivos ADIF a JSON',
    py_modules=["adif2json"],
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='César Gallego Rodríguez',
    author_email='gallego.cesar@gmail.com',
    url='https://github.com/username/adif2json',
    packages=find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
        # 'nombrePaquete>=versionMinima',
    ],
    entry_points={
        'console_scripts': [
            'adif2json=adif2json.__main__:adif2json',
        ]
    },
)
