# -*- coding: utf-8 -*-
#
# File: Temporal.py
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
from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope.interface import implements
import interfaces
from Products.PleiadesEntity.content.TemporalAttestation import TemporalAttestation
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.CompoundField.ArrayField import ArrayField
from Products.CompoundField.ArrayWidget import ArrayWidget
from Products.CompoundField.EnhancedArrayWidget import EnhancedArrayWidget
from Products.CompoundField.EnhancedArrayWidget import EnhancedArrayWidget

from Products.PleiadesEntity.config import *

# additional imports from tagged value 'import'
from Products.CompoundField.CompoundWidget import CompoundWidget

##code-section module-header #fill in your manual code here
from Products.CMFCore import permissions
from Products.PleiadesEntity.time import periodRanges, TimePeriodCmp
from Products.CompoundField.CompoundWidget import CompoundWidget
from Products.CMFCore.utils import getToolByName
##/code-section module-header

schema = Schema((

    ArrayField(
        TemporalAttestation(
            name='attestations',
            widget=CompoundWidget(
                label="Time period and confidence level",
                label_msgid='PleiadesEntity_label_attestations',
                i18n_domain='PleiadesEntity',
            ),
            description="Temporal attestations",
            multiValued=True,
        ),

        widget=EnhancedArrayWidget(
            label="Temporal attestations",
            description="Select time period and level of confidence in attestation",
            macro="pleiadesattestationwidget",
            label_msgid='PleiadesEntity_label_array:attestations',
            description_msgid='PleiadesEntity_help_array:attestations',
            i18n_domain='PleiadesEntity',
        ),
        size=0,
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

Temporal_schema = schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class Temporal(BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.ITemporal)

    _at_rename_after_creation = True

    schema = Temporal_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    security.declareProtected(permissions.View, 'getSortedTemporalAttestations')
    def getSortedTemporalAttestations(self):
        """
        """
        def _cmp(a, b):
            return TimePeriodCmp(self)(a['timePeriod'], b['timePeriod'])
        return sorted(self.getAttestations(), cmp=_cmp)

    security.declareProtected(permissions.View, 'getTimePeriods')
    def getTimePeriods(self):
        """
        """
        return [a['timePeriod'] for a in self.getSortedTemporalAttestations()]

    # Manually created methods

    security.declareProtected(permissions.View, 'displaySortedTemporalAttestations')
    def displaySortedTemporalAttestations(self):
        """
        """
        def _cmp(a, b):
            return TimePeriodCmp(self)(a['timePeriod'], b['timePeriod'])
        attestations = sorted(self.getAttestations(), cmp=_cmp)
        vocab_t = TemporalAttestation.schema[
            'timePeriod'].vocabulary.getVocabularyDict(self)
        vocab_c = TemporalAttestation.schema[
            'confidence'].vocabulary.getVocabularyDict(self)
        try:
            return [dict(timePeriod=vocab_t[a['timePeriod']], confidence=vocab_c[a['confidence']]) for a in attestations]
        except KeyError:
            return []

    def period_vocab(self):
        return TemporalAttestation.schema[
            'timePeriod'].vocabulary.getVocabulary(self).getTarget()
    def confidence_vocab(self):
        return TemporalAttestation.schema[
            'confidence'].vocabulary.getVocabulary(self).getTarget()

    security.declareProtected(permissions.View, 'temporalRange')
    def temporalRange(self, period_vocab=None):
        """Nominal temporal range, not accounting for level of confidence"""
        vocab = period_vocab or self.period_vocab()
        ranges = periodRanges(vocab)
        years = []
        check = self.getAttestations()
        for a in self.getAttestations():
            tp = a['timePeriod']
            if tp:
                years.extend(list(ranges[a['timePeriod']]))
        if len(years) >= 2:
            return min(years), max(years)
        else:
            return None

# end of class Temporal

##code-section module-footer #fill in your manual code here
##/code-section module-footer



