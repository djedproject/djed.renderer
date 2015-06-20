from djed.renderer.layer import ID_LAYER

from djed.testing import BaseTestCase


class TestOrder(BaseTestCase):

    _includes = ('djed.renderer', 'pyramid_chameleon')
    _autocommit = False
    _settings = {'djed.renderer.order.test': 'l1 l2 l3'}

    def test_custom_dir(self):
        self.config.add_layer(
            'test', 'l1', path='tests:dir1/')
        self.config.add_layer(
            'test', 'l2', path='tests:bundle/dir1/')
        self.config.commit()

        storage = self.registry.get(ID_LAYER)
        self.assertIn('test', storage)
        self.assertEqual(2, len(storage['test']))
        self.assertEqual('l1', storage['test'][0]['name'])
        self.assertEqual('l2', storage['test'][1]['name'])


class TestOrderUnknown(BaseTestCase):

    _includes = ('djed.renderer', 'pyramid_chameleon')
    _autocommit = False
    _settings = {'djed.renderer.order.test2': 'l1 l2 l3'}

    def test_custom_dir(self):
        self.config.add_layer(
            'test', 'l1', path='tests:dir1/')
        self.config.add_layer(
            'test', 'l2', path='tests:bundle/dir1/')
        self.config.commit()

        storage = self.registry.get(ID_LAYER)
        self.assertIn('test', storage)
        self.assertNotIn('test2', storage)
