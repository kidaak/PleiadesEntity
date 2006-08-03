# -*- coding: utf-8 -*-
#
# File: GeographicNameLite.py
#
# Copyright (c) 2006 by Tom Elliott and Sean Gillies
# Generator: ArchGenXML Version 1.5.0 svn/devel
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#

__author__ = """Tom Elliott and Sean Gillies <maia@unc.edu>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from Products.ATVocabularyManager.namedvocabulary import NamedVocabulary
from Products.GeographicEntityLite.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    StringField(
        name='nameString',
        widget=StringWidget(
            label='Namestring',
            label_msgid='GeographicEntityLite_label_nameString',
            i18n_domain='GeographicEntityLite',
        )
    ),

    BooleanField(
        name='modern',
        default="0",
        widget=BooleanWidget(
            label='Modern',
            label_msgid='GeographicEntityLite_label_modern',
            i18n_domain='GeographicEntityLite',
        )
    ),

    StringField(
        name='language',
        widget=SelectionWidget(
            label='Language',
            label_msgid='GeographicEntityLite_label_language',
            i18n_domain='GeographicEntityLite',
        ),
        vocabulary=NamedVocabulary("""nameLanguages""")
    ),

    StringField(
        name='script',
        widget=SelectionWidget(
            label='Script',
            label_msgid='GeographicEntityLite_label_script',
            i18n_domain='GeographicEntityLite',
        ),
        vocabulary=NamedVocabulary("""nameScript""")
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

GeographicNameLite_schema = BaseSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class GeographicNameLite(BaseContent):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(BaseContent,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'GeographicNameLite'

    meta_type = 'GeographicNameLite'
    portal_type = 'GeographicNameLite'
    allowed_content_types = []
    filter_content_types = 0
    global_allow = 0
    #content_icon = 'GeographicNameLite.gif'
    immediate_view = 'base_view'
    default_view = 'base_view'
    suppl_views = ()
    typeDescription = "GeographicNameLite"
    typeDescMsgId = 'description_edit_geographicnamelite'

    _at_rename_after_creation = True

    schema = GeographicNameLite_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

registerType(GeographicNameLite, PROJECTNAME)
# end of class GeographicNameLite

##code-section module-footer #fill in your manual code here
##/code-section module-footer



