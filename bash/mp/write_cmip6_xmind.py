# -*- coding: utf-8 -*-

"""
.. module:: write_cmip6_xmind.py
   :platform: Unix, Windows
   :synopsis: Rewrites cmip6 vocab defintions to xmind files.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import argparse
import inspect

import xmind
from xmind.core.topic import TopicElement

import sea_ice



# Define command line options.
_ARGS = argparse.ArgumentParser("Rewrites CMIP6 vocab definitions to xmind files.")
_ARGS.add_argument(
    "--dest",
    help="Path to a directory into which xmind defintions will be written.",
    dest="dest",
    type=str
    )


# Set of CMIP6 domains to be converted to mindmaps.
_DOMAINS = {
    sea_ice
}


def _get_sub_modules(mod):
    """Returns set of sub-modules derived from inspecting a module's members.

    """
    return [m[1] for m in inspect.getmembers(mod) if inspect.ismodule(m[1])]


def _get_definitions(mod):
    """Returns set of vocab definitions derived from inspecting a module's members.

    """
    return [(m[0], m[1].__doc__, m[1]()) for m in inspect.getmembers(mod) if inspect.isfunction(m[1])]


def _get_process_url(process_name):
    """Returns URL to a scientific process definition.

    """
    return "https://github.com/ES-DOC/esdoc-cv/tree/master/cmip6/sea_ice/{}".format(process_name)


def _get_vocab_group_url(process_name, group_name):
    """Returns URL to a scientific process definition.

    """
    return "https://github.com/ES-DOC/esdoc-cv/tree/master/cmip6/sea_ice/{}/{}.py".format(process_name, group_name)



def _write_vocab_item(parent_topic, title, description):
    """Writes a vocabulary item.

    """
    topic = TopicElement()
    topic.setTitle(title)
    if description:
        topic.setPlainNotes(description)

    parent_topic.addSubTopic(topic)


def _write_vocab_set(parent_topic, name, description, definition):
    """Writes a vocabulary to the worksheet.

    """
    topic = TopicElement()
    topic.setTitle(name)
    if description:
        topic.setPlainNotes(description)
    for label, description in definition['choices']:
        _write_vocab_item(topic, label, description)

    parent_topic.addSubTopic(topic)


def _write_vocab_group(parent_topic, mod, title):
    """Writes a group of vocabularies to the worksheet.

    """
    # Derive group attributes.
    group_name = mod.__name__.split(".")[-1]
    group_url = _get_vocab_group_url(parent_topic.getTitle(), group_name)

    # Initialise vocab group.
    topic = TopicElement()
    topic.setTitle(title)
    topic.setTopicHyperlink(group_url)

    # For each vocab add a sub-topic.
    for name, description, definition in _get_definitions(mod):
        _write_vocab_set(topic, name, description, definition)

    parent_topic.addSubTopic(topic)


def _write_process(sheet, mod):
    """Writes a worksheet that represents a scientific process.

    """
    # Derive process attributes.
    process_name = mod.__name__.split(".")[-1]
    process_url = _get_process_url(process_name)

    # Initialise worksheet.
    sheet.setTitle(process_name)
    topic = sheet.getRootTopic()
    topic.setTitle(process_name)
    topic.setTopicHyperlink(process_url)

    # Append algorithm properties.
    if hasattr(mod, "algorithm_properties"):
        _write_vocab_group(topic, mod.algorithm_properties, "algorithms")

    # Append detailed properties.
    if hasattr(mod, "detailed_properties"):
        _write_vocab_group(topic, mod.detailed_properties, "details")


def _write_domain(mod, dest):
    """Writes a worksheet (i.e. xmind file) that represents a scientific domain.

    """
    # Open workbook.
    fname = mod.__name__.split(".")[-1].replace("_", "-")
    fpath = "{}/{}.xmind".format(dest, fname)
    book = xmind.load(fpath)

    # Write a worksheet per scientific process.
    for idx, mod in enumerate(_get_sub_modules(mod)):
        sheet = book.getPrimarySheet() if idx == 0 else book.createSheet()
        book.addSheet(sheet)
        _write_process(sheet, mod)

    # Save workbook.
    xmind.save(book, fpath)


def _main(args):
    """Main entry point.

    """
    # Write a workbook (i..e xmind file) per scientific domain.
    for mod in _DOMAINS:
        _write_domain(mod, args.dest)


# Entry point.
if __name__ == '__main__':
    _main(_ARGS.parse_args())
