#! /usr/bin/env python
# -*- coding: utf-8 -*-

import Levenshtein
import json
import sys
import zipfile
import os

OUTPUT_PATH = "./index.txt"
ZIP_PATH    = "./zip/"

def readIndexFile():
    f = open(OUTPUT_PATH, "r")
    lines = f.readlines()
    f.close()
    matchDataList = []
    for line in lines:
        try:
            matchDataList.append(json.loads(line))
        except:
            pass
    return matchDataList

def unzip(path, fileName):
    ret = ""
    zf = zipfile.ZipFile(path, 'r')
    for f in zf.namelist():
        if f[f.rindex("/"):] != fileName: continue
        filePath = ZIP_PATH + f
        dirPath  = filePath[:filePath.rindex("/")]
        ret = filePath
        if not os.path.exists(dirPath):
            os.mkdir(dirPath)
        if not os.path.exists(filePath):
            out = file(filePath, 'w')
            out.write(zf.read(f))
            out.close()
    return ret

def getRank(origin, matchDataList):
    ret = []
    if not isinstance(origin, unicode):
        origin = origin.decode('utf-8')
    for matchData in matchDataList:
        defArray = matchData['match']
        for (i, defObj) in enumerate(defArray):
            defName = defObj['name'].strip().replace("_", "").lower()
            ratio = Levenshtein.ratio(origin, defName)
            ret.append(
                    {
                        'id'              : matchData['id'],
                        'repos_name'      : matchData['name'],
                        'description'     : matchData['description'],
                        'full_name'       : matchData['full_name'],
                        'language'        : matchData['language'],
                        'url'             : matchData['url'],
                        'clone_url'       : matchData['clone_url'],
                        'git_url'         : matchData['git_url'],
                        'homepage'        : matchData['homepage'],
                        'def_name'        : defName,
                        'def_name_origin' : origin,
                        'line'            : defObj['line'],
                        'path'            : defObj['path'],
                        'ratio'           : ratio
                    }
                    )
    ret = sorted(ret, key=lambda x:x['ratio'], reverse=True)
    # Fetch top 3 relative repositories
    return ret[:3]

def main():
    argvs = sys.argv
    if len(argvs) == 1:
        print("python down_img [userid] [count(default=10)]")
        return

    matchDataList = readIndexFile()
    matchDataListMap = {}
    for argv in argvs[1:]:
        matchDataListMap[argv] = getRank(argv, matchDataList)
    output = ""
    for defName, matchDataList in matchDataListMap.items():
        for matchData in matchDataList:
            key  = "%20s - l.%4d %s in %s [%s]" % (matchData['def_name_origin'], matchData['line'], matchData['def_name'], matchData['repos_name'], matchData['description'])
            path = unzip(ZIP_PATH + matchData['repos_name'] + ".zip", matchData['path'])
            url  = "https://github.com/" + matchData['full_name']
            output += "%s++%s++%d++%s||" %(key, path, matchData['line'], url)
    print output[:len(output)-2]

if __name__ == '__main__':
    main()
