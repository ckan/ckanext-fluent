import ckan.plugins as p
from ckan.plugins.toolkit import add_template_directory

from ckanext.fluent import converters



class FluentPlugin(p.SingletonPlugin):
    p.implements(p.IConverters)
    p.implements(p.IConfigurer)

    def update_config(self, config):
        """
        We have some form snippets that support ckanext-scheming
        """
        add_template_directory(config, 'templates')

    def get_converters(self):
        return {
            'fluent_text': converters.fluent_text,
            'fluent_text_output':
                converters.fluent_text_output,
            }
