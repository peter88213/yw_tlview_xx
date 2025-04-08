"""Set up translations for the yw_tlview language pack.

- Generate the language specific '*.po' dictionaries for yw_tlview and its plugins.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/yw_tlview.xx
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from settings import languageName
import translations


def main():
    print(f'Set up yw_tlview translation files for {languageName}.')

    translationsComplete = True
    poPath = f'../i18n'
    if not translations.main(poPath, app='nv_tlview'):
        translationsComplete = False
    return translationsComplete


if __name__ == '__main__':
    main()
