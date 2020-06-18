# -*- coding: utf-8 -*-

import functools
import jinja2
import logging
import os
import simplejson
import sys
import werkzeug.utils
import werkzeug.wrappers
try:
    import xlwt
except ImportError:
    xlwt = None

import openerp
import openerp.modules.registry
from openerp.addons.web.controllers.main import Database
from openerp.tools import topological_sort
from openerp import http

from openerp.http import request, serialize_exception as _serialize_exception

_logger = logging.getLogger(__name__)

if hasattr(sys, 'frozen'):
    # When running on compiled windows binary, we don't have access to package loader.
    path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'views'))
    loader = jinja2.FileSystemLoader(path)
else:
    loader = jinja2.PackageLoader('openerp.addons.dimgray_backend_theme_v8', "views")

env = jinja2.Environment(loader=loader, autoescape=True)
env.filters["json"] = simplejson.dumps

# 1 week cache for asset bundles as advised by Google Page Speed
BUNDLE_MAXAGE = 60 * 60 * 24 * 7

#----------------------------------------------------------
# OpenERP Web helpers
#----------------------------------------------------------

db_list = http.db_list

db_monodb = http.db_monodb

def serialize_exception(f):
    @functools.wraps(f)
    def wrap(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception, e:
            _logger.exception("An exception occured during an http request")
            se = _serialize_exception(e)
            error = {
                'code': 200,
                'message': "Odoo Server Error",
                'data': se
            }
            return werkzeug.exceptions.InternalServerError(simplejson.dumps(error))
    return wrap


def module_boot(db=None):
    server_wide_modules = openerp.conf.server_wide_modules or ['web']
    serverside = []
    dbside = []
    for i in server_wide_modules:
        if i in http.addons_manifest:
            serverside.append(i)
    monodb = db or db_monodb()
    if monodb:
        dbside = module_installed_bypass_session(monodb)
        dbside = [i for i in dbside if i not in serverside]
    addons = serverside + dbside
    return addons

def module_installed_bypass_session(dbname):
    loadable = http.addons_manifest.keys()
    modules = {}
    try:
        registry = openerp.modules.registry.RegistryManager.get(dbname)
        with registry.cursor() as cr:
            m = registry.get('ir.module.module')
            # TODO The following code should move to ir.module.module.list_installed_modules()
            domain = [('state','=','installed'), ('name','in', loadable)]
            ids = m.search(cr, 1, [('state','=','installed'), ('name','in', loadable)])
            for module in m.read(cr, 1, ids, ['name', 'dependencies_id']):
                modules[module['name']] = []
                deps = module.get('dependencies_id')
                if deps:
                    deps_read = registry.get('ir.module.module.dependency').read(cr, 1, deps, ['name'])
                    dependencies = [i['name'] for i in deps_read]
                    modules[module['name']] = dependencies
    except:
        pass
    sorted_modules = topological_sort(modules)
    return sorted_modules

class DatabaseBackend(Database):

    @http.route('/web/database/selector', type='http', auth="none")
    def selector(self, **kw):
        try:
            dbs = http.db_list()
            if not dbs:
                return http.local_redirect('/web/database/manager')
        except openerp.exceptions.AccessDenied:
            dbs = False
        return env.get_template("database_selector_backend.html").render({
            'databases': dbs,
            'debug': request.debug,
            'error': kw.get('error')
        })

    @http.route('/web/database/manager', type='http', auth="none")
    def manager(self, **kw):
        print("OKAY")
        # TODO: migrate the webclient's database manager to server side views
        request.session.logout()
        return env.get_template("database_manager_backend.html").render({
            'modules': simplejson.dumps(module_boot()),
        })

