"""Provide a class to handle GNU gettext translation files.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/yw_tlview.xx
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import sys
import os
from string import Template
from datetime import datetime
from settings import *

poHeader = '''\
# ${app} Dictionary (English-${languageName})
# Copyright (C) 2023 ${provider}
#
msgid ""
msgstr ""
${version_id}
${pot_creation}
"PO-Revision-Date: ${datetime}\\n"
"Last-Translator: ${lastTranslator}\\n"
"Language: ${languageCode}\\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=UTF-8\\n"
"Content-Transfer-Encoding: 8bit\\n"


'''


class Translations:
    """Class to handle GNU gettext translation files.
    
    - .po file and .pot file are in the same directory.
    - Existing translations are used.
    - Missing translations are taken from a JSON dictionary, if any.
    - The JSON dictionary is updated by translations found in the initial '.po' file.
    """

    def __init__(self, potPath, app=''):
        self.poFile = f'{potPath}/{languageCode}.po'
        self.potFile = f'{potPath}/messages.pot'
        self.msgDict = {}
        self.msgList = []
        self.header = ''
        self.app = app
        self.currentDateTime = datetime.today().replace(microsecond=0).isoformat(sep=" ")
        self.potCreation = f'"POT-Creation-Date: {self.currentDateTime}\\n"'

    def read_pot(self):
        """Read the messages of the '.pot' file.
        
        Parse the file and collect messages in msgList.
        """
        msgCount = 0
        print(f'Reading "{self.potFile}" ...')
        with open(self.potFile, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        inHeader = True
        for line in lines:
            line = line.strip()
            if line.startswith('msgid ""'):
                pass
            elif inHeader:
                if line.startswith('"POT-Creation-Date'):
                    self.potCreation = line
                elif line.startswith('"Project-Id-Version'):
                    self.versionId = line
                elif line.startswith('msgid "'):
                    inHeader = False
            if not inHeader:
                if line.startswith('msgid "'):
                    self.msgList.append(self._extract_text('msgid "', line))
                    msgCount += 1
            self.msgList.sort()
        print(f'{msgCount} entries read.')

    def read_po(self):
        """Read the existing translations of the '.po' file.
        
        Parse the file and collect translations in msgDict.
        """

        # Create the header.
        msgMap = {'app': self.app,
                  'datetime':self.currentDateTime,
                  'pot_creation': self.potCreation,
                  'version_id': self.versionId,
                  'languageName': languageName,
                  'languageCode': languageCode,
                  'provider': provider,
                  'lastTranslator': lastTranslator,
                  }
        hdTemplate = Template(poHeader)
        self.header = hdTemplate.safe_substitute(msgMap)

        print(f'Reading "{self.poFile}" ...')
        try:
            with open(self.poFile, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except FileNotFoundError:
            print('Not found.')
            return

        inHeader = True
        msgCount = 0
        for line in lines:
            line = line.strip()
            if line.startswith('msgid ""'):
                pass
            elif inHeader:
                if line.startswith('msgid "'):
                    inHeader = False
            if not inHeader:
                if line.startswith('msgid "'):
                    message = self._extract_text('msgid "', line)
                    msgCount += 1
                elif line.startswith('msgstr "'):
                    translation = self._extract_text('msgstr "', line)
                    if translation:
                        self.msgDict[message] = translation
        print(f'{msgCount} entries read.')
        print(f'{len(self.msgDict)} translations total.')

    def write_po(self):
        """Write translations to the '.po' file.

        Return True, if all messages have translations.
        Return False, if messages need to be translated. 
        """
        lines = [self.header]
        missingCount = 0
        msgCount = 0
        for message in self.msgList:
            try:
                translation = self.msgDict[message]
            except:
                translation = ''
            lines.append(f'msgid "{message}"\nmsgstr "{translation}"\n\n')
            if not translation:
                print(f'Translation missing for "{message}".')
                missingCount += 1
            msgCount += 1
        print(f'Writing "{self.poFile}" ...')
        if os.path.isfile(self.poFile):
            os.replace(self.poFile, f'{self.poFile}.bak')
            backedUp = True
        else:
            backedUp = False
        try:
            with open(self.poFile, 'w', encoding='utf-8') as f:
                f.writelines(lines)
        except Exception as ex:
            if backedUp:
                os.replace(f'{self.poFile}.bak', self.poFile)
            print(f'ERROR: Cannot write file: "{self.poFile}".\n{ex}')
            return False

        if missingCount > 0:
            print(f'NOTE: {missingCount} translations missing.')
            return False

        print(f'{msgCount} entries written.')
        return True

    def _extract_text(self, prefix, line):
        firstPos = len(prefix)
        lastPos = len(line) - 1
        message = line[firstPos:lastPos]
        return message


def main(potPath, app='', appVersion='unknown'):
    """Update a '.po' translation file.
    
    - Add missing entries from the '.pot' template file.
    
    Return True, if all messages have translations.
    Return False, if messages need to be translated. 
    """
    translations = Translations(potPath, app=app)
    translations.read_pot()
    translations.read_po()
    if translations.write_po():
        return True
    else:
        return False


if __name__ == '__main__':
    main(sys.argv[1])
