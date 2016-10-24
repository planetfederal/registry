import os
import rawes
import sys
import getopt
from django.conf import settings
from django.core import management
from django.conf.urls import url
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from distutils.util import strtobool

from pycsw import server
from pycsw.core import config
from pycsw.core import admin as pycsw_admin
from pycsw.core.repository import Repository
from pycsw.core.util import wkt2geom

from shapely.geometry import box

from rawes.elastic_exception import ElasticException

__version__ = 0.1

DEBUG = strtobool(os.getenv('REGISTRY_DEBUG', 'True'))
ROOT_URLCONF = 'registry'
DATABASES = {'default': {}}  # required regardless of actual usage
SECRET_KEY = os.getenv('REGISTRY_SECRET_KEY', 'Make sure you create a good secret key.')

REGISTRY_INDEX_NAME = os.getenv('REGISTRY_INDEX_NAME', 'registry')
REGISTRY_MAPPING_PRECISION = os.getenv('REGISTRY_MAPPING_PRECISION', '500m')
REGISTRY_SEARCH_URL = os.getenv('REGISTRY_SEARCH_URL', 'http://127.0.0.1:9200')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
         'console': {
            'class': 'logging.StreamHandler',
         },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': True,
        },
        'pycsw': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

if not settings.configured:
    settings.configure(**locals())

PYCSW = {
        'repository': {
          'source': 'registry.RegistryRepository',
          'mappings': 'registry',
          'database': 'sqlite:////tmp/registry.db',
          'table': 'records',
        },
        'server': {
            'maxrecords': '100',
            'pretty_print': 'true',
            'domaincounts': 'true',
            'encoding': 'UTF-8',
            'profiles': 'apiso',
            'home': '.',
        },
        'metadata:main': {
            'identification_title': 'Registry',
            'identification_abstract': 'Registry is a CSW catalogue with faceting capabilities via OpenSearch',
            'identification_keywords': 'registry, pycsw',
            'identification_keywords_type': 'theme',
            'identification_fees': 'None',
            'identification_accessconstraints': 'None',
            'provider_name': 'Organization Name',
            'provider_url': '',
            'contact_name': 'Lastname, Firstname',
            'contact_position': 'Position Title',
            'contact_address': 'Mailing Address',
            'contact_city': 'City',
            'contact_stateorprovince': 'Administrative Area',
            'contact_postalcode': 'Zip or Postal Code',
            'contact_country': 'Country',
            'contact_phone': '+xx-xxx-xxx-xxxx',
            'contact_fax': '+xx-xxx-xxx-xxxx',
            'contact_email': 'Email Address',
            'contact_url': 'Contact URL',
            'contact_hours': 'Hours of Service',
            'contact_instructions': 'During hours of service. Off on weekends.',
            'contact_role': 'pointOfContact',
        },
        'manager': {
            'transactions': 'true',
            'allowed_ips': os.getenv('REGISTRY_ALLOWED_IPS', '*'),
        },
}

MD_CORE_MODEL = {
    'typename': 'pycsw:CoreMetadata',
    'outputschema': 'http://pycsw.org/metadata',
    'mappings': {
        'pycsw:Identifier': 'identifier',
        'pycsw:Typename': 'typename',
        'pycsw:Schema': 'schema',
        'pycsw:MdSource': 'mdsource',
        'pycsw:InsertDate': 'insert_date',
        'pycsw:XML': 'xml',
        'pycsw:AnyText': 'anytext',
        'pycsw:Language': 'language',
        'pycsw:Title': 'title',
        'pycsw:Abstract': 'abstract',
        'pycsw:Keywords': 'keywords',
        'pycsw:KeywordType': 'keywordstype',
        'pycsw:Format': 'format',
        'pycsw:Source': 'source',
        'pycsw:Date': 'date',
        'pycsw:Modified': 'date_modified',
        'pycsw:Type': 'type',
        'pycsw:BoundingBox': 'wkt_geometry',
        'pycsw:CRS': 'crs',
        'pycsw:AlternateTitle': 'title_alternate',
        'pycsw:RevisionDate': 'date_revision',
        'pycsw:CreationDate': 'date_creation',
        'pycsw:PublicationDate': 'date_publication',
        'pycsw:OrganizationName': 'organization',
        'pycsw:SecurityConstraints': 'securityconstraints',
        'pycsw:ParentIdentifier': 'parentidentifier',
        'pycsw:TopicCategory': 'topicategory',
        'pycsw:ResourceLanguage': 'resourcelanguage',
        'pycsw:GeographicDescriptionCode': 'geodescode',
        'pycsw:Denominator': 'denominator',
        'pycsw:DistanceValue': 'distancevalue',
        'pycsw:DistanceUOM': 'distanceuom',
        'pycsw:TempExtent_begin': 'time_begin',
        'pycsw:TempExtent_end': 'time_end',
        'pycsw:ServiceType': 'servicetype',
        'pycsw:ServiceTypeVersion': 'servicetypeversion',
        'pycsw:Operation': 'operation',
        'pycsw:CouplingType': 'couplingtype',
        'pycsw:OperatesOn': 'operateson',
        'pycsw:OperatesOnIdentifier': 'operatesonidentifier',
        'pycsw:OperatesOnName': 'operatesoname',
        'pycsw:Degree': 'degree',
        'pycsw:AccessConstraints': 'accessconstraints',
        'pycsw:OtherConstraints': 'otherconstraints',
        'pycsw:Classification': 'classification',
        'pycsw:ConditionApplyingToAccessAndUse': 'conditionapplyingtoaccessanduse',
        'pycsw:Lineage': 'lineage',
        'pycsw:ResponsiblePartyRole': 'responsiblepartyrole',
        'pycsw:SpecificationTitle': 'specificationtitle',
        'pycsw:SpecificationDate': 'specificationdate',
        'pycsw:SpecificationDateType': 'specificationdatetype',
        'pycsw:Creator': 'creator',
        'pycsw:Publisher': 'publisher',
        'pycsw:Contributor': 'contributor',
        'pycsw:Relation': 'relation',
        'pycsw:Links': 'links',
    }
}

# TODO: make registry work using CSRF cookie.
@method_decorator(csrf_exempt, name='dispatch')
def csw_view(request, catalog=None):
    """CSW dispatch view.
       Wraps the WSGI call and allows us to tweak any django settings.
    """
    env = request.META.copy()
    env.update({'local.app_root': os.path.dirname(__file__),
                'REQUEST_URI': request.build_absolute_uri()})

    # pycsw prefers absolute urls, let's get them from the request.
    url = request.build_absolute_uri()
    PYCSW['server']['url'] = url
    PYCSW['metadata:main']['provider_url'] = url

    csw = server.Csw(PYCSW, env)
    status, content = csw.dispatch_wsgi()
    status_code = int(status[0:3])
    response = HttpResponse(content,
                            content_type=csw.contenttype,
                            status=status_code,
                            )

    return response


def record_to_dict(record):
    #TODO: check for correct order.
    bbox = wkt2geom(record.wkt_geometry)
    min_x, min_y, max_x, max_y = bbox[0], bbox[1], bbox[2], bbox[3]
    record_dict = {
        'title': record.title,
        'abstract': record.abstract,
        'bbox': bbox,
        'min_x': min_x,
        'min_y': min_y,
        'max_x': max_x,
        'max_y': max_y,
        # 'rectangle': box(min_x, min_y, max_x, max_y),
        'layer_geoshape': {
            'type': 'envelope',
            'coordinates': [
                [min_x, max_y], [max_x, min_y]
            ]
        }
    }

    return record_dict

class RegistryRepository(Repository):
    def __init__(self, *args, **kwargs):

        es =  rawes.Elastic(REGISTRY_SEARCH_URL)
        try:
            es.get(REGISTRY_INDEX_NAME)
        except ElasticException as e:
            mapping = {
                "mappings": {
                    "layer": {
                        "properties": {
                            "layer_geoshape": {
                                "type": "geo_shape",
                                "tree": "quadtree",
                                "precision": REGISTRY_MAPPING_PRECISION
                            }
                        }
                    }
                }
            }
            es.put(REGISTRY_INDEX_NAME, data=mapping)
        self.es = es

        database = PYCSW['repository']['database']
        return super(RegistryRepository, self).__init__(database, context=config.StaticContext())

    def insert(self, *args, **kwargs):
        record = args[0]
        es_dict = record_to_dict(record)
        self.es[REGISTRY_INDEX_NAME]['layer'].post(data=es_dict)
        super(RegistryRepository, self).insert(*args)


urlpatterns = [
    url(r'^$', csw_view),
    url(r'^(?P<catalog>\w+)?$', csw_view),
]


if __name__ == '__main__':  # pragma: no cover
    COMMAND = None
    os.environ['DJANGO_SETTINGS_MODULE'] = 'registry'

    if 'pycsw' in sys.argv[:2]:

        OPTS, ARGS = getopt.getopt(sys.argv[2:], 'c:f:ho:p:ru:x:s:t:y')

        for o, a in OPTS:
            if o == '-c':
                COMMAND = a

        database = PYCSW['repository']['database']
        table = PYCSW['repository']['table']
        home = PYCSW['server']['home']

        available_commands = ['setup_db', 'get_sysprof']

        if COMMAND not in available_commands:
            print('pycsw supports only the following commands: %s' % available_commands)
            sys.exit(1)

        if COMMAND == 'setup_db':
            pycsw_admin.setup_db(database, table, home)

        elif COMMAND == 'get_sysprof':
            print(pycsw_admin.get_sysprof())

        sys.exit(0)

    management.execute_from_command_line()
