from setuptools import setup

setup(
    name = 'tickets',
    version = '0.0.1',
    py_modules = ['tickets', 'stations'],
    install_requires = ['requests', 'docopt', 'prettytable', 'colorama'],
    entry_points = {
        'console_scripts': ['tickets = tickets:cli']
    }
)
