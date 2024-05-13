from setuptools import setup, find_packages

setup(
    name='pythongame',  # A projekt neve
    version='0.4',  # A verziószám
    packages=find_packages(),  # Az összes csomag megtalálása az aktuális könyvtár alatt
    include_package_data=True,  # A csomaghoz tartozó összes adat becsomagolása, beleértve a fájlokat is
    install_requires=[  # A függőségek felsorolása
        'pygame'
    ],
    author='Muhel Nimród Róbert',
    author_email='nimrimi@gmail.com',
    description='Egy egyszerű játék grafikus megvalósítása pythonban',
    url='https://github.com/Nimie00/pythongame',
)