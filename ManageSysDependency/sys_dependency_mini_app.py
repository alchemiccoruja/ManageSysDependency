#! /usr/bin/python
# :maintainer:    Osman Jalloh <osman.jalloh@gmail.com>
# :maturity:      new
# :depends:       xxxxxx
# :platform:      all
import sys
import os.path
import os
import pickle
import pprint


ARGVS_LEN = len(sys.argv)

class ComponentDependencyManager(object):
    #"""
    #Application for Managing System Dependencies
    #"""
    
    #Possible commands
    DEPEND = "DEPEND"
    INSTALL = "INSTALL"
    REMOVE  = "REMOVE"
    LIST = "LIST"
    
    #A key into the persistent storage for dependencies
    DEPENDENCIES = "DEPENDENCIES"
    #A key into the persistent storage for installations
    INSTALLATIONS = "INSTALLATIONS"
    
    def __init__(self,_argv):
        self._command_and_params = _argv
        
        #Mapping of Commands to Handler funcions
        self._command_handlers = {}
        self._command_handlers[self.DEPEND] = self.processDepend
        self._command_handlers[self.INSTALL] = self.processInsall
        self._command_handlers[self.REMOVE] = self.processRemove
        self._command_handlers[self.LIST] = self.ProcessList
        
        #Current command and parameters
        self._current_command = self._command_and_params[0]
        self._current_params = self._command_and_params[1:]
        
        
        #Simple Persistent Storage (Map)
        self._basedir = os.path.abspath(os.path.dirname(__file__))
        self._database_file =  os.path.join(self._basedir, "component_dependency_manager.txt")
        self._dependency_map = {}
        
        
    def processDepend(self, _target, _dependencies):
        #Handler for DEPEND commands
        retval = False            
        #If we have not encounter this compnent before
        #Add it to the dependency group
        if  _target not in self.dependencies.keys():
            self.dependencies[_target] = _dependencies
        
        #Account for all it items that it depends on
        for each_dependency in _dependencies:
            if each_dependency not in self.dependencies[_target]:
                self.dependencies[_target].append(each_dependency)
        
        retval = True
        return retval
    
    
    def processInsall(self, _target, _dependencies):
        #Handler for INSTALL commands
        retval = False
        
        #Make sure that we install all dependcies 
        if  _target in self.dependencies.keys():
            #The dependents for this component
            for each_dependent in self.dependencies[_target]:
                #Install each dependent
                #Recursively call processInstall on dependents
                self.processInsall(each_dependent,[])
        
        #Now install the the actual compment
        if  _target not in self.installations.keys():
            print("Installing %s: "%(_target))
            self.installations[_target] = True
        else:
            print("%s already installed: "%(_target))
        
        retval = True
        return retval
    
    
    def processRemove(self, _target, _dependencies):
        #Handler for REMOVE commands
        retval = False
        
        #Ensure that the intended component to be removed
        #is not required for another component
        for _kay, _values in self.dependencies.items():
            #Another component is dependent on this targeted component
            if _target in _values:
                print("%s is still needed"%(_target))
                break
        else:
            
            #Recursively Remove dependencies if they are not depended on other components
            #Note we are not checking got cycled dependencies.
            if  _target in self.dependencies.keys():
                #The dependents for this component
                for each_dependent in self.dependencies[_target]:
                    #Remove each dependent
                    #Recursively call processRemove on dependents
                    self.processRemove(each_dependent,[])
            
            #Remove the component if no one else depends on it
            if _target in self.installations:
                print ("Removing: %s"%(_target))
                del self.installations[_target]
            else:
                print ("%s not Installed"%(_target))
        
        retval = True
        return retval
    
    
    def ProcessList(self, _target, _dependencies):
        #Handler for LIST commands
        retval = False
        print "Listing: "
        for _component in self.installations.keys():
            print _component
        retval = True
        return retval
      
      
    @property
    def dependencies(self):
        #Shortcut to get the dependecies
        return self._dependency_map[self.DEPENDENCIES]
    
    
    @property
    def installations(self):
        #Shortcut to get the installations
        return self._dependency_map[self.INSTALLATIONS] 
    
    
    def provisionDatabase(self):
        #Provision the persistent storage/databases
        #A section for dependencies
        self._dependency_map[self.DEPENDENCIES] = {}
        #A section for installations
        self._dependency_map[self.INSTALLATIONS] = {}
    
    
    def openDatabase(self):
        #Open and read the recorded installations and dependencies
        if os.path.exists(self._database_file) is True:
            with open(self._database_file, 'rb') as output_file:
                self._dependency_map = pickle.load(output_file)
        else:
            self.provisionDatabase()
     
           
    def writeToDatabase(self):
        #Open and write the recorded installations and dependencies
        if os.path.exists(self._database_file) is True:
            #replace the old pickled file
            os.system("rm "+self._database_file)
        with open(self._database_file, 'wb') as output_file:
            pickle.dump(self._dependency_map, output_file)
        

    def run(self):        
        #Not all the commands expect dependencies
        if len(self._current_params) > 0:
            _target = self._current_params[0]
        else:
            _target = None
        
        if len(self._current_params) > 1:
            _dependencies = self._current_params[1:]
        else:
            _dependencies = {}
        
        #Call Handler to execute the commands
        self.openDatabase()
        if self._command_handlers[self._current_command](_target, _dependencies) is True:
            self.writeToDatabase()
        
        
        

if __name__=='__main__':
    if ARGVS_LEN > 1:
        input_file = sys.argv[1]
        print("Input File: %s"%(input_file))
        #Open the input file
        with open(input_file,"r") as _input_fd:
            while _input_fd.closed == False:
                #Read each entry
                _entry = _input_fd.readline()
                #Break once we reach the end of file
               
                #Replace new lines
                _entry = _entry.replace("\n","")
                if _entry == "END":
                   break
                
                #Split the entry into a list form
                #The first item on the list is the intended command
                command_list = _entry.split(" ")
                
                #Execute the command 
                runner=ComponentDependencyManager(command_list)
                runner.run()
        pass
    else:
        print("""
                ERROR: Unexpect paramater count.  Please provide full path to the input file.
              """
              )
        sys.exit(1)
    pass