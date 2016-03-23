#!/usr/bin/python
'''
This is universal install script, which requeres only Python 2.7
The main point of this script is to create virtual environment with all nessesary python packages for sucessfully autotest work
It made for vtest(visual test) project

Work of install script we can separete in follow steps:
1) Parse input data via argparse
2) If present flag --clear, remove folders docs, venv, log, etc... and exit
3) Create nessesary folders docs, log, venv, etc...
4) Create virtual environment in venv directory
5) Only for Windows! Install pyhton binary packages via easy_install which requires compiler like visual studio
6) Fill virtual environment via pip and etc/requirements.txt file
TODO
7) Make symlink ./venv/bin/py.test -> ./py.test for easy usage
8) Generate docs in ./docs folder via pydoc

If this script doesn`t work, you may manually install python packages from etc/requerements.txt file,
and run python with this packages

@author George Regentov george_regentov@ocslab.com
'''

import urllib
import subprocess
import tempfile
import sys
import os
import shutil
  
class PackageManager(object):
  """
  This class was enhanced to temporary install python modules via pip
  Make temporary directory on creation, add it to sys.path
  For import use class attribute. For example need virtualenv package, use class.virtualenv
  If system provide virtualenv package, class will returm this module
  Otherwise PacketManager will install this package via pip in temporary directory
  If system doesn`t provide pip, it will be install to temporary directory too

  The main point of this class is to provide any system module or install itin temporary directory
  """  
  pip_url = 'http://bootstrap.pypa.io/get-pip.py'
  
  def __init__(self):
    self.system_env = tempfile.gettempdir()
    sys.path.append( self.system_env )
      
  def __getattr__(self, attr):
    try:
      module = __import__( attr )
    except ImportError:
      if attr == 'pip':
        module = self.install_pip()
      else:
        module = self.install_module( attr )
    except:
      print "Unexpected error:", sys.exc_info()[0]
      module = None
    finally:
      return module

  def install_pip(self):
    get_pip_path = tempfile.gettempdir() + os.sep + 'get-pip.py'
    urllib.urlretrieve( self.pip_url, get_pip_path )
    args = [sys.executable, get_pip_path]
    if self.system_env:
      args.extend( ('--target', self.system_env) )

    subprocess.call( args )
    sys.path_importer_cache.clear()
    return self.pip 
  
  def install_module(self, module):
    args = ['install', module]
    
    if self.system_env:
      args.extend( ('--target', self.system_env) )

    self.pip.main( args )
    sys.path_importer_cache.clear()
    return getattr(self, module)    

if __name__ == "__main__":
  pm = PackageManager()

  description = 'Install python environment script.'
  usage = ''
  epilog = ''
  parser = pm.argparse.ArgumentParser(description=description,
                                      usage=usage,
                                      epilog=epilog,
                                      formatter_class=pm.argparse.RawTextHelpFormatter)
  parser.add_argument('--venv', type=str, default='venv', metavar='dir_name',
                     help="Diredtory for virtual environment\nDefault: venv\n")
  parser.add_argument('-r', type=str, default='requirements.txt', metavar='filename',
                     dest='requirements',
                     help="Path to requrements.txt file\nDefault requirements.txt\n")
  parser.add_argument('--clear', default=False, action='store_true',
                     help='Clear temporary data')
  args = parser.parse_args()
  
  cwd = os.path.dirname(os.path.abspath(__file__))

  local_dirs = ['docs', 'log', args.venv]
  local_dirs = map(lambda x: os.path.join(cwd, x), local_dirs)

  # Remove temporary files
  if args.clear:
    map(lambda x: shutil.rmtree(x, ignore_errors = True), local_dirs)
    print 'Temporary data was removed successfully'
    sys.exit(0)

  # Create necessary directories
  map(lambda x: os.path.exists(x) or os.makedirs(x), local_dirs)
  print "Temporary dirictories was created successfully"
  
  # Create virtualenv
  venv = os.path.join(cwd, args.venv)
  pm.virtualenv.create_environment( args.venv )
  print 'Virtual evnironment was successfully created in %s directory.' % args.venv

  # Install Windows specific packages in virtual environment
  if sys.platform == 'win32':
    if sys.maxsize > 2**32: # for 64-bit system
      binary_packages = ( 'https://pypi.python.org/packages/2.7/l/lxml/lxml-3.3.4.win-amd64-py2.7.exe',
                          'http://www.voidspace.org.uk/downloads/pycrypto26/pycrypto-2.6.win-amd64-py2.7.exe')
    else: # for 32-bit system
      binary_packages = ( 'https://pypi.python.org/packages/2.7/l/lxml/lxml-3.3.4.win32-py2.7.exe',
                          'http://www.voidspace.org.uk/downloads/pycrypto26/pycrypto-2.6.win32-py2.7.exe' )
    easy_install = venv + "\Scripts\easy_install.exe"
    for binary_package in binary_packages:
      subprocess.call([ easy_install, binary_package ])
     
  # Fill virtual env
  if os.path.isfile(args.requirements):
    if sys.platform == 'win32':
      pip = os.path.join( venv, 'Scripts', 'pip' )
    else:
      pip = os.path.join( venv, 'bin', 'pip' )
    subprocess.call([ pip, 'install', '-r', args.requirements ])
    print "Virtualenv was successfully filled. \nInstalled environment from %s file" % args.requirements
  else:
    print "File \"%s\" is not exists\nThis file need to fill virtualenv" % args.requirements
    sys.exit(1)

  # Make simlink ./venv/bin/py.test -> py.test for easy usage
  #os.symlink( os.path.join( os.path.dirname(pip), 'py.test'), 'py.test') 

  # Generate documentation via pydoc in docs directory

