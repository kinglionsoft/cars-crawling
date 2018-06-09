#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
计时器

>>> print([name for name,value in StopWatchStatus.__members__.items()])
['init', 'running', 'stopped']
>>> sw=StopWatch('test')
>>> sw._name
'test'
>>> int(sw())
0
>>> sw.start()
>>> tm.sleep(1)
>>> int(sw.stop())
1
>>> sw.reset()
0.0
>>> int(sw())
0
>>> sw.start()
>>> tm.sleep(2)
>>> int(sw.stop())
2
>>> sw.display() # doctest: +ELLIPSIS
Name: test
...
Elapsed: 2
    
'''
__author__='yangchao'

import time as tm
import doctest
from enum import Enum

StopWatchStatus=Enum('StopWatchStatus',('init','running','stopped'))
    
class StopWatch(object): 
    
    _count = 0          #StopWatch实例的数量
    
    def __init__(self,name='not defined'):
        self._name = name
        self._elapsed = 0.
        self._mode = StopWatchStatus.init
        self._starttime = 0.
        self._created = tm.strftime('%Y-%m-%d %H:%M:%S', tm.gmtime())
        StopWatch._count += 1

    def __call__(self):
        if self._mode == StopWatchStatus.running:
            return tm.time() - self._starttime
        elif self._mode == StopWatchStatus.stopped:
            return self._elapsed
        else:
            return 0.

    def display(self):
        if self._mode == StopWatchStatus.running:
            self._elapsed = tm.time() - self._starttime
        elif self._mode == StopWatchStatus.init:
            self._elapsed = 0.
        elif self._mode == StopWatchStatus.stopped:
            pass
        else:
            pass
        print('Name: %s\n Created: %s \nStart-time: %s\nMode: %s\nElapsed: %s' % (self._name,self._created,self._starttime,self._mode,int(self._elapsed)))
        
    def start(self):
        if self._mode == StopWatchStatus.running:
            self._starttime = tm.time()
            self._elapsed = tm.time() - self._starttime
        elif self._mode == StopWatchStatus.init:
            self._starttime = tm.time()
            self._mode = StopWatchStatus.running
            self._elapsed = 0.
        elif self._mode == StopWatchStatus.stopped:
            self._mode = StopWatchStatus.running
            self._starttime = tm.time() - self._elapsed
        else:
            pass
        return

    def stop(self):
        if self._mode == StopWatchStatus.running:
            self._mode = StopWatchStatus.stopped
            self._elapsed = tm.time() - self._starttime
        elif self._mode == StopWatchStatus.init:
            self._mode = StopWatchStatus.stopped
            self._elapsed = 0.
        elif self._mode == StopWatchStatus.stopped:
            pass
        else:
            pass
        return self._elapsed

    def lap(self):
        if self._mode == StopWatchStatus.running:
            self._elapsed = tm.time() - self._starttime
        elif self._mode == StopWatchStatus.init:
            self._elapsed = 0.
        elif self._mode == StopWatchStatus.stopped:
            pass
        else:
            pass
        return self._elapsed

    def reset(self):
        self._starttime=0.
        self._elapsed=0.
        self._mode=StopWatchStatus.init
        return self._elapsed



if __name__=='__main__':
    import doctest
    doctest.testmod(verbose=False);
    

