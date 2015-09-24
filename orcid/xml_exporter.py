
"""Class for exporting Python dictionaries to standarized ORCID XML."""

from jinja2 import FileSystemLoader, Environment
import os

class OrcidXmlExporter(object):

    """Python to XML Exporter

    Exports Python dictionary to XML format acceptable by ORCID API.
    """

    @classmethod
    def export(cls, records, template_name):
        """Creates XML with ORCID data from python dictionar/list.

        Currently supported template names:
        + "works.xml" - for works exporting. Records are a list of works. Every
                work is a dictionary and it can contain following fields (most
                fields are optional):
            * work_title - a dictionary:
                - title (required) - string
                - subtitle - string
                - translated_titles - list of pairs (tuples):
                    1). code of language - string (eg. "fr")
                    2). translated title - string
            * journal_title - string
            * short_description - string
            * work_citation - a pair (tuple):
                1). type - string
                2). citation - string in correct format
                See http://support.orcid.org/knowledgebase/articles/
                135758-anatomy-of-a-citation
            * work_type - string
              See http://support.orcid.org/knowledgebase/articles/118795
            * publication_date - a dictionary:
                - year - four digit integer - required
                - month - two digit integer - required if day is provided
                - day - two digit integer
            * work_external_identifiers - a list of pairs (tuples):
                1). type - string
                2). id - string
                See http://support.orcid.org/knowledgebase/articles/118807
                for available types
            * url - string in anyURI format.
              See http://www.datypic.com/sc/xsd/t-xsd_anyURI.html
            * work_contributors - a list of dictionaries. Every contributor can
              contain:
                - orcid - string
                - name - string
                - email - string
                - attributes - a dictionary with "role" and/or "sequence" keys
                See http://support.orcid.org/knowledgebase/articles/
                118843-anatomy-of-a-contributor for details
            * work-source - string with ORCID
            * language_code - string (eg. "en")
            * country - a pair (tuple):
                1). abbreviation - two letters string in ISO 3166 format
                2). visibility - string (see below)
            * visibility - string. One from:
                + "limited"
                + "public"
                + "private"
                + "registered-only"
            * put-code - integer

        :param dictionary: dictionary containing orcid fields
        :type dictionary: dict
        :param template_name: name of file from 'xml_templates' directory
        :type template_name: str
        :returns: str -- XML which can be sent to ORCID with API.
        :raises: TemplateNotFound
        """
        template_dir = os.path.join(os.path.dirname(__file__), 'xml_templates/')
        environment = Environment(loader=FileSystemLoader(template_dir))
        template = environment.get_template(template_name)
        xml = template.render({'records': records})
        return xml
