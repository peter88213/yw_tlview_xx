"""Download the latest "messages.pot" file from the GitHub repository.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/yw_tlview.xx
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
import urllib.request

POT_URL = 'https://raw.githubusercontent.com/peter88213/yw_tlview/refs/heads/main/i18n/messages.pot'

targetPath = '../i18n/'
with urllib.request.urlopen(POT_URL) as f:
    dataStr = f.read().decode('utf-8')
os.makedirs(targetPath, exist_ok=True)
with open(f'{targetPath}/messages.pot', 'w', encoding='utf-8') as f:
    f.write(dataStr)

print('Done.')

