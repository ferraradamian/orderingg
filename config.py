# Solucionado tipo D100 Missing docstring in public module. Pablo.

"""Encontre que haciendo esto se solucionaba."""

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    """Encontre que haciendo esto se solucionaba."""

    # Solucionado tipo D101 Missing docstring in public class. Pablo.

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# Solucionado tipo W292 no newline at end of file. Pablo.
