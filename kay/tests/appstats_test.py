# -*- coding: utf-8 -*-


from werkzeug import (
  BaseResponse, Client, Request
)

from kay.app import get_application
from kay.conf import LazySettings
from kay.ext.testutils.gae_test_base import GAETestBase
from kay.ext.appstats.middleware import AppStatsMiddleware

class AppStatsMiddlewareTestCase(GAETestBase):
  KIND_NAME_UNSWAPPED = False
  USE_PRODUCTION_STUBS = True
  CLEANUP_USED_KIND = True

  def setUp(self):
    s = LazySettings(settings_module='kay.tests.appstats_settings')
    app = get_application(settings=s)
    self.client = Client(app, BaseResponse)

  def tearDown(self):
    pass

  def test_appstats_middleware(self):
    from google.appengine.api import apiproxy_stub_map

    request = Request({})
    middleware = AppStatsMiddleware()

    r = middleware.process_request(request)
    self.assertTrue(r is None)

    r = middleware.process_response(request, BaseResponse("", 200))
    self.assertTrue(isinstance(r, BaseResponse))

    memcache = apiproxy_stub_map.apiproxy._APIProxyStubMap__stub_map['memcache']._the_cache
    self.assertTrue('__appstats__' in memcache)

  def test_appstats_middleware_request(self):
    from google.appengine.api import apiproxy_stub_map
    response = self.client.get('/no_decorator')
    memcache = apiproxy_stub_map.apiproxy._APIProxyStubMap__stub_map['memcache']._the_cache
    self.assertTrue('__appstats__' in memcache)
