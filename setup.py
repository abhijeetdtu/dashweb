from setuptools import setup

setup(
    name='dashweb',
    version='0.0.1',
    author='meekagin',
    author_email='aac@example.com',
    packages=['dashweb'],
    url='http://pypi.python.org/pypi/PackageName/',
    license='LICENSE.txt',
    description='A package that combines Dash and Plotnine to build interactive visualization apps',
    long_description=open('README.md').read(),
    install_requires=[
       "pandas",
       "flask",
       "sklearn",
       "spacy",
       "dash",
       "plotnine",
       "mizani",
       "pymongo",
       "nltk",
       "python-youtube",
       "bs4",
       "statsmodels",
       "circlify",
       "networkx",
       "dnspython",
       "gunicorn",
       "psutil"
    ],
)
