# encoding: utf-8
'''Tests for the ckanext.fluent extension's validators.

'''
import pytest
import ckan.tests.helpers as helpers


@pytest.mark.usefixtures('clean_db', 'with_plugins', 'with_request_context')
class TestFluentCoreTranslatedOutput(object):
    '''Test class for fluent_core_translated_output output validator.
    '''
    def test_core_field_value_returned(self):
        '''Return a value for a core field based on the _translated field
        multilingual dict. Test assumes ckan.locale_default is en or not set.
        '''
        dataset = helpers.call_action(
            'package_create',
            type = 'fluent-test',
            title_translated = {
                'en': 'Title',
                'fr': 'Titre'
            },
            name = 'name-slug'
        )

        assert dataset["title"] == "Title"
