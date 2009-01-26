# -*- coding: utf-8 -*-
#
# File: Place.py
#
# Copyright (c) 2008 by Ancient World Mapping Center, University of North
# Carolina at Chapel Hill, U.S.A.
# Generator: ArchGenXML Version 2.1
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """Sean Gillies <unknown>, Tom Elliott <unknown>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope.interface import implements
import interfaces

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import \
    ReferenceBrowserWidget
from Products.PleiadesEntity.config import *

##code-section module-header #fill in your manual code here
from Products.CMFCore import permissions
from Products.PleiadesEntity.time import TimePeriodCmp
##/code-section module-header

schema = Schema((

    StringField(
        name='title',
        required=1,
        searchable=1,
        default='',
        accessor='Title',
        widget=StringWidget(
            label_msgid='label_title',
            visible={'view' : 'invisible'},
            i18n_domain='plone',
            macro='rdfa_name_widget'
        ),
    ),
    
    StringField(
        name='modernLocation',
        widget=StringField._properties['widget'](
            label="Modern Location",
            description="The modern location or vicinity of the ancient place",
            label_msgid='PleiadesEntity_label_modernLocation',
            description_msgid='PleiadesEntity_help_modernLocation',
            i18n_domain='PleiadesEntity',
        ),
    ),
    TextField(
        name='content',
        widget=RichWidget(
            label="Content",
            description="About the place",
            label_msgid='PleiadesEntity_label_content',
            description_msgid='PleiadesEntity_help_content',
            i18n_domain='PleiadesEntity',
        ),
    ),
    ReferenceField(
        name='features',
        widget=ReferenceBrowserWidget(
            label='Features',
            label_msgid='PleiadesEntity_label_features',
            i18n_domain='PleiadesEntity',
        ),
        allowed_types=('Feature',),
        multiValued=1,
        relationship='hasFeature',
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

Place_schema = BaseSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class Place(BaseContent, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IPlace)

    meta_type = 'Place'
    _at_rename_after_creation = False

    schema = Place_schema

    ##code-section class-header #fill in your manual code here
    schema["features"].widget.visible = {"edit": "visible", "view": "invisible"}
    ##/code-section class-header

    # Methods

    security.declareProtected(permissions.View, 'Title')
    def Title(self):
        """
        """
        t = self.getField('title').get(self)
        if t:
            return t
        if not t:
            return self.get_title()

    security.declareProtected(permissions.View, 'get_title')
    def get_title(self):
        titles = []
        types = []
        for o in self.getFeatures():
            try:
                name = o.getRefs('hasName')[0]
                titles.append(name.Title())
                types.append(name.getNameType())
            except:
                pass
        if len(titles) == 0:
            return 'Unnamed Place'
        else:
            return '/'.join([t for t in titles if t])
    
    security.declareProtected(permissions.View, 'getTimePeriods')
    def getTimePeriods(self):
        """
        """
        result = []
        for o in self.getFeatures():
            for t in o.getTimePeriods():
                if t not in result:
                    result.append(t)
        return sorted(result, cmp=TimePeriodCmp(self))

    security.declareProtected(permissions.View, 'getPlaceType')
    def getPlaceType(self):
        """
        """
        result = []
        for o in self.getFeatures():
            t = o.getFeatureType()
            if t not in result:
                result.append(t)
        return result

    # Manually created methods

    security.declareProtected(permissions.View, 'getFeatureType')
    def getFeatureType(self):
        """
        """
        result = []
        for o in self.getFeatures():
            t = o.getFeatureType()
            if t not in result:
                result.append(t)
        return result

    security.declareProtected(permissions.View, 'getFeatures')
    def getFeatures(self):
        for o in self.getRefs('hasFeature'):
            if interfaces.IFeature.providedBy(o):
                yield o

    security.declareProtected(permissions.View, 'featuresByLocation')
    def featuresByLocation(self):
        """
        """
        d = {}
        for f in self.getFeatures():
            for l in f.getLocations():
                lid = l.getId()
                if lid not in d:
                    d[lid] = dict(
                        url=l.absolute_url(), 
                        title=l.pretty_title_or_id(), 
                        features=[]
                        )
                d[lid]['features'].append(
                    dict(title=f.pretty_title_or_id(), url=f.absolute_url())
                    )
        return d


registerType(Place, PROJECTNAME)
# end of class Place

##code-section module-footer #fill in your manual code here
##/code-section module-footer



