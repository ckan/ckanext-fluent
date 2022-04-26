from ckanext.fluent.helpers import (
    fluent_form_languages,
    fluent_alternate_languages,
    fluent_form_label
)


class TestFluentHelpers(object):

    def test_fluent_form_languages_field(self):
        field = {
            'form_languages': ['en', 'es']
        }
        res = fluent_form_languages(field=field)
        assert res == ['en', 'es']

    def test_fluent_form_languages_schema(self):
        schema = {
            'form_languages': ['en', 'fr']
        }
        res = fluent_form_languages(schema=schema)
        assert res == ['en', 'fr']

    def test_fluent_alternate_languages_field(self):
        field = {
            'alternate_languages': {'en': ['en-GB']}
        }
        res = fluent_alternate_languages(field=field)
        assert res == {'en': ['en-GB']}

    def test_fluent_alternate_languages_schema(self):
        schema = {
            'alternate_languages': {'en': ['en-GB']}
        }
        res = fluent_alternate_languages(schema=schema)
        assert res == {'en': ['en-GB']}

    def test_fluent_form_label_exists(self):
        
        field = {
            'fluent_form_label': {
                'en': 'English label',
                'fr': 'French label'
            }
        }
        lang = 'en'
        res = fluent_form_label(field, lang)
        assert res == 'English label'

    def test_fluent_form_label_not_exists(self):
        
        field = {
            'fluent_form_label': {
                'en': 'English label',
                'fr': 'French label'
            },
            'label': 'Standard label'
        }
        lang = 'es'
        res = fluent_form_label(field, lang)
        assert res == 'ES Standard label'
