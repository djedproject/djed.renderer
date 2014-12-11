from unittest import mock
from pyramid.exceptions import ConfigurationError
from pyramid.exceptions import ConfigurationConflictError

from base import BaseTestCase


class TestLayerDirective(BaseTestCase):

    _includes = ()

    def test_layer_directive(self):
        self.assertFalse(hasattr(self.config, 'add_layer'))
        self.assertFalse(hasattr(self.config, 'add_layers'))
        self.assertFalse(hasattr(self.config, 'add_template_filter'))
        self.config.include('djed.templates')

        self.assertTrue(hasattr(self.config, 'add_layer'))
        self.assertTrue(hasattr(self.config, 'add_layers'))
        self.assertTrue(hasattr(self.config, 'add_template_filter'))


class TestLayer(BaseTestCase):

    _auto_commit = False

    def test_layer_registration(self):
        from djed.templates.layer import ID_LAYER

        self.config.add_layer(
            'test', path='djed.templates:tests/dir1/')
        self.config.commit()

        data = self.registry.get(ID_LAYER)
        self.assertIn('test', data)
        self.assertEqual(len(data['test']), 1)
        self.assertEqual(data['test'][0]['name'], '')
        self.assertTrue(data['test'][0]['path'].endswith(
            'djed/templates/tests/dir1/'))

    def test_layer_path_required(self):
        self.assertRaises(
            ConfigurationError, self.config.add_layer, 'test')

    def test_multple_layer_registration(self):
        from djed.templates.layer import ID_LAYER

        self.config.add_layer(
            'test', path='djed.templates:tests/dir1/')
        self.config.commit()

        self.config.add_layer(
            'test', 'custom', path='djed.templates:tests/bundle/dir1/')
        self.config.commit()

        data = self.registry.get(ID_LAYER)
        self.assertIn('test', data)
        self.assertEqual(len(data['test']), 2)
        self.assertEqual(data['test'][0]['name'], 'custom')
        self.assertTrue(data['test'][0]['path'].endswith(
            'djed/templates/tests/bundle/dir1/'))
        self.assertEqual(data['test'][1]['name'], '')
        self.assertTrue(data['test'][1]['path'].endswith(
            'djed/templates/tests/dir1/'))

    def test_register_layers(self):
        from djed.templates.layer import ID_LAYER

        self.config.add_layers(
            'custom', path='djed.templates:tests/bundle/')
        self.config.commit()

        data = self.registry.get(ID_LAYER)
        self.assertIn('dir1', data)
        self.assertEqual(len(data['dir1']), 1)
        self.assertEqual(data['dir1'][0]['name'], 'custom')
        self.assertTrue(data['dir1'][0]['path'].endswith(
            'djed/templates/tests/bundle/dir1'))

    def test_reg_conflict(self):
        self.config.commit()

        self.config.add_layer(
            'test', path='djed.templates:tests/dir1/')
        self.config.add_layer(
            'test', path='djed.templates:tests/bundle/dir1/')

        self.assertRaises(
            ConfigurationConflictError, self.config.commit)


class TestTemplateFilter(BaseTestCase):

    def test_add_template_filter_err(self):
        def _filter(context, request):
            return {}

        self.assertRaises(
            ConfigurationError,
            self.config.add_template_filter, 'test:view', _filter)

    @mock.patch('djed.templates.layer.venusian')
    def test_add_template_filter_deco_err(self, m_venusian):
        import djed.templates

        @djed.templates.template_filter('test:view')
        def _filter(context, request):
            return {}

        wrp, cb = m_venusian.attach.call_args[0]

        self.assertIs(wrp, _filter)

        m_venusian.config.with_package.return_value = self.config
        self.assertRaises(
            ConfigurationError, cb, m_venusian, 't', _filter)

    def test_add_template_filter(self):
        from djed.templates.layer import ID_LAYER

        self.config.add_layer(
            'test', path='djed.templates:tests/dir1/')
        self.config.add_layer(
            'test', 'custom', path='djed.templates:tests/bundle/dir1/')

        def _filter(context, request):
            return {}

        self.config.add_template_filter('test:view', _filter)

        data = self.registry.get(ID_LAYER)
        self.assertIn('test', data)
        self.assertEqual(len(data['test']), 2)
        self.assertEqual(data['test'][1]['name'], '')
        self.assertIs(_filter, data['test'][1]['filters']['view'])
