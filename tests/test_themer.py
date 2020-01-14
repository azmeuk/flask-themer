import pytest
from flask import Flask, url_for
from jinja2 import TemplateNotFound

from flask_themer import (
    Themer,
    EXTENSION_KEY,
    MAGIC_PATH_PREFIX,
    render_template,
    NoThemeResolver,
    ThemerNotInitialized
)


@pytest.fixture
def app():
    app = Flask('testing')
    app.config['SERVER_NAME'] = 'testing'

    Themer(app, loaders=[])

    with app.app_context():
        yield app


def test_jinja_env(app):
    """Ensure that we properly configure the Jinja environment."""
    assert 'theme' in app.jinja_env.globals
    assert 'theme_static' in app.jinja_env.globals


def test_static_path(app):
    """Ensure we can generate a path to a static resource."""
    assert url_for(
        f'{MAGIC_PATH_PREFIX}.static',
        theme='testing',
        filename='testing.static',
        _scheme='http',
        _external=True
    ) == 'http://testing/static/testing/testing.static'


def test_no_resolver(app):
    """Ensure we raise the correct errors when no resolver can be found."""
    with pytest.raises(NoThemeResolver):
        assert render_template('test.html')

    themer = app.extensions[EXTENSION_KEY]
    themer.current_theme_loader(lambda: 'test_theme')

    with pytest.raises(TemplateNotFound):
        assert render_template('test.html')


def test_not_setup():
    """Ensure we provide a useful error when init_app() hasn't been used."""
    app = Flask('testing')
    with app.app_context():
        with pytest.raises(ThemerNotInitialized):
            render_template('test.html')
