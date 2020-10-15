# encoding: utf-8
'''Tests for the ckanext.fluent extension.

'''

######################################
# CKAN 2.9 Basic Test
######################################

import pytest

@pytest.mark.ckan_config('ckan.plugins', 'fluent')
@pytest.mark.usefixtures('clean_db', 'with_plugins', 'with_request_context')
class TestFluent(object):
    '''Dummy test class to ensure things are working.
    '''
    def test_that_tests_run(self):
        '''Dummy test to ensure things are working before going much further.
        '''
        assert True
