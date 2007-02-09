# ===========================================================================
# Copyright (C) 2006 Ancient World Mapping Center
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

import glob
import sys
import re
from os.path import basename

import lxml.etree as etree

from Products.CMFCore.utils import getToolByName

from Products.PleiadesEntity.Extensions.xmlutil import *
from Products.PleiadesEntity.Extensions.cooking import *


class EntityLoadError(Exception):
    pass


def format_listofstrings(list):
    """convert ['x', 'y', 'z'] to u'x, y, and z'"""
    
    try:
        length = len(list)
    except:
        length = 0
    out = u''
    if length == 0:
        pass
    elif length < 3:
        out = unicode(' and '.join(list))
    else:
        out = unicode(', '.join(list[:-1]))
        out = unicode(' and '.join([out, list[-1]]))
    return out
   
def initialize(self):
    """Setup the places, names, and locations containers."""
    lpf = self.portal_types['Large Plone Folder']
    lpf_allow = lpf.global_allow
    lpf.global_allow = True

    n = self.portal_types['GeographicName']
    n_allow = n.global_allow
    n.global_allow = True

    n = self.portal_types['EthnicName']
    n_allow = n.global_allow
    n.global_allow = True

    self.invokeFactory('Large Plone Folder', id='names', title='Pleiades Names')
    self.invokeFactory('LocationContainer', id='locations', title='Pleiades Locations')
    self.invokeFactory('PlaceContainer', id='places', title='Pleiades Places')

def loaden(self, sourcedir):
    """Attempt to load all XML files in the specified source directory.
    Files which can not be loaded are reported."""
    failures = []
    count = 0
    for xml in glob.glob("%s/*.xml" % sourcedir):
        try:
            load_place(self, xml)
            count += 1
        except Exception, e:
            failures.append([basename(xml), str(e)])
    if len(failures) == 0:
        return "Loaded %d of %d files." % (count, count)
    else:
        msg = "Loaded %d of %d files. Failures:\n" % (count, count + len(failures))
        for f in failures:
            msg += "%s\n" % str(f)
        return msg
    
AWMC = "http://www.unc.edu/awmc/gazetteer/schemata/ns/0.3"
ADLGAZ = "http://www.alexandria.ucsb.edu/gazetteer/ContentStandard/version3.2/"
GEORSS = "http://www.georss.org/georss"
DC = "http://purl.org/dc/elements/1.1/"

import sys

def load_place(site, file):
    """Create a new Place in plonefolder and populate it with
    the data found in the xml file at sourcepath."""

    root = etree.parse(file).getroot()
    ptool = getToolByName(site, 'plone_utils')

    places = site.places
    names = site.names
    locations = site.locations

    # Place
    pid = places.invokeFactory('Place')
    p = getattr(places, pid)
    
    # modern location
    e = root.findall("{%s}modernLocation" % AWMC)
    if e:
        p.setModernLocation(e[0].text)
    
    e = root.findall("{%s}classificationSection/{%s}classificationTerm" \
                     % (ADLGAZ, ADLGAZ))
    if e:
        p.setPlaceType(e[0].text)

    # Authorship
    creators = [e.text for e in root.findall("{%s}creator" % DC)]
    contributors = [e.text for e in root.findall("{%s}contributor" % DC)]
    
    # Rights
    e = root.findall("{%s}rights" % DC)
    if e:
        rights = e[0].text
    else:
        rights = None

    p.setCreators(creators)
    p.setContributors(contributors)
    p.setRights(rights)
    
    # lists of location and name ids
    lids = []
    nids = []

    # Names
    for e in root.findall("{%s}featureName" % ADLGAZ):
        transliteration = e.findall("{%s}transliteration" % AWMC)[0].text
        na = e.findall("{%s}name" % ADLGAZ)
        if na:
            nameAttested = na[0].text
        else:
            nameAttested = ''
        type = e.findall("{%s}classificationSection/{%s}classificationTerm" \
                         % (ADLGAZ, ADLGAZ))[0].text
        if not transliteration or not type:
            raise EntityLoadError, "Incomplete featureName element"

        id = ptool.normalizeString(transliteration)

        if type == u'geographic':
            nid = names.invokeFactory('GeographicName', id=id)
        elif type == u'ethnic':
            nid = names.invokeFactory('EthnicName', id=id)
        else:
            raise EntityLoadError, "Invalid name type"
            
        n = getattr(names, nid)
        n.setTitle(transliteration)
        n.setNameAttested(nameAttested)
        n.setCreators(creators)
        n.setContributors(contributors)
        n.setRights(rights)

        # make the reference
        p.addReference(n, 'name_name')
        
        nids.append(nid)

    # Locations
    for e in root.findall("{%s}spatialLocation" % ADLGAZ):
        coords = e.findall("{%s}point" % GEORSS)[0].text

        lid = locations.invokeFactory('Location')
        l = getattr(locations, lid)
        l.setGeometryType('Point')
        l.setSpatialCoordinates(coords)
        l.setCreators(creators)
        l.setContributors(contributors)
        l.setRights(rights)

        # make the reference
        p.addReference(l, 'location_location')

        lids.append(lid)

    return {'place_id': pid, 'location_ids': lids, 'name_ids': nids}

