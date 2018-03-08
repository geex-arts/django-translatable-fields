from django.conf import settings
from django.utils import translation


class TranslatableValue(dict):
    def __str__(self):
        language = translation.get_language() or settings.LANGUAGE_CODE
        languages = [language]

        if len(self):
            languages.append(list(self.keys())[0])

        for lang_code in languages:
            value = self.get(lang_code)
            if value:
                return value or ''

        return ''
