import os, sys
import glob
import unittest
import doctest

from Testing import ZopeTestCase as ztc
from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup, PloneSite, ZCMLLayer
import Products.PleiadesEntity
from Products.PleiadesEntity.tests import _testing

ztc.installProduct('ATVocabularyManager')
ztc.installProduct('Products.ATBackRef')
ztc.installProduct('Products.CompoundField')
ztc.installProduct('Products.OrderableReferenceField')
ztc.installProduct('pleiades.vocabularies')
ztc.installProduct('PleiadesEntity')

@onsetup
def setup_pleiades_entity():
    fiveconfigure.debug_mode = True
    import Products.PleiadesEntity
    zcml.load_config('configure.zcml', Products.PleiadesEntity)
    fiveconfigure.debug_mode = False
    
    ztc.installPackage('pleiades.vocabularies')
    ztc.installPackage('Products.PleiadesEntity')
    
setup_pleiades_entity()
ptc.setupPloneSite(products=['PleiadesEntity'])

optionflags = (
    doctest.ELLIPSIS
    | doctest.NORMALIZE_WHITESPACE
    | doctest.REPORT_ONLY_FIRST_FAILURE
    )

class PleiadesEntityTestCase(ptc.PloneTestCase):
    
    layer = PloneSite
    
    def afterSetUp(self):
        self.test_params = _testing
        self.test_params.TEST_DATA = os.path.join(
            os.path.dirname(__file__), 'data'
            )
        # Currently this stuff isn't being torn down between doctests. Why not?
        try:
            self.folder.invokeFactory('FeatureContainer', id='features')
            self.folder['features'].invokeFactory('Folder', id='metadata')
            self.folder.invokeFactory('PlaceContainer', id='places')
            mid = self.folder['features']['metadata'].invokeFactory('PositionalAccuracy', id='cap-map65')
            self.folder['features']['metadata'][mid].setValue(0.01)
            self.folder['features']['metadata'][mid].setText("That's right, 1 cm!")
        except:
            pass

integration_tests = [
    'Entities.txt',
    'WSTransliteration.txt',
    'WSValidation.txt',
    'subscribers.txt',
    'LoadEntity.txt',
#    'BatchLoad.txt',
    'attestations-view.txt',
    'citations.txt',
    'LoadCAP.txt'
    ]

functional_tests = [
    ]

def make_integration_suite(name):
    return ztc.ZopeDocFileSuite(
                name,
                package='Products.PleiadesEntity.tests',
                test_class=PleiadesEntityTestCase,
                optionflags=optionflags,
                )

def make_functional_suite(name):
    return ztc.FunctionalDocFileSuite(
                name,
                package='Products.PleiadesEntity.tests',
                test_class=PleiadesEntityTestCase,
                optionflags=optionflags,
                )

def test_suite():
    return unittest.TestSuite(
        [make_integration_suite(n) for n in integration_tests]
      + [make_functional_suite(n) for n in functional_tests]
      )

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')

