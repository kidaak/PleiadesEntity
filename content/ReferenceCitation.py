# -*- coding: utf-8 -*-
#
# File: ReferenceCitation.py
#
# Copyright (c) 2009 by Ancient World Mapping Center, University of North
# Carolina at Chapel Hill, U.S.A.
# Generator: ArchGenXML Version 2.4.1
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """Sean Gillies <unknown>, Tom Elliott <unknown>"""
__docformat__ = 'plaintext'

#ReferenceCitation

from AccessControl import ClassSecurityInfo
from Acquisition import aq_base

from Products.CMFCore.utils import getToolByName

from Products.Archetypes.Field import ObjectField,encode,decode
from Products.Archetypes.Registry import registerField
from Products.Archetypes.utils import DisplayList
from Products.Archetypes import config as atconfig
from Products.Archetypes.Widget import *
from Products.Archetypes.Field  import *
from Products.Archetypes.Schema import Schema
try:
    from Products.generator import i18n
except ImportError:
    from Products.Archetypes.generator import i18n

from Products.PleiadesEntity import config

##code-section module-header #fill in your manual code here
##/code-section module-header

from zope.interface import implements

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin


from Products.CMFCore import permissions

from Products.CompoundField.CompoundField import CompoundField
######CompoundField
schema = Schema((

    StringField(
        name='identifier',
        widget=StringField._properties['widget'](
            macro="url_widget",
            label="Reference identifier",
            description="Enter unique identifier for reference work",
            label_msgid='PleiadesEntity_label_identifier',
            description_msgid='PleiadesEntity_help_identifier',
            i18n_domain='PleiadesEntity',
        ),
    ),
    StringField(
        name='range',
        widget=StringField._properties['widget'](
            label="Specific citation",
            description="Enter specific range of citation",
            label_msgid='PleiadesEntity_label_range',
            description_msgid='PleiadesEntity_help_range',
            i18n_domain='PleiadesEntity',
        ),
    ),

),
)




class ReferenceCitation(CompoundField):
    """
    """
    ##code-section class-header #fill in your manual code here
    ##/code-section class-header



    _properties = CompoundField._properties.copy()
    _properties.update({
        'type': 'referencecitation',
        ##code-section field-properties #fill in your manual code here
        ##/code-section field-properties

        })

    security  = ClassSecurityInfo()

    schema=schema

    security.declarePrivate('set')
    security.declarePrivate('get')


    def getRaw(self, instance, **kwargs):
        return CompoundField.getRaw(self, instance, **kwargs)

    def SearchableText(self,):
        return 'foobar'

    def set(self, instance, value, **kwargs):
        return CompoundField.set(self, instance, value, **kwargs)

    def get(self, instance, **kwargs):
        return CompoundField.get(self, instance, **kwargs)


registerField(ReferenceCitation,
              title='ReferenceCitation',
              description='')

##code-section module-footer #fill in your manual code here
##/code-section module-footer


