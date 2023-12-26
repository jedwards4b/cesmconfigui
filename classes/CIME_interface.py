import os
import sys
from importlib import import_module
debug = True

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
        machines = import_module('CIME.XML.machines')
        self.machinesxml = machines.Machines(infile=config_machines, read_only=False)
        return self.machinesxml.list_available_machines()


    def get_machine_name(self):
        return self.machinesxml.get_machine_name()
    
    def copy_machine(self, oldname, newname):
        ''' copy machine node matching oldname to newname,
        newname should not exist in file. '''
        if debug: print(f"Get node for machine {oldname}")
        nodes = self.machinesxml.get_children("machine")
        for machnode in nodes:
            if self.machinesxml.get(machnode, "MACH") == oldname:
                oldnode = machnode
                break

        if debug: print(f"Copy node for machine {oldname}")
        newnode = self.machinesxml.copy(oldnode)

        if debug: print(f"Add name for node for machine {newname}")
        
        self.machinesxml.add_child(newnode)
        self.machinesxml.set(newnode,"MACH", newname)
