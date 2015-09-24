# pylint: disable=W0621, C0111, E1101

"""Tests for OrcidXmlExporter class."""

# third party
import pytest
import urllib2
from lxml import etree

# local
from orcid import OrcidXmlExporter

XSD_URL = "https://raw.githubusercontent.com/ORCID/ORCID-Source/master" + \
          "/orcid-model/src/main/resources/orcid-message-1.1.xsd"

@pytest.fixture
def exporter():
    return OrcidXmlExporter()

@pytest.fixture
def schema():
    xsd_schema = urllib2.urlopen(XSD_URL)
    schema_root = etree.XML(xsd_schema.read())
    schema = etree.XMLSchema(schema_root)
    return schema

def is_valid_orcid_xml(xmlstring, schema):
    """Validates xmlstring using ORCID xsd schema.

    For the format definition and tutorials see:
    http://support.orcid.org/knowledgebase/articles/135422-xml-for-orcid-works

    :param xmlstring: xml in ORCID readable format.
    :type xmlstring: str
    :returns: bool -- indicates whether the validation passed or not
    """

    xmlparser = etree.XMLParser(schema=schema, encoding='utf-8')
    try:
        etree.fromstring(xmlstring.encode('utf-8'), xmlparser)
        return True
    except etree.XMLSyntaxError, exception_message:
        print exception_message
        return False


class TestWorkExporter(object):

    """ A class with validation of ORCID work XMLs.

    It checks whether the XMLs produced by OrcidXmlExporter and works.xml
    are compatible with ORCID's XSD schema.
    """

    @classmethod
    def _export_and_validate(cls, worklist, exporter):
        xmlstring = exporter.export(worklist, "works.xml")
        return is_valid_orcid_xml(xmlstring, schema())

    def test_empty_export(self, exporter):
        assert self._export_and_validate([], exporter) == True

    def test_orcid_example_export(self, exporter):
        assert self._export_and_validate([{
            "work_title" : {
                "title" : "API Test Title",
                "subtitle" : "My Subtitle",
                "translated_titles" : [("fr", "API essai Titre")]
            },
            "journal_title" : "Journal Title",
            "short_description" : "My Abstract",
            "work_citation" : ("formatted-apa",
                               "My correctly formatted citation"),
            "work_type" : "journal-article",
            "publication_date" : {
                "year" : 2010,
                "month" : 11
            },
            "work_external_identifiers" : [("other-id", "1234")],
            "url" : "www.orcid.org",
            "contributors" : [{
                "name" : "LastName, FirstName",
                "attributes" : {
                    "role" : "author",
                    "sequence" : "first"
                }
            }],
            "language_code" : "en",
            "country" : ("US", "public")
        }], exporter) == True

    def test_work_visibility(self, exporter):
        assert self._export_and_validate([{
            "work_title" : {
                "title" : "Public work"
            },
            "short_description" : "Short description of public work",
            "work_type" : "test",
            "visibility" : "public"
        }], exporter) == True

    def test_work_put_code(self, exporter):
        assert self._export_and_validate([{
            "work_title" : {
                "title" : "A work"
            },
            "short_description" : "Very short description",
            "work_type" : "test",
            "put_code" : 1
        }], exporter) == True

    def test_no_title(self, exporter):
        """ If no title is provided, the xml will not be accepted by ORCID."""
        assert self._export_and_validate([{
            "work_title" : {
                "subtitle" : "A work",
                "translated_titles" : [("fr", "Omlette du fromage")]
            },
            "short_description" : "Very short description",
            "work_type" : "test"
        }], exporter) == False

    def test_many_works(self, exporter):
        work_dict = {
            "work_title" : {
                "title" : "A work",
            },
            "short_description" : "Very short description",
            "work_type" : "test"
        }
        assert self._export_and_validate([work_dict, work_dict, work_dict],
                                          exporter) == True

    def test_incomplete_date(self, exporter):
        """ The 'day' field in publication_date dictionary requires 'month' and
        'year' fields. Also, the 'month' field requires the 'year' field.
        """
        assert self._export_and_validate([{
            "work_title" : {
                "title" : "A work"
            },
            "short_description" : "Very short description",
            "work_type" : "test",
            "publication_date" : {
                "month" : 10,
                "day" : 12
            }
        }], exporter) == False

    def test_many_contributors(self, exporter):
        contributor = {
            "orcid" : "ContributorOrcid",
            "name" : "Contributor Contributowski",
            "email" : "contrib@ut.or",
            "attributes" : {
                "role" : "author",
                "sequence" : "first"
            }
        }
        assert self._export_and_validate([{
            "work_title" : {
                "title" : "A work"
            },
            "short_description" : "Very short description",
            "work_type" : "test",
            "contributors" : [contributor, contributor, contributor]
        }], exporter) == True

    def test_wrong_year(self, exporter):
        """ Year should be a four digit number. """
        assert self._export_and_validate([{
            "work_title" : {
                "title" : "A work"
            },
            "short_description" : "Very short description",
            "work_type" : "test",
            "publication_date" : {
                "year" : 10000
            }
        }], exporter) == False

    def test_wrong_month(self, exporter):
        """ Month should be a two digit number. """
        assert self._export_and_validate([{
            "work_title" : {
                "title" : "A work"
            },
            "short_description" : "Very short description",
            "work_type" : "test",
            "publication_date" : {
                "year" : 2014,
                "month" : 8
            }
        }], exporter) == False
