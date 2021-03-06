PleiadesEntity
====================

<out-of-date>The PleiadesEntity product provides Plone content types suitable for
constructing and managing collections of geographic data items, for
example, digital gazetteer entries. 

See http://icon.stoa.org/trac/pleiades/wiki/PleiadesEntityProduct for more
information.

Written by Tom Elliott and Sean Gillies for the Pleiades Project. 
Contact: Pleiades administration <maia@unc.edu>
This product was developed using ArchGenXML, i18ndude, ArgoUML and coffee

The following content types are provided:

    * GeographicEntity: built atop the Archetypes Base Folder, Geographic
    entities can contain 0..n geographic names. This content type provides all
    standard fields, plus custom fields for:
    
          o alphanumeric identifier (a string)
          o geoEntityType (i.e., feature type; a string)
          o modern location (a textual description)
          o time periods (a list)
          o secondary references (a list)
          o spatial coordinates (a string encoded according to the geoRSSSimple 
          specification)
          o spatial geometry type (a string) 

    * GeographicName: built atop the Archetypes Base content class, this
    content type provides all standard fields, plus custom fields for:
    
          o title (this standard field is re-labled in the view template as 
          "nameTransliterated" and it is the intent that an ASCII-
          transliterated version of the content of the nameAttested field be 
          stored therein)
          o alphanumeric identifier (a string)
          o geoNameType (a string)
          o nameAttested (a unicode string, intended for storing the name in its 
          original orthography)
          o nameLanguage (a string, intended to store the name and script 
          associated with the name as attested)
          o time periods (a list)
          o primary references (a list)
          o secondary references (a list) 

Further documentation of the content types, including after-edit and
after-creation behaviors (some fields are automatically filled or rewritten) can
be found in the UML model.</out-of-date>


Future Improvements
----------------------------

<out-of-date>This product will be refactored to reduce its emphasis on (but not
eliminate its suppport for) historical geographic data. If you use or subclass
this product, keep track of your dependencies!</out-of-date>


Installation
---------------

The product is installed using the Plone Quick Installer. Copy or link the
PleiadesEntity directory tree into your Products directory, restart Zope
and use the Quick Installer to install the product.

See DEPENDENCIES.txt for dependency information.


Usage
--------

<out-of-date>Once the product is installed, Geographic entities may be added in any location
where a standard Plone folder can be added. Geographic Names can only be added
within Geographic entities.

The product presently has no custom workflow.

The product attempts to add a number of its fields to appropriate indexes in the
portal_catalog. A site administrator can then configure smart folder settings to
permit users to employ these indexes in constructing smart folder criteria,
thereby providing filtered views of geographic content.</out-of-date>

Places, together with their associated locations and names may be created 
programmatically using the load_place and
loaden functions in Extensions/loader.py. These functions load the content of
xml files, structured according to a loose adaptation of the Alexandria Digital
Library Gazetteer Content Standard (http://www.alexandria.ucsb.edu/gazetteer/).
The xml schema used in the data files will be fully documented in a
future release. A series of extensive tests, using example data, provide
examples that use these functions, and can also guide customizers in writing
their own loading functions. See /tests and /tests/test-data for more. 

Extensions/loader.py also includes an initialize function that can be used to modify a 
stock Plone to meet the expectations of Extensions.loader.loaden. To use both, first
put a copy of loader.py in Zope/Extensions and restart Zope. Then create 
an External Method via the ZMI in the root of the Plone instance (id=initializeModel, 
ModuleName=loader, FunctionName=initialize). Call it from the web browser
like http://localhost/initializeModel. This will adjust addable types as 
needed and create the various container objects you need. Create another 
External Method in the root (id=load_entities, ModuleName=loader, 
FunctionName=loaden). Call it it through the browser as follows:
http://loadlhost/load_entities?sourcedir=/some/filesystem/path

Note that, for efficiency's sake, the loaden function does not update portal_catalog
indexes for newly created items. To get relationships to show up, LiveSearch
to work properly, etc., you'll need to do this manually through the ZMI after
batch creation is finished.

Support
----------

Please subscribe to the pleiades-software email list. The archives may be viewed
online without subscription. 
See: http://icon.stoa.org/trac/pleiades/wiki/PleiadesSoftwareList


About Pleiades
-------------------

Pleiades is an international research network and associated web portal and
content management system devoted to the study of ancient geography. 

See http://icon.stoa.org/trac/pleiades/wiki.

Funding for the creation of this software was provided by a grant from the 
U.S. National Endowment for the Humanities (http://www.neh.gov).
