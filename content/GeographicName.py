# ===========================================================================
# Copyright (c) 2006 by Ancient World Mapping Center, University of North
# Carolina at Chapel Hill, U.S.A.
#
# Generator: ArchGenXML Version 1.5.0
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# About Pleiades
# --------------
#
# Pleiades is an international research network and associated web portal and
# content management system devoted to the study of ancient geography. 
#
# See http://icon.stoa.org/trac/pleiades/wiki.
#
# Funding for the creation of this software was provided by a grant from the 
# U.S. National Endowment for the Humanities (http://www.neh.gov).
# ===========================================================================

__author__ = """Sean Gillies <unknown>, Tom Elliott <unknown>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from Products.PleiadesEntity.config import *

# additional imports from tagged value 'import'
from Products.PleiadesEntity.Extensions.cooking import *

##code-section module-header #fill in your manual code here
##/code-section module-header

copied_fields = {}
copied_fields['title'] = BaseSchema['title'].copy()
copied_fields['title'].widget.label = "Transliterated Name"
schema = Schema((

    copied_fields['title'],
        StringField(
        name='identifier',
        index="FieldIndex",
        widget=StringWidget(
            label="Identifier",
            label_msgid='PleiadesEntity_label_identifier',
            i18n_domain='PleiadesEntity',
        ),
        required=1
    ),

    StringField(
        name='geoNameType',
        index="FieldIndex",
        widget=StringWidget(
            label="Name Type",
            label_msgid='PleiadesEntity_label_geoNameType',
            i18n_domain='PleiadesEntity',
        )
    ),

    StringField(
        name='nameAttested',
        index="FieldIndex",
        widget=StringWidget(
            label="Name as Attested",
            label_msgid='PleiadesEntity_label_nameAttested',
            i18n_domain='PleiadesEntity',
        )
    ),

    StringField(
        name='nameLanguage',
        index="FieldIndex",
        widget=StringWidget(
            label="Language and Writing System of Attested Name",
            label_msgid='PleiadesEntity_label_nameLanguage',
            i18n_domain='PleiadesEntity',
        )
    ),

    LinesField(
        name='timePeriods',
        index="KeywordIndex",
        widget=LinesWidget(
            label="Time Periods",
            label_msgid='PleiadesEntity_label_timePeriods',
            i18n_domain='PleiadesEntity',
        )
    ),

    LinesField(
        name='primaryReferences',
        index="KeywordIndex",
        widget=LinesWidget(
            label="Primary References",
            label_msgid='PleiadesEntity_label_primaryReferences',
            i18n_domain='PleiadesEntity',
        )
    ),

    LinesField(
        name='secondaryReferences',
        index="KeywordIndex",
        widget=LinesWidget(
            label="Secondary References",
            label_msgid='PleiadesEntity_label_secondaryReferences',
            i18n_domain='PleiadesEntity',
        )
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

GeographicName_schema = BaseSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class GeographicName(BaseContent):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(BaseContent,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'Geographic Name'

    meta_type = 'GeographicName'
    portal_type = 'GeographicName'
    allowed_content_types = []
    filter_content_types = 0
    global_allow = 0
    content_icon = 'geoname_icon.gif'
    immediate_view = 'base_view'
    default_view = 'base_view'
    suppl_views = ()
    typeDescription = "A content type for storing information about geographic names as they apply to simple geographic entities (features)."
    typeDescMsgId = 'description_edit_geographicname'

    _at_rename_after_creation = False

    schema = GeographicName_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    security.declarePrivate('at_post_create_script')
    def at_post_create_script(self):
        """
        """

        newID=setIdFromTitle(self)

    security.declarePrivate('at_post_edit_script')
    def at_post_edit_script(self):
        """
        """

        self.at_post_create_script()


registerType(GeographicName, PROJECTNAME)
# end of class GeographicName

##code-section module-footer #fill in your manual code here
##/code-section module-footer


