from setuptools import setup

setup(
    name='adif2json',
    version='0.1.0',
    author='Cesar Gallego',
    author_email='gallego.cesar@gmail.com',
    description='convert adif to json and back',
    license='MIT',
    packages=['adif2json'],
    install_requires=[
        "aiofiles",
        "chardet"
    ],
    entry_points={
        'console_scripts': [
            'adif2json = adif2json.adif2json:main',
            'json2adif = adif2json.json2adif:main'
        ]
    },
)
