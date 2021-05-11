#!/usr/bin/env python3
'''
Dafault: create wheel
'''
import glob
from doit.tools import create_folder

DOIT_CONFIG = {'default_tasks': ['all']}


def task_gitclean():
    """Clean all generated files not tracked by GIT."""
    return {
            'actions': ['git clean -xdf'],
           }


def task_html():
    """Make HTML documentationi."""
    return {
            'actions': ['sphinx-build -M html docs build'],
           }


def task_test():
    """Preform tests."""
    yield {'actions': ['coverage run -m unittest -v'], 'name': "run"}
    yield {'actions': ['coverage report'], 'verbosity': 2, 'name': "report"}


def task_pot():
    """Re-create .pot ."""
    return {
            'actions': ['pybabel extract -o main.pot SuperCat'],
            'file_dep': glob.glob('SuperCat/*.py'),
            'targets': ['main.pot'],
           }


def task_po():
    """Update translations."""
    return {
            'actions': ['pybabel update -D main -d po -i main.pot'],
            'file_dep': ['main.pot'],
            'targets': ['po/ru/LC_MESSAGES/main.po'],
           }


def task_mo():
    """Compile translations."""
    return {
            'actions': [
                (create_folder, ['SuperCat/ru/LC_MESSAGES']),
                'pybabel compile -D main -l ru -i po/ru/LC_MESSAGES/main.po -d SuperCat'
                       ],
            'file_dep': ['po/ru/LC_MESSAGES/main.po'],
            'targets': ['SuperCat/ru/LC_MESSAGES/main.mo'],
           }


def task_sdist():
    """Create source distribution."""
    return {
            'actions': ['python -m build -s'],
            'task_dep': ['gitclean'],
           }


def task_wheel():
    """Create binary wheel distribution."""
    return {
            'actions': ['python -m build -w'],
            'task_dep': ['mo'],
           }


def task_app():
    """Run application."""
    return {
            'actions': ['python -m SuperCat'],
            'task_dep': ['mo'],
           }


def task_style():
    """Check style against flake8."""
    return {
            'actions': ['flake8 SuperCat',
                        'flake8 test']
           }


def task_docstyle():
    """Check docstrings against pydocstyle."""
    return {
            'actions': ['pydocstyle SuperCat',
                        'pydocstyle test']
           }


def task_check():
    """Perform all checks."""
    return {
            'actions': None,
            'task_dep': ['style', 'docstyle', 'test']
           }


def task_all():
    """Perform all build task."""
    return {
            'actions': None,
            'task_dep': ['check', 'wheel', 'req']
           }


def task_req():
    """Try to calculate runtime requirements."""
    return {
            'actions': ['pymin_reqs -d SuperCat'],
            'verbosity': 2
           }


def task_buildreq():
    """Try to calculate build requirements."""
    return {
            'actions': ['python BuildReq.py doit all'],
            'task_dep': ['gitclean'],
           }