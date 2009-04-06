import os
import errno
import shutil
import locale

from umit.core import BasePaths

class AlreadyExistsError(Exception):
    def __init__(self, msg, backup_path):
        self._msg = msg
        self.backup_path = backup_path

    def __str__(self):
        return self._msg

def merge():
    """Moves the old ~/.umit to the new configuration directory, this new
    one is the user's local appdata if using nt with umit 1.0beta2 or newer."""
    if os.name != 'nt':
        # There is nothing to do here.
        return

    if BasePaths.UMIT_CFG_DIR == 'umit':
        # This is indeed a version new enough of umit.
        old_path = os.path.join(os.path.expanduser("~"), ".umit")
        old_path = old_path.decode(locale.getdefaultlocale()[1])

        backup_path = old_path + '_backup'
        if os.path.exists(old_path):
            # Move the old ~/.umit to ~/.umit_backup so next time this
            # merger runs it will notice the ausence of ~/.umit
            shutil.move(old_path, backup_path)

            new_path = os.path.join(BasePaths.HOME, BasePaths.UMIT_CFG_DIR)
            if os.path.exists(new_path):
                # Destination already exists, need to merge the files
                # from the old directory to this new one.
                return backup_path
            else:
                shutil.copytree(backup_path, new_path)
