"""
delete all compiled binaries files
"""
import os
import argparse


def delete_binaries(folder_path=None):
    """
    delete binaries given a folder, if not given,
    delete migration_files under current folder directory
    """
    # find all binary folders
    if not folder_path:
        folder_path = os.getcwd()
    for a,b,c in os.walk(folder_path):
        if a.endswith('__pycache__'):
            # find all binary files
            migration_files = [f for f in c if f.endswith('.pyc')]
            for f in migration_files:
                print(os.path.join(a, f))
                # delete binary files
                os.remove(os.path.join(a, f))


if __name__ == '__main__':
    delete_binaries()
