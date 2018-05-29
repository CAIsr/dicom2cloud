from glob import iglob
from hashlib import sha256
from os import access, R_OK, getcwd
from os.path import join, abspath


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
    resource_dir = '.'  # default not used
    # try local
    localsearch = join('.', '**', "config")
    allfiles = [y for y in iglob(localsearch)]
    while len(allfiles) == 0:
        localsearch = join('..', localsearch)
        allfiles = [y for y in iglob(localsearch)]

    files = [f for f in allfiles if not 'build' in f]
    if len(files) == 1:
        resource_dir = files[0]
        # print('Found resources at: ', abspath(resource_dir))
    elif len(files) > 1:
        for rf in files:
            if access(join(rf, 'd2c.db'), R_OK):
                resource_dir = rf
                break
    else:
        raise ValueError('Cannot locate resources dir from: ', abspath(getcwd()))
    print('Resources dir located to: ', abspath(resource_dir))
    return abspath(resource_dir)
