from distutils.core import setup

install_requires = ['snowflake-connector-python']
setup(
    name='SnowflakeUtils',
    version='0.12',
    packages=['snowflake_utils'],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.md').read(),
    install_requires=install_requires,
)
