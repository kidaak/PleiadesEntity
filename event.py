import geojson
import logging
import re
from os import makedirs

from Acquisition import aq_inner, aq_parent
from plone.app.iterate.interfaces import IAfterCheckinEvent
from Products.CMFCore.interfaces import IActionSucceededEvent, IContentish
from Products.CMFCore.utils import getToolByName
from zope.component import adapter, getMultiAdapter
from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from DateTime import DateTime

from Products.PleiadesEntity.content.interfaces import ILocation, IName
from Products.PleiadesEntity.content.interfaces import IFeature, IPlace
from Products.PleiadesEntity.time import temporal_overlap
from pleiades.transliteration import transliterate_name
from pleiades.json.browser import getContents, wrap, W
from pleiades.geographer.geo import extent, representative_point
from shapely.geometry import asShape, LineString, mapping, Point, shape

log = logging.getLogger('PleiadesEntity')

pidrex = re.compile('^\d+$')

def getView(context, name):
    """ Return a view associated with the context and current HTTP request.

    @param context: Any Plone content object.
    @param name: Attribute name holding the view name.
    """

    try:
        view = context.unrestrictedTraverse("@@" + name)
    except AttributeError:
        raise RuntimeError("Instance %s did not have view %s" % (str(context), name))

    view = view.__of__(context)

    return view


def reindexWhole(obj, event):
    for p in obj.getBRefs('hasPart'):
        log.debug("Reindexing whole %s", p)
        p.reindexObject()

def reindexContainer(obj, event):
    x = aq_inner(obj)
    f = aq_parent(x)
    if IPlace.providedBy(f):
        log.debug("Reindexing container %s", f)
        f.reindexObject()
        reindexWhole(f, event)
        #writePlaceJSON(f, event)


def writePlaceJSON(place, event, published_only=True):
    wftool = getToolByName(place, "portal_workflow")
    status = wftool.getStatusOf("pleiades_entity_workflow", place)
    if published_only and status and status.get("review_state", None) != "published":
        return

    # determine the filename to write, and what directory to use, so the filesystem doesn't choke
    pid = place.getId()
    m = pidrex.match(pid)
    if not m:
        # don't write out json for temp places, e.g., copy_of_12345
        return
    pidbits = list(pid)
    pidpath = '/home/zope/pleiades/json/' + '/'.join(pidbits[:3]) + "/%s" % pid
    try:
        makedirs(pidpath)
    except OSError:
        pass
    fn = "%s/json" % pidpath

    # get JSON for this place
    data = getView(place, 'json')._data(published_only=True)


    # write JSON to disk
    f = open(fn, 'w')
    f.write(str(data))
    f.close()

@adapter(IPlace, IObjectModifiedEvent)
def placeJSONSubscriber(obj, event):
    log.debug("Event handled: %s, %s", obj, event)
    #writePlaceJSON(obj, event)

@adapter(IName, IObjectModifiedEvent)
def nameChangeSubscriber(obj, event):
    obj.getField('title').set(
        obj, obj.getNameTransliterated().split(',')[0].strip() or "Untitled")
    reindexContainer(obj, event)
    
@adapter(ILocation, IObjectModifiedEvent)
def locationChangeSubscriber(obj, event):
    log.debug("Event handled: %s, %s", obj, event)

    # Reindex co-temporal names of the parent place since they are being
    # localized by this location.
    place = aq_parent(aq_inner(obj))
    for o in filter(
            lambda x: temporal_overlap(obj, x),
            place.getNames() ):
        o.reindexObject()

    reindexContainer(obj, event)

@adapter(IFeature, IObjectModifiedEvent)
def featureChangeSubscriber(obj, event):
    reindexWhole(obj, event)

@adapter(IContentish, IObjectModifiedEvent)
def contributorsSubscriber(obj, event):
    # Ensure that principals from the obj's version history are represented
    # in the Contributors field.
    
    def fixSeanTom(p):
        if p in ("T. Elliott", "Tom Elliott"):
            return "thomase"
        elif p in ("S. Gillies", "Sean Gillies", "admin"):
            return "sgillies"
        else:
            return p

    def repairPrincipal(p):
        return [fixSeanTom(v.strip()) for v in p.split(",")]
    
    def repairPrincipals(seq):
        return reduce(lambda x, y: x+y, map(repairPrincipal, seq), [])

    creators = set(repairPrincipals(obj.Creators()))
    contributors = set(filter(
        lambda x: x not in creators, 
        repairPrincipals(obj.Contributors())))
    credited = creators.union(contributors)
    
    def getPrincipals(ob):
        principals = set()
        context = aq_inner(ob)
        rt = getToolByName(context, "portal_repository")
        history = rt.getHistoryMetadata(context)
        if history:
            for i in range(len(history)):
                metadata = history.retrieve(i)['metadata']['sys_metadata']
                for p in repairPrincipal(metadata['principal']):
                    principals.add(p)
        return principals

    try:
        principals = getPrincipals(obj)
        if IPlace.providedBy(obj):
            for sub in (obj.getNames() + obj.getLocations()):
                sub_principals = set(
                    repairPrincipals(sub.Creators()) \
                    + repairPrincipals(sub.Contributors()))
                principals = principals.union(sub_principals)
        uncredited = principals - credited
        
        obj.setCreators(list(creators))
        obj.setContributors(list(contributors.union(uncredited)))
        obj.reindexObject(idxs=['Creator', 'Contributors'])
        
        context = aq_inner(obj)
        parent = aq_parent(context)
        if IPlace.providedBy(parent):
            contributorsSubscriber(parent, event)

    except:
        log.exception(
            "Failed to sync Contributors with revision history" )

# We want to reindex containers when locations, names change state
#
@adapter(ILocation, IActionSucceededEvent)
def locationActionSucceededSubscriber(obj, event):
    log.debug("Event handled: %s, %s", obj, event)
    reindexContainer(obj, event)

@adapter(IName, IActionSucceededEvent)
def nameActionSucceededSubscriber(obj, event):
    reindexContainer(obj, event)

@adapter(IPlace, IAfterCheckinEvent)
def placeAfterCheckinSubscriber(obj, event):
    for child in obj.values():
        child.reindexObject()
    reindexContainer(event.object, event)

