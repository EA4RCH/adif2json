from setuptools import setup

setup(
    name='adif2json',
    version='0.1.0',
    author='Cesar Gallego',
    author_email='gallego.cesar@gmail.com',
    description='convert adif to json and back',
    license='MIT',
    packages=['adif2json'],
    entry_points={
        'console_scripts': [
            'adif2json = adif2json.__main__:main',
            'json2adif = adif2json.__main__:json2adif'
        ]
    },
)
