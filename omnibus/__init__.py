import pkg_resources
default_app_config = 'omnibus.apps.omnibusAppConfig'
VERSION = pkg_resources.get_distribution('django_omnibus').version
