from cx_Freeze import setup, Executable

setup(name='Saurin',
      version="0.1",
      description="Exe stuff",
      executables= [Executable('main_function.py')])


