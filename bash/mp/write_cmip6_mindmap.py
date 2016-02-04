# -*- coding: utf-8 -*-

"""
.. module:: write_cmip6_xmind.py
   :platform: Unix, Windows
   :synopsis: Rewrites cmip6 vocab defintions to xmind files.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import argparse
import json
import os

import xml.etree.ElementTree as ET

from esdoc_mp.vocabs.cmip6 import VocabParser



# Define command line options.
_ARGS = argparse.ArgumentParser("Rewrites CMIP6 vocab definitions to xmind files.")
_ARGS.add_argument(
    "--dest",
    help="Path to a directory into which xmind defintions will be written.",
    dest="dest",
    type=str
    )
_ARGS.add_argument(
    "--domain",
    help="Domain for whise mindmap file will be written.",
    dest="domain",
    type=str,
    default=None
    )


_NOTE = """
<html>
  <head></head>
  <body>
    <dl>
      <dt><b>Coffee</b></dt>
      <dd>Black hot drink</dd>
      <dt>Milk</dt>
      <dd>White cold drink</dd>
    </dl>
  </body>
</html>
"""


class _VocabParserConfiguration(object):
    """Wraps access to configuration information stored in associated config file.

    """
    def __init__(self):
        """Instance constructor.

        """
        fname = "{}.conf".format(__file__.split("/")[-1].split(".")[0])
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), fname)
        with open(path, 'r') as config:
            self._data = json.loads(config.read())


    def get_section(self, key):
        """Returns a section within the config file.

        """
        return self._data.get(key, {})


class _VocabParser(VocabParser):
    def __init__(self, cfg, domain_filter=None):
        """Instance constructor.

        """
        super(_VocabParser, self).__init__(domain_filter)
        self.cfg = _VocabParserConfiguration()
        self.domain_filter = domain_filter
        self.maps = {}
        self.nodes = {}
        self.positions = {}


    @property
    def mindmaps(self):
        """Returns set of mindmaps and associated domains.

        """
        return self.maps.values()


    def _set_node(self, parent, owner, text=None, url=None, style=None, position=None):
        """Sets a mindmap node.

        """
        cfg = self.cfg.get_section(owner.type)
        atts = {
            'FOLDED': str(cfg['is-collapsed']).lower(),
            'COLOR': cfg['font-color'],
            'BACKGROUND_COLOR': cfg['bg-color'],
            'STYLE': style or "bubble",
            'TEXT': text if text else owner.name
        }

        if position:
            atts['POSITION'] = position

        try:
            url = url or owner.url
        except AttributeError:
            pass
        else:
            atts['LINK'] = url

        if not isinstance(parent, ET.Element):
            parent = self.nodes[parent]

        self.nodes[owner] = ET.SubElement(parent, 'node', atts)
        self._set_font(owner)


    def _set_font(self, owner):
        """Styles a node with font information.

        """
        cfg = self.cfg.get_section(owner.type)

        ET.SubElement(self.nodes[owner], 'font', {
            'BOLD': str(cfg['font-bold']),
            'NAME': cfg['font-name'],
            'SIZE': str(cfg['font-size'])
            })


    def _set_notes(self, owner):
        """Set notes associated with a node.

        """
        print ET.fromstring(_NOTE)
        content = ET.SubElement(self.nodes[owner], 'richcontent', {"TYPE": "NOTE"})
        content.append(ET.fromstring(_NOTE))

        # html = ET.SubElement(content, 'html')
        # head = ET.SubElement(html, 'head')
        # body = ET.SubElement(html, 'body')
        # p = ET.SubElement(body, 'p')
        # p.text = _NOTE


    def on_domain_parse(self, domain):
        """On domain parse event handler.

        """
        self.maps[domain] = ET.Element('map', {})
        self._set_node(self.maps[domain], domain, style="fork")


    def on_process_parse(self, domain, process):
        """On process parse event handler.

        """
        self.positions[process] = 'left' if len(self.positions) % 2 == 0 else 'right'
        self._set_node(domain, process, position=self.positions[process])
        self._set_notes(process)


    def on_subprocess_parse(self, process, subprocess):
        """On sub-process parse event handler.

        """
        self.positions[subprocess] = self.positions[process]
        self._set_node(process, subprocess)


    def on_detail_parse(self, owner, detail):
        """On process detail parse event handler.

        """
        self.positions[detail] = self.positions[owner]
        self._set_node(owner, detail)


    def on_detail_property_parse(self, owner, detail_property):
        """On detail property parse event handler.

        """
        text = "{} .. {}"
        if self.positions[owner] == 'left':
            text = text.format(detail_property.name, detail_property.cardinality)
        else:
            text = text.format(detail_property.cardinality, detail_property.name)

        self._set_node(owner, detail_property, text=text)

        for choice in detail_property.choices:
            self._set_node(detail_property, choice, text=choice.value)



def _main(args):
    """Main entry point.

    """
    # Perform a vocab parse in order to create mindmaps.
    parser = _VocabParser(args.domain if args.domain != "*" else None)
    parser.parse()

    # Write mindmaps to file system.
    for domain, mindmap in parser.maps.items():
        fpath = os.path.join(args.dest, "{}.mm".format(domain.id))
        with open(fpath, 'w') as f:
            f.write(ET.tostring(mindmap))
            print fpath


# Entry point.
if __name__ == '__main__':
    _main(_ARGS.parse_args())
