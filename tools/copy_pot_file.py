"""Copy the "messages.pot" file from the local yw_tlview directory.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/yw_tlview.xx
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
from shutil import copyfile

POT_FILE = '../../yw_tlview/i18n/messages.pot'

targetPath = '../i18n/'
if os.path.isfile(POT_FILE):
    os.makedirs(targetPath, exist_ok=True)
    copyfile(POT_FILE, f'{targetPath}/messages.pot')
    print('Done.')
