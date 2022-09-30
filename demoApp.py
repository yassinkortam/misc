import os
import importlib

from fastapi import FastAPI
app = FastAPI()

#getting the absolute path of main.py
real_path = os.path.realpath(__file__)
#getting the path of the main.py file directory
dir_path = os.path.dirname(real_path)

#subdirectory where modules are located
pathToModules = 'yourPath'

#getting a list of all the modules' files 
moduleFiles = os.listdir(dir_path + '/' + pathToModules)


#automatically import modules
for file in moduleFiles: 

    #skip irrelevant files
    if not file.endswith('.py'): continue
    if file.endswith('__init__.py'): continue

    #add the relative path to the module
    path = pathToModules.replace('/', '.') 
    moduleName = file.removesuffix('.py')

    module = importlib.import_module('.' + moduleName, package=path)
    globals()[moduleName] = module
    print("imported " + moduleName)

importlib.invalidate_caches()

#automatically handle api calls
@app.get("/command/")
async def command(
  moduleToCall: str, 
  arg: int
): #this bit needs later stress testing and conditionals
    module = globals()[moduleToCall]
    function = module.__getattribute__(moduleToCall)
    output = function(arg)
    return {
      "command": output
    }
