import ckan.plugins as p
from ckan.plugins.toolkit import add_template_directory

from ckanext.fluent import validators



class FluentPlugin(p.SingletonPlugin):
    p.implements(p.IValidators)
    p.implements(p.IConfigurer)

    def update_config(self, config):
        """
        We have some form snippets that support ckanext-scheming
        """
        add_template_directory(config, 'templates')

    def get_validators(self):
        return {
            'fluent_text': validators.fluent_text,
            'fluent_text_output':
                validators.fluent_text_output,
            }
