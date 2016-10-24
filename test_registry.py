import pytest
import random
import rawes
import registry
import requests
import time
from pycsw.core import config
from pycsw.core.admin import delete_records
from pycsw.core.etree import etree


get_records_url = '?service=CSW&version=2.0.2&request=' \
                  'GetRecords&typenames=csw:Record&elementsetname=full' \


search_url = '%s/_search' % (registry.REGISTRY_SEARCH_URL)


@pytest.mark.skip(reason='')
def get_xml_block():
    identifier = random.randint(1e6, 1e7)
    lower_corner_1 = random.uniform(-90, 0)
    lower_corner_2 = random.uniform(-180, 0)
    upper_corner_1 = random.uniform(0, 90)
    upper_corner_2 = random.uniform(0, 180)
    xml_block = (
        '  <csw:Record>\n'
        '    <dc:identifier>%d</dc:identifier>\n'
        '    <dc:title>acus netus eleifend facilisis enim leo sollicitudin '
        'metus ad erat quisque</dc:title>\n'
        '    <dct:alternative>Fames magna sed.</dct:alternative>\n'
        '    <dct:modified>2016-08-24T23:54:58Z</dct:modified>\n'
        '    <dct:abstract>Augue purus vehicula ridiculus eu donec et eget '
        'sit justo. Fames dolor ipsum dignissim aliquet. Proin massa congue '
        'lorem tortor facilisis feugiat vitae ut. Purus justo cum arcu '
        'nascetur etiam hymenaeos volutpat amet. Lacus curae cras quam eni '
        'mi odio purus venenatis massa a elit parturient. Porta lacus '
        'lacinia lectus ad semper sociosqu. Augue neque vel. Neque fusce a'
        'ante ipsum sem ornare fames nisl fames curabitur auctor. Dolor '
        'class praesent curabitur id venenatis potenti auctor dis nec. '
        'Massa magna semper eu bibendum amet. Velit fusce rhoncus ultrices '
        'commodo cras enim curabitur. Proin vitae mus ante luctus ut orci '
        'sociosqu nonummy integer nisi a proin. Justo augue libero. Felis '
        'massa potenti. Fusce dolor iaculis tempor eu. Massa velit. Risus '
        'metus enim molestie sed pede a amet parturient facilisis '
        'scelerisque dui nibh.</dct:abstract>\n'
        '    <dc:type>dataset</dc:type>\n'
        '    <dc:format>ESRI:ArcGIS:MapServer</dc:format>\n'
        '    <dc:source>http://water.discomap.eea.europa.eu/arcgis/rest/'
        'services/Noise/2007_NOISE_END_LAEA_Contours/MapServer/?f=json'
        '</dc:source>\n'
        '    <dc:relation>%d</dc:relation>\n'
        '    <dct:references scheme="ESRI:ArcGIS:MapServer">http://water.'
        'discomap.eea.europa.eu/arcgis/rest/services/Noise/2007_NOISE_END_'
        'LAEA_Contours/MapServer/?f=json</dct:references>\n'
        '    <dct:references scheme="WWW:LINK">http://localhost:8000/layer'
        '/%d/</dct:references>\n'
        '    <ows:BoundingBox crs="http://www.opengis.net/def/crs/EPSG/0/'
        '4326" dimensions="2">\n'
        '        <ows:LowerCorner>%4f %4f</ows:LowerCorner>\n'
        '        <ows:UpperCorner>%4f %4f</ows:UpperCorner>\n'
        '    </ows:BoundingBox>\n'
        '    </csw:Record>\n'
    ) % (identifier, identifier, identifier, lower_corner_1, lower_corner_2,
         upper_corner_1, upper_corner_2)

    return xml_block


@pytest.mark.skip(reason='')
def construct_payload(records_number=1):
    xml_string = (
        '<csw:Transaction xmlns:csw="http://www.opengis.net/cat/csw/2.0.2" '
        'xmlns:ows="http://www.opengis.net/ows" '
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
        'xsi:schemaLocation="http://www.opengis.net/cat/csw/2.0.2 '
        'http://schemas.opengis.net/csw/2.0.2/CSW-publication.xsd" '
        'service="CSW" version="2.0.2" xmlns:dc="http://purl.org/dc/'
        'elements/1.1/" xmlns:dct="http://purl.org/dc/terms/" '
        'xmlns:registry="http://gis.harvard.edu/HHypermap/registry/0.1" >\n'
        '<csw:Insert>\n'
    )

    end_part = ('  </csw:Insert>\n'
                '</csw:Transaction>')

    for i in range(records_number):
        xml_block = get_xml_block()
        xml_string += xml_block

    xml_string += end_part
    return xml_string


@pytest.mark.skip(reason='')
def get_number_records(request):
    parsed = etree.fromstring(request.content,
                              etree.XMLParser(resolve_entities=False))
    search_param = '{http://www.opengis.net/cat/csw/2.0.2}SearchResults'
    search_results = parsed.findall(search_param)[0]

    return int(search_results.attrib['numberOfRecordsMatched'])


@pytest.yield_fixture(autouse=True)
def clear_records():
    '''
    Function that clears records for both database and search backend.
    '''
    registry.REGISTRY_INDEX_NAME = 'test'
    context = config.StaticContext()
    delete_records(context,
                   registry.PYCSW['repository']['database'],
                   registry.PYCSW['repository']['table'])
    yield
    es_client = rawes.Elastic(registry.REGISTRY_SEARCH_URL)
    es_client.delete(registry.REGISTRY_INDEX_NAME)
    delete_records(context,
                   registry.PYCSW['repository']['database'],
                   registry.PYCSW['repository']['table'])


def test_single_transaction(client):
    '''
    Test single csw transaction.
    '''
    payload = construct_payload()
    response = client.post('/', payload, content_type='text/xml')
    assert 200 == response.status_code

    response = client.get(get_records_url)
    number_records_matched = get_number_records(response)
    assert 200 == response.status_code
    assert 1 == number_records_matched

    # Give backend some time.
    time.sleep(1)

    search_response = requests.get(search_url)
    search_response = search_response.json()
    assert 'hits' in search_response
    assert 'total' in search_response['hits']
    assert 1 == search_response['hits']['total']


def test_multiple_transactions(client):
    '''
    Test multiple csw transactions.
    '''
    records_number = 10
    payload = construct_payload(records_number=records_number)

    response = client.post('/', payload, content_type='text/xml')
    assert 200 == response.status_code

    response = client.get(get_records_url)
    number_records_matched = get_number_records(response)
    assert 200 == response.status_code
    assert records_number == number_records_matched

    # Give backend some time.
    time.sleep(5)

    search_response = requests.get(search_url)
    search_response = search_response.json()
    assert 'hits' in search_response
    assert 'total' in search_response['hits']
    assert records_number == search_response['hits']['total']


if __name__ == '__main__':
    pytest.main()
