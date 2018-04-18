from hashlib import sha256

def generateuid(seriesnum):
    hashed = sha256(seriesnum).hexdigest()
    return hashed


def checkhashed(seriesnum, hashed):
    if hashed == sha256(seriesnum).hexdigest():
        print("It Matches!")
        return True
    else:
        print("It Does not Match")
        return False