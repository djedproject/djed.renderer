from pyramid.exceptions import ConfigurationError
from djed.templates.layer import ID_LAYER

from base import BaseTestCase


class TestSettingsError(BaseTestCase):

    _settings = {'djed.templates.custom': 'unknown'}
    _includes = ()

    def test_custom(self):
        self.assertRaises(
            ConfigurationError, self.config.include, 'djed.templates')


class TestSettingsCustom(BaseTestCase):

    _auto_commit = False
    _settings = {'djed.templates.custom': 'djed.templates:tests/bundle/'}

    def test_custom_dir(self):
        self.config.add_layer(
            'dir1', path='djed.templates:tests/dir1/')
        self.config.commit()

        storage = self.registry.get(ID_LAYER)
        self.assertIn('dir1', storage)
        self.assertEqual(2, len(storage['dir1']))
        self.assertEqual('layer_custom', storage['dir1'][0]['name'])
        self.assertEqual('', storage['dir1'][1]['name'])
