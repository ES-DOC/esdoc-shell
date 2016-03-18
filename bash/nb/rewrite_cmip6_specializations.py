# -*- coding: utf-8 -*-

"""
.. module:: rewrite_cmip6_vocab.py
   :platform: Unix, Windows
   :synopsis: Rewrites esdoc-nb cmip6 vocabulary definitions to esdoc-mp.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import argparse
import inspect
import os

from esdoc_nb.mp.cmip6 import cmip6_atmosphere as atmosphere
from esdoc_nb.mp.cmip6 import cmip6_ocean as ocean
from esdoc_nb.mp.cmip6 import cmip6_seaice as sea_ice


# Define command line options.
_ARGS = argparse.ArgumentParser("Rewrites esdoc-nb cmip6 vocabulary definitions to esdoc-mp.")
_ARGS.add_argument(
    "--dest",
    help="Path to a directory into which esdoc-mp compatible vocabulary definitions will be written.",
    dest="dest",
    type=str
    )


class _DefinitionBase(object):
    def __init__(self, nb_mod, nb_func):
        """Instance constructor.

        """
        self.nb_mod = nb_mod
        self.nb_func = nb_func
        self.nb_definition = nb_func()
        self.nb_constraints = {i[0]:i[2] for i in self.nb_definition['constraints']}


    def __repr__(self):
        """Instance representation.

        """
        return self.name


    @property
    def description(self):
        """Gets the definition description.

        """
        return self.nb_func.__doc__


    @property
    def vocab_status(self):
        """Gets the definition vocabulary status.

        """
        return self.nb_definition["vocab_status"]


    def _get_nb_funcs(self, collection):
        nb_funcs = self.nb_constraints.get(collection, [])
        nb_funcs = ["_{}".format(i.split(".")[-1]) for i in nb_funcs]
        nb_funcs = [getattr(self.nb_mod, f) for f in nb_funcs]

        return nb_funcs


class _ProcessAlgorithmDefinition(object):
    pass


class _ProcessPropertyDefinition(object):
    pass


class _SelectionEnumDefinition(object):
    @property
    def vocab_status(self):
        """Gets the definition vocabulary status.

        """
        return self.nb_definition["vocab_status"]


class _ProcessDefinition(_DefinitionBase):
    @property
    def name(self):
        """Gets the process's name.

        """
        return self.nb_constraints['name']


    @property
    def algorithm_properties(self):
        """Gets the process's set of algorithm properties.

        """
        return self._get_nb_funcs("algorithm_properties")


    @property
    def detailed_properties(self):
        """Gets the process's set of detail properties.

        """
        return self._get_nb_funcs("detailed_properties")


class _DomainDefinition(_DefinitionBase):
    def __init__(self, nb_mod, nb_func, name=None):
        super(_DomainDefinition, self).__init__(nb_mod, nb_func)

        name = name or nb_mod.__name__.split("_")[-1]
        self.name = name[0].upper() + name[1:]


    @property
    def process_definitions(self):
        """Gets the domain's process definitions.

        """
        nb_funcs = self._get_nb_funcs("simulates")

        return [_ProcessDefinition(self.nb_mod, i) for i in nb_funcs]



_DOMAIN_SET = {
    _DomainDefinition(atmosphere, atmosphere._atmos_domain),
    # _DomainDefinition(ocean, ocean._ocean_domain),
    _DomainDefinition(sea_ice, sea_ice._sea_ice_domain, "Sea Ice"),
}

for dd in _DOMAIN_SET:
    for pd in dd.process_definitions:
        print pd
        # print pd.detailed_properties

