from distutils.core import setup

setup(
    name='ExtractRepetitions',
    version='0.1.0',
    author='Miha Stopar',
    author_email='miha.stopar@xlab.si',
    packages=['entextractor'],
    description="Automatic extraction of repeated entities on web pages.",
    long_description=open('README.rst').read(),
    install_requires=[
        "requests",
        "BeautifulSoup",
    ],
)