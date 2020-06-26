from __future__ import print_function
import time
import datetime
from termcolor import colored

class Timer:
    def __init__(self, msg='elapsed'):
        self.msg = msg
        
    def __enter__(self):
        self.start = datetime.datetime.now()
        return self
    
    def __exit__(self, type, value, traceback):
        s = [ self.msg ]
        if value:
            s += [ colored(self.time(),'red') ]
            s += [ '%s'%type ]
            s += [ '%s'%value ]
        else:
            s += [ colored(self.time(),'green') ]
        print( ' '.join(s) )
    
    def seconds(self, N=1):
        return (datetime.datetime.now() - self.start).total_seconds()*N
    
    def time(self, N=1):
        t = self.seconds(N)
        if t > 60*60:
            s = '%sh%sm%ss%sms' %( int(t)/60/60, int(t/60)%60, int(t)%60, int(t*1e3)%1000 )
        else: 
            if t > 60: s = '%sm%ss%sms' %( int(t)/60, int(t)%60, int(t*1e3)%1000 )
            else: s = '%ss%sms' % (int(t), int(t*1e3)%1000 )
        return s

    def check(self, wait_secs, total_loop_number):
        try:
            self.loop_number +=1
            if self.seconds()/wait_secs > self.count:
                secs_per_loop = self.seconds(1./self.loop_number)
                remaining_loops = total_loop_number - self.loop_number
                eta_secs = secs_per_loop * remaining_loops
                print('eta', colored( self.time( eta_secs ), 'yellow') )
                self.count += 1
        except:
            self.loop_number = 0
            self.count = 1
        return

class timer:
    def __init__(self, name = ''):
        self.name = name
        self.start = time.clock()
        self.text = ''
    def factor( self, text = '', f = None ):
        self.text = text
        self.f = f
    def __del__(self):
        print( self.__call__() )
        if not self.text == '': print( '\t%s: %.3gs'%(self.text, self.f*elapsed) )
    def __call__(self):
        elapsed = time.clock() - self.start
        return 'timer[%s] '%self.name + str(datetime.timedelta(seconds=elapsed))

class LoopTimer:
    def __init__(self, n=1, name=''):
        self.name = name
        self.start = time.time()
        self.n = n
        print( self.name, 'start', time.strftime("%Hh%Mm%Ss", time.localtime(self.start) ) )
        return
    
    def __del__(self):
        print( self.name, 'done in', time.strftime("%Hh%Mm%Ss", time.gmtime(time.time() - self.start) ) )
        return
    
    def eta( self, i ):
        if i==0: return
        ave = (time.time() - self.start)/i
        print( self.name, 'eta', time.strftime("%Hh%Mm%Ss", time.gmtime((self.n-i)*ave ) ) )
        return
    
    def end( self, i ):
        if i==0: return
        ave = (time.time() - self.start)/i
        print( self.name, 'end', time.strftime("%Hh%Mm%Ss", time.localtime(time.time() + (self.n-i)*ave ) ) )
        return
        
