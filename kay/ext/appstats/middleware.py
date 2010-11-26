#!/usr/bin/env python2.5
# -*- coding:utf-8 -*-

"""
AppStatsMiddleware adapted to Kay framework.

:Copyright: (c) 2010 Ian Lewis <ianmlewis@gmail.com>,
:license: BSD, see LICENSE for more details.
"""

class AppStatsMiddleware(object):
  """
  Middleware to enable appstats recording.

  Based off of the the AppstatsDjangoMiddleware in the 
  Appengine SDK
  """

  def process_request(self, request):
    """
    Called by Kay before deciding which view to execute.
    """
    from google.appengine.ext.appstats.recording import start_recording
    start_recording()

  def process_response(self, request, response):
    """
    Stops recording. Optionally sets some extension data for
    FirePython.
    """
    from google.appengine.ext.appstats.recording import end_recording

    firepython_set_extension_data = getattr(
      request,
      'firepython_set_extension_data',
      None)
    end_recording(response.status_code, firepython_set_extension_data)
    return response
