from setuptools import setup

setup(
    name="audit-securite",
    version="0.1",
    py_modules=["app"],  # On indique que ton code est dans app.py
    install_requires=[
        "typer",
    ],
    entry_points={
        'console_scripts': [
            # La commande à taper dans le terminal = fichier:objet_typer
            'audit-securite = app:app',
        ],
    },
)