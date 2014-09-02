"""
.. module:: validate_document.py
   :copyright: @2013 Earth System Documentation (http://es-doc.org)
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Validates a document held upon local file system.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import datetime, sys

import pyesdoc



# Report banner.
_BANNER = "--------------------------------------\n"


def _emit(stream, fpath, report):
    """Emits report to an I/O stream."""
    def _write_header():
        """Writes report header."""
        stream(_BANNER)
        stream("ES-DOC Documentation Validation Report\n")
        stream(_BANNER)
        stream("Generated @ {0}\n".format(datetime.datetime.now()))
        stream("Target = {0}\n".format(fpath))
        stream(_BANNER)

    def _write_body():
        """Writes report body."""
        stream("------ VALIDATION REPORT BEGINS ------\n")
        stream("\n")
        for err in report:
            stream(str(err) + "\n")
        stream("\n")
        stream("\n------ VALIDATION REPORT ENDS --------")

    _write_header()
    _write_body()


def _emit_to_stdout(fpath, report):
    """Emits report to stdout."""
    _emit(pyesdoc.rt.log_warning, fpath, report)


def _emit_to_file_system(fpath, report, opath):
    """Emits report to file system."""
    with open(opath, 'w') as ofile:
        _emit(ofile.write, fpath, report)
    pyesdoc.rt.log("Validation report written to ---> {0}.".format(opath))


def _main(fpath, opath=None):
    """Main entry point."""
    # Open document & validate.
    doc = pyesdoc.read(fpath)
    report = pyesdoc.validate(doc)

    # Inform user of validation result.
    if report:
        if opath:
            _emit_to_file_system(fpath, report, opath)
        else:
            _emit_to_stdout(fpath, report)
    else:
        pyesdoc.rt.log("Documemt is valid.")


# Entry point.
if __name__ == '__main__':
    _main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
