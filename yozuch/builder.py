"""
Blog builder.
"""

import functools
import os
import sys
import jinja2
from yozuch import logger, validator
from yozuch.context import Context
from yozuch.utils import emptydir, import_module, import_module_member, is_external_url


def build(project_dir, config_overrides=None, validate=False, output_dir=None):

    if not os.path.isfile(os.path.join(project_dir, 'config.py')):
        logger.fatal('Unable to find config.py in {}. Wrong project directory?'.format(project_dir))
        sys.exit(1)

    context = Context(config_overrides, project_dir, output_dir)
    _load_theme(context)
    _register_plugins(context)
    _load_sources(context)
    env = _create_template_env(context.theme_path, context.templates_path, context.pages_dir)
    emptydir(context.output_path)

    generators = list(_init_generators(context))

    env.globals['url_for'] = functools.partial(_url_for, generators, context.references)
    env.globals['url_exists_for'] = functools.partial(_url_exists_for, generators)

    _generate_content(context, generators, env, context.output_path)

    if validate:
        validator.validate(context.config, context.output_path)

    logger.info('Done!')

    return context.output_path


def _load_theme(context):
    context.config.update_from_directory(context.theme_path, replace_duplicates=False)
    asset_loader = ('yozuch.loaders.asset.AssetLoader', {'path': os.path.join(context.theme_path, 'assets')})
    context.config['LOADERS'].insert(0, asset_loader)


def _load_sources(context):
    for name, kwargs in context.config['LOADERS']:
        cls = import_module_member(name)
        if cls is None:
            raise LookupError('Unable to find loader with name "{}"'.format(name))
        path = kwargs.pop('path', None)
        loader = cls(**kwargs)
        if path is None:
            path = os.path.join(context.project_path, loader.name)
        if not os.path.isdir(path):
            continue
        sources = list(loader.load(context, path))
        if sources:
            logger.info('Loaded {} {} from {}'.format(len(sources), loader.name, path))
            context.site.setdefault(loader.name, []).extend(sources)


def _register_plugins(context):
    for name in context.config['PLUGINS']:
        mod = import_module(name)
        if mod is None:
            raise LookupError('Unable to find plugin with name "{}"'.format(name))
        mod.register(context)


def _create_template_env(theme_dir, templates_dir, pages_dir):
    loaders = []

    if os.path.isdir(templates_dir):
        loaders.append(jinja2.FileSystemLoader(templates_dir))

    if os.path.isdir(pages_dir):
        loaders.append(jinja2.PrefixLoader({'!pages': jinja2.FileSystemLoader(pages_dir)}))

    theme_loader = jinja2.FileSystemLoader(os.path.join(theme_dir, 'templates'))
    loaders.append(jinja2.PrefixLoader({'!theme': theme_loader}))
    loaders.append(theme_loader)
    loaders.append(jinja2.PackageLoader('yozuch', os.path.join('themes', 'base', 'templates')))

    env = jinja2.Environment(loader=jinja2.ChoiceLoader(loaders))
    return env


def _init_generators(context):
    theme_default_templates = context.config['THEME_DEFAULT_TEMPLATES']
    for route in context.config['VIEWS']:
        url_template, name, generator, kwargs = route
        if 'template' not in kwargs and name in theme_default_templates:
            kwargs['template'] = theme_default_templates[name]
        cls = import_module_member(generator)
        if cls is not None:
            yield cls(url_template, name, **kwargs)
        else:
            raise LookupError('Unable to find generator with name "{}" for url "{}".'.format(generator, url_template))


def _url_template_for(generators, name):
    for gen in generators:
        if gen.name == name:
            return gen.url_template


def _url_for(generators, references, name_or_url, **kwargs):
    if name_or_url in references:
        return references[name_or_url]
    if name_or_url.startswith('/') or is_external_url(name_or_url):
        return name_or_url
    url_template = _url_template_for(generators, name_or_url)
    if url_template is None:
        raise LookupError('Unable to resolve URL for {} {}'.format(name_or_url, kwargs))
    else:
        return url_template.format(**kwargs)


def _url_exists_for(generators, name):
    return _url_template_for(generators, name) is not None


def _generate_content(context, generators, env, output_dir):
    for gen in generators:
        for entry in gen.generate(context):
            if entry.url in context.entries:
                logger.warning('URL {} has been already registered {}'.format(entry.url, context.entries[entry.url]))
            context.entries[entry.url] = entry

    for entry in context.entries.values():
        entry.publish(context)

    logger.info('Writing content...')
    for entry in context.entries.values():
        entry.write(context, env, output_dir)
