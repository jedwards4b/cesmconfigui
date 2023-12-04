import os
import sys
from importlib import import_module

class CIME_interface():
    def __init__(self, cimeroot=None):
        self.machinexml = None
        if not cimeroot:
            cimeroot = os.environ.get("CIMEROOT")
            if cimeroot is None:
                raise SystemExit("ERROR: CIMEROOT must be defined in environment or passed in init")            
        _LIBDIR = os.path.join(cimeroot)
        sys.path.append(_LIBDIR)
        _LIBDIR = os.path.join(cimeroot,"CIME", "Tools")
        sys.path.append(_LIBDIR)
            
        self.files = import_module('CIME.XML.files')
        

        
    def get_machines_file(self, filename=None):
        if filename:
            self.filename = filename
        else:
            filexml = self.files.Files(comp_interface="nuopc")
            self.filename = filexml.get_value("MACHINES_SPEC_FILE")

    def get_machines(self, config_machines):
        '''Get a list of supported machines from the config_machines.xml file.'''
        self.machines = import_module('CIME.XML.machines')
        machinesxml = self.machines.Machines(infile=config_machines)
        return machinesxml.list_available_machines()

    
