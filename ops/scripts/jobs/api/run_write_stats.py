# -*- coding: utf-8 -*-
import json, os, sys

from pyesdoc import config, db



def _get_stat(stat):
    """Returns a stat in dictionary format."""
    return {
        "project": stat[1],
        "institute": stat[2],
        "doc_type": stat[3],
        "doc_count": stat[0]
    }


def _write_json(dirpath, stats):
    """Writes stats in json format."""
    fpath = os.path.join(dirpath, "doc_stats.json")
    stats = [_get_stat(s) for s in stats]

    with open(fpath, 'w') as io_stream:
        json.dump(stats, io_stream, encoding="ISO-8859-1")


def _write_jsonp(dirpath, stats):
    """Writes stats in jsonp format."""
    fpath = os.path.join(dirpath, "doc_stats.jsonp")
    stats = [_get_stat(s) for s in stats]

    with open(fpath, 'w') as io_stream:
        io_stream.write('onESDOC_JSONPLoad(')
        json.dump(stats, io_stream, encoding="ISO-8859-1")
        io_stream.write(');')


def _write_csv(dirpath, stats):
    """Writes stats in csv format."""
    fpath = os.path.join(dirpath, "doc_stats.csv")
    line_template = "{0}, {1}, {2}, {3}\n"

    with open(fpath, 'w') as io_stream:
        io_stream.write("Project, Institute, Document Type, Document Count\n")
        for count, project, institute, doc_type in stats:
            line = line_template.format(project, institute, doc_type, count)
            io_stream.write(line)


def _main(dirpath):
    """Main entry point."""
    # Start session.
    db.session.start(config.api.db)

    # Get stats.
    stats = db.dao.get_document_counts()

    # End session.
    db.session.end()

    # Write files.
    for writer in (_write_csv, _write_json, _write_jsonp):
        writer(dirpath, stats)


# Main entry point.
if __name__ == '__main__':
    _main(sys.argv[1])

