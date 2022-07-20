from setuptools import setup, find_packages

setup(name='clean_foldef',
      version='1.0.0',
      description='Сode that sorts files by category',
      url='https://github.com/IvanShkvyr/sort_goit_6',
      author='Ivan Shkvyr',
      author_email='GIS2011i@gmail.com',
      license='MIT',
      packages=find_packages(),
      entry_points={'console_scripts': ['clean-folder=clean_foldef.sort:main']}
      )