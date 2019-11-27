# -*- coding: utf-8 -*-

"""
.. module:: generate_cim.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Generates CMIP6 CIM documents from simplified JSON output.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
import argparse
import os

from cmip6.utils import vocabs



# Define command line argument parser.
_ARGS = argparse.ArgumentParser("Generates CMIP6 ensemble subset JSON files.")
_ARGS.add_argument(
    "--institution-id",
    help="An institution identifier",
    dest="institution_id",
    type=str
    )
_ARGS.add_argument(
    "--archive-directory",
    help="Path to cdf2cim archive",
    dest="archive_dir",
    type=str
    )
_ARGS.add_argument(
    "--output-directory",
    help="Path to cdf2cim subsets",
    dest="output_dir",
    type=str
    )

# MIP era.
_MIP_ERA = "cmip6"

def _main(args):
    """Main entry point.

    """
    for i in vocabs.get_institutes(args.institution_id):
        for s in vocabs.get_institute_sources(i):
            for e in vocabs.get_experiments():
                _map_superset_to_subset(args.archive_dir, i, s, e)


def _map_superset_to_subset(archive_dir, i, s, e):
    print(archive_dir, i, s, e)
    # for fpath in  _yield_superset_files(args.archive_dir, i, s):
    #     with open(fpath, 'r') as fstream:
    #         _write_subset_file(fpath, json.loads(fstream.read()))


def _yield_superset_files(archive_dir, i, s):
    """Yields set of scanned files for further processing.

    """
    dpath = archive_dir
    dpath = os.path.join(dpath, _MIP_ERA)
    dpath = os.path.join(dpath, i.canonical_name)
    dpath = os.path.join(dpath, s.canonical_name)

    if os.path.exists(dpath):
        for dpath, _, fnames in os.walk(dpath):
            for fname in fnames:
                yield os.path.join(dpath, fname)


def _write_subset_file(fpath, metadata):
    # Corrections may need to be applied prior to further processing.
    _apply_metadata_corrections(metadata)

    superset = SuperSetContent(metadata)


    raise IOError('dasdsa')


def _apply_metadata_corrections(metadata):
    """Applies corrections to incoming metadata.

    """
    # Early version of client published activity identifiers as a string.
    if not isinstance(metadata['activity_id'], list):
        metadata['activity_id'] = [i for i in metadata['activity_id'].split(' ') if len(i) > 0]


class SuperSetContent(object):
    """A concrete class within the cim v2 type system.

    Dataset discovery information.

    """
    def __init__(self, metadata):
        """Instance constructor.

        """
        super(SuperSetContent, self).__init__()

        for field in [
            # ensemble fields
            'mip_era',
            'activity_id',
            'institution_id',
            'source_id',
            'experiment_id',
            'sub_experiment_id',

            # simulation fields
            'realization_index',
            'initialization_index',
            'physics_index',
            'forcing_index',

            # simulation start/end times
            'end_time',
            'start_time',

            # parent simulation
            'parent_realization_index',
            'parent_initialization_index',
            'parent_physics_index',
            'parent_forcing_index',

            # datasets
            'dataset_versions',
            'filenames',
        ]:
            setattr(self, field, metadata[field])

        self.dataset_versions = self.dataset_versions or []
        self.filenames = self.filenames or []


    @property
    def ensemble_drs(self):
        return '{}/{}/{}/{}/{}'.format(
            self.mip_era.lower(),
            self.institution_id.lower(),
            self.source_id.lower(),
            self.experiment_id.lower(),
            self.sub_experiment_id.lower(),
        )

    @property
    def simulation_drs(self):
        return '{}/r{}i{}p{}f{}'.format(
            self.ensemble_drs,
            self.realization_index,
            self.initialization_index,
            self.physics_index,
            self.forcing_index
        )

# Main entry point.
if __name__ == '__main__':
    _main(_ARGS.parse_args())


"""
{
    "_hash_id": "defadf72e4cf4dc51b3dae4b8a1429a6",

    "mip_era": "CMIP6",
    "institution_id": "MOHC",
    "source_id": "HadGEM3-GC31-HH",
    "experiment_id": "hist-1950",
    "sub_experiment_id": "none",

    "forcing_index": 1,
    "initialization_index": 1,
    "physics_index": 1,
    "realization_index": 1,

    "end_time": "2015-01-01T00:00:00Z",
    "start_time": "1950-01-01T00:00:00Z",

    "activity_id": "HighResMIP",

    "parent_forcing_index": 1,
    "parent_initialization_index": 1,
    "parent_physics_index": 1,
    "parent_realization_index": 1,

    "branch_time_in_child": "1950-01-01T00:00:00Z",
    "branch_time_in_parent": "1980-01-01T00:00:00Z",

    "calendar": "360_day",

    "dataset_versions": [
        "v20171213"
    ],

    "further_info_url": "https://furtherinfo.es-doc.org/CMIP6.MOHC.HadGEM3-GC31-HH.hist-1950.none.r1i1p1f1",
    "variant_info": "none",
    "contact": "enquiries@metoffice.gov.uk",
    "references": "Williams, K., et al: The Met Office Global Coupled model 3.0 and 3.1 (GC3.0 & GC3.1) configurations. JAMES, submitted July 2017.",

}
"""
