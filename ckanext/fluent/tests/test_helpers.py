from ckanext.fluent.helpers import (
    fluent_form_languages,
    fluent_alternate_languages,
    fluent_form_label
)


class TestFluentHelpers(object):
    """ TODO """

    def test_fluent_form_languages(self):
        """ Not a real test. """
        res = fluent_form_languages()

    def test_fluent_alternate_languages(self):
        """ Not a real test. """
        res = fluent_alternate_languages()

    def test_fluent_form_label(self):
        """ Not a real test. """
        field = {
            'label': 'some label'
        }
        lang = 'en'
        res = fluent_form_label(field, lang)
