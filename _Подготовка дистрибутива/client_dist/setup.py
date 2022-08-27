from setuptools import setup, find_packages

setup(name="py_bestmess_client",
      version="0.1.1",
      description="Mess Client",
      author="Pavel Zhirnov",
      author_email="pavel@inbox.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
