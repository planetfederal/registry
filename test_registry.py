import os
import pytest
import registry


def test_import():
    assert '__version__' in registry.__dict__


def test_default_catalog(client):
    request = client.get('/')
    assert 'default' in request.content


def test_custom_catalog(client):
    request = client.get('/sample')
    assert 'sample' in request.content


if __name__ == '__main__':
    os.environ['DJANGO_SETTINGS_MODULE'] = 'registry'
    pytest.main()
