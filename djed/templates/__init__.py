from djed.templates.layer import template_filter
from djed.templates.renderer import render
from djed.templates.renderer import RendererNotFound

def includeme(config):
    import os
    from pyramid.path import AssetResolver
    from pyramid.settings import aslist
    from pyramid.exceptions import ConfigurationError

    from djed.templates.renderer import lt_renderer_factory
    from djed.templates.layer import add_layer, add_layers, change_layers_order
    from djed.templates.layer import add_template_filter


    # config directives
    config.add_directive('add_layer', add_layer)
    config.add_directive('add_layers', add_layers)
    config.add_directive('add_template_filter', add_template_filter)

    # request.render_tmpl
    config.add_request_method(render, 'render_template')

    # renderer factory
    config.add_renderer('.lt', lt_renderer_factory)

    # order
    settings = config.get_settings()

    order = {}
    for key, val in settings.items():
        if key.startswith('djed.templates.order.'):
            layer = key[21:]
            order[layer] = [s.strip() for s in aslist(val)]

    if order:
        config.action(
            'djed.templates.order',
            change_layers_order, (config, order), order=999999+1)

    # global custom layer
    custom = settings.get('djed.templates.custom', '').strip()
    if custom:
        resolver = AssetResolver()
        directory = resolver.resolve(custom).abspath()
        if not os.path.isdir(directory):
            raise ConfigurationError(
                "Directory is required for layer.custom setting: %s"%custom)

        config.action(
            'djed.templates.custom',
            add_layers, (config, 'layer_custom', custom), order=999999+2)
