# -*- coding:utf-8 -*-

import numpy as np
import os.path
import subprocess
import os
import shutil
from scipy import misc
import time
import sys

n = '\n'
t = '\t'


def updateDir(dir):
    if os.path.exists(dir):
        shutil.rmtree(dir)
    time.sleep(0.5)
    os.mkdir(dir)


def removeFile(file):
    if os.path.exists(file):
        os.remove(file)


def url_download(url):
    print('downloading ' + url)
    name = url[url.rfind('/') + 1:url.rfind('.')]
    os.system('wget -O ' + name + '.ogg ' + url)


def dictGet(dict, key):
    if key in dict:
        return dict[key]
    return None


def asyncShellCommand(command, log):
    subprocess.call('nohup ' + command + '>' + log + ' &', shell=True)


def dict2file(dict, splitor, path):
    l = []
    for key in dict:
        l.append(key + splitor + dict[key])
    list2file(l, path)


def appendSystemPath(path):
    import sys

    if not os.path.exists(path):
        raise Exception("目录不存在!")
    sys.path.append(path)


def showImage(x):
    import matplotlib.pyplot

    matplotlib.pyplot.imshow(x.astype('float32'))


def getImageMatrix(path):
    import matplotlib.image
    from PIL import Image
    x = matplotlib.image.imread(path)
    if x.shape[2]==4:   # 4 channels
        x = Image.open(path).convert("RGB")
        x = np.asarray(x, dtype=np.float32)
    return x

def matrix2image(m,path):
    misc.imsave(path, m)

def file2str(path):
    i = open(path)
    res = i.read()
    i.close()
    return res


def countOccurence(list):
    dic = dict()
    for s in list:
        c = 1
        if s in dic:
            c = dic[s] + 1
        dic[s] = c
    return sortDict(dic)


def sortDict(dic):
    return [(k, dic[k]) for k in sorted(dic, key=dic.get)]


def file2set(path):
    res = set()
    read = open(path, encoding='utf-8')
    while True:
        line = read.readline()
        if not line: break
        line = line.replace('\n', '').replace('\r', '')
        if len(line) == 0: break
        res.add(line)
    read.close
    return res


def list2file(list, path):
    o = open(path, 'w')  # , encoding='utf-8'
    for s in list:
        o.write(str(s) + n)
    o.close()


def file2list(path):
    read = open(path , encoding='utf-8')
    return [x.replace('\n', '').replace('\r', '') for x in read.readlines()]


def str2file(content, path, isAppend):
    type = 'w'
    if isAppend: type = 'a'
    o = open(path, type)  # , encoding='utf-8'
    o.writelines(content)
    o.close()


def getMatrix(rowNum, colNum):
    return [[0 for col in range(colNum)] for row in range(rowNum)]


def command_run(command, timeout=1000000):
    proc = subprocess.Popen(command, bufsize=0, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    poll_seconds = 1
    deadline = time.time() + timeout
    while float(time.time()) < float(deadline) and proc.poll() == None:
        time.sleep(poll_seconds)
    timeout = False
    if proc.poll() == None:
        if float(sys.version[:3]) >= 2.6:
            timeout = True
            proc.terminate()

    stdoutS, stderrS = None, None
    if (not timeout):
        stdoutS, stderrS = proc.communicate()

    return stdoutS, stderrS, timeout


def list2str(list):
    return '[' + ','.join([str(e) for e in list]) + ']'



# get int in [0,i)
def getRandomInt(i):
    import random as ra

    return ra.randint(0, i - 1)


def getHtmlSrc(url):
    import urllib.request

    response = urllib.request.urlopen(url)
    html = str(response.read(), 'utf-8')
    return html
