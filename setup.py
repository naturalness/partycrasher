from distutils.core import setup

def slurp(filename):
    with open(filename) as text_file:
        return text_file.read()

setup(
    name='Partycrasher',
    version='0.1dev',
    packages=['partycrasher',],
    author='Joshua Charles Campbell, Eddie Antonio Santos',
    license='GPLv3+',
    long_description=slurp('README.md'),
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    ],
    install_requires=slurp('requirements.txt').splitlines()
)
