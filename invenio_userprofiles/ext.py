# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015, 2016 CERN.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""User profiles module for Invenio."""

from __future__ import absolute_import, print_function

from .api import current_userprofile
from .forms import confirm_register_form_factory, register_form_factory
from .models import UserProfile
from .views import blueprint


class InvenioUserProfiles(object):
    """Invenio-UserProfiles extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        self.init_config(app)

        # Register blueprint for templates
        app.register_blueprint(
            blueprint, url_prefix=app.config['USERPROFILES_PROFILE_URL'])

        # Register current_profile
        app.context_processor(lambda: dict(
            current_userprofile=current_userprofile))

        app.extensions['invenio-userprofiles'] = self

    def init_config(self, app):
        """Initialize configuration."""
        app.config.setdefault('USERPROFILES', True)
        app.config.setdefault('USERPROFILES_EXTEND_SECURITY_FORMS', False)

        app.config.setdefault(
            'USERPROFILES_PROFILE_URL',
            '/account/settings/profile/')

        app.config.setdefault('USERPROFILES_EMAIL_ENABLED', True)

        app.config.setdefault(
            'USERPROFILES_PROFILE_TEMPLATE',
            'invenio_userprofiles/settings/profile.html')

        app.config.setdefault(
            'USERPROFILES_BASE_TEMPLATE',
            app.config.get('BASE_TEMPLATE',
                           'invenio_userprofiles/base.html'))

        app.config.setdefault(
            'USERPROFILES_SETTINGS_TEMPLATE',
            app.config.get('SETTINGS_TEMPLATE',
                           'invenio_userprofiles/settings/base.html'))

        app.config['SECURITY_REGISTER_USER_TEMPLATE'] = \
            'invenio_userprofiles/register_user.html'

        if app.config['USERPROFILES_EXTEND_SECURITY_FORMS']:
            security_ext = app.extensions['security']
            security_ext.confirm_register_form = confirm_register_form_factory(
                security_ext.confirm_register_form)
            security_ext.register_form = register_form_factory(
                security_ext.register_form)
