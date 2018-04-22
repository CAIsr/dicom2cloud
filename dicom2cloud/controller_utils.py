from hashlib import sha256
import sys
from os import access,R_OK
from os.path import join,abspath
from glob import iglob

def generateuid(seriesnum):
    hashed = sha256(str(seriesnum).encode('utf-8')).hexdigest()
    return hashed


def checkhashed(seriesnum, hashed):
    if hashed == sha256(str(seriesnum).encode('utf-8')).hexdigest():
        print("It Matches!")
        return True
    else:
        print("It Does not Match")
        return False

##### Global functions
def findResourceDir():
    # try local
    if sys.platform =='darwin':
        resource_dir = join('.', 'config')
    else:
        resource_dir = join('.', 'config')
    print("1. Base resource dir:",resource_dir)
    if not access(resource_dir,R_OK):
        print('1b. Cannot access local resource_dir')
        #Try to locate resource dir
        allfiles = [y for y in iglob(join('..', '..','**', "config"))]#, recursive=True)]
        files = [f for f in allfiles if not 'build' in f]
        print('Possible paths: ', len(files))
        if len(files) == 1:
            resource_dir = files[0]
            print('2. Found resources at: ', abspath(resource_dir))
        elif len(files) > 1:
            for rf in files:
                if access(rf, R_OK):
                    resource_dir= rf
                    print('3. Access resources at ', abspath(rf))
                    break
        else:
            raise ValueError('Cannot locate resources dir: ', abspath(resource_dir))
    print('Resources dir located to: ', abspath(resource_dir))
    return abspath(resource_dir)