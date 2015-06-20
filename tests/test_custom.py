from pyramid.exceptions import ConfigurationError
from djed.renderer.layer import ID_LAYER

from djed.testing import BaseTestCase


class TestSettingsError(BaseTestCase):

    _settings = {'djed.renderer.custom': 'unknown'}
    _includes = ()

    def test_custom(self):
        self.assertRaises(
            ConfigurationError, self.config.include, 'djed.renderer')


class TestSettingsCustom(BaseTestCase):

    _includes = ('djed.renderer', 'pyramid_chameleon')
    _autocommit = False
    _settings = {'djed.renderer.custom': 'tests:bundle'}

    def test_custom_dir(self):
        self.config.add_layer(
            'dir1', path='tests:dir1/')
        self.config.commit()

        storage = self.registry.get(ID_LAYER)

        for k, v in storage.items():
            for i in v:
                print(i.__dict__)
        self.assertIn('dir1', storage)
        self.assertEqual(2, len(storage['dir1']))
        self.assertEqual('layer_custom', storage['dir1'][0]['name'])
        self.assertEqual('', storage['dir1'][1]['name'])
