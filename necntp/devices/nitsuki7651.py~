
import time
import subprocess
import pyinterface


class nitsuki7651(object):
    def __init__(self):
        self.dio1 = pyinterface.open(2702, 0)
        pass
        
    def get_current_datetime(self):
        d1 = self.dio1.input_dword('IN1_32')
        d2 = self.dio1.input_dword('IN33_64')
        
        d = d1.to_uint() + (d2.to_uint() * 2**32)
        
        yy = ((d >> 0) & 0x01) + \
             ((d >> 1) & 0x01) * 4 +\
             ((d >> 2) & 0x01) * 10 +\
             ((d >> 3) & 0x01) * 40 +\
             ((d >> 25) & 0x01) * 2 +\
             ((d >> 26) & 0x01) * 8 +\
             ((d >> 27) & 0x01) * 20 +\
             ((d >> 28) & 0x01) * 80 +\
             2000
        
        month = ((d >> 4) & 0x01) +\
                ((d >> 5) & 0x01) * 4 +\
                ((d >> 6) & 0x01) * 10 +\
                ((d >> 29) & 0x01) * 2 +\
                ((d >> 30) & 0x01) * 8 
        
        day = ((d >> 31) & 0x01) +\
              ((d >> 32) & 0x01) * 4 +\
              ((d >> 33) & 0x01) * 10 +\
              ((d >> 7) & 0x01) * 2 +\
              ((d >> 8) & 0x01) * 8 +\
              ((d >> 9) & 0x01) * 20
        
        hour = ((d >> 10) & 0x01) +\
               ((d >> 11) & 0x01) * 4 +\
               ((d >> 12) & 0x01) * 10 +\
               ((d >> 35) & 0x01) * 2 +\
               ((d >> 36) & 0x01) * 8 +\
               ((d >> 37) & 0x01) * 20 
        
        minute = ((d >> 13) & 0x01) +\
                 ((d >> 14) & 0x01) * 4 +\
                 ((d >> 15) & 0x01) * 10 +\
                 ((d >> 16) & 0x01) * 40 +\
                 ((d >> 38) & 0x01) * 2 +\
                 ((d >> 39) & 0x01) * 8 +\
                 ((d >> 40) & 0x01) * 20 
        
        sec = ((d >> 41) & 0x01) +\
              ((d >> 42) & 0x01) * 4 +\
              ((d >> 43) & 0x01) * 10 +\
              ((d >> 44) & 0x01) * 40 +\
              ((d >> 17) & 0x01) * 2 +\
              ((d >> 18) & 0x01) * 8 +\
              ((d >> 19) & 0x01) * 20 
            
        msec = ((d >> 20) & 0x01) * 100 +\
               ((d >> 21) & 0x01) * 400 +\
               ((d >> 45) & 0x01) * 200 +\
               ((d >> 46) & 0x01) * 800
        
        return {'year': yy,
                'month': month,
                'day': day,
                'hour': hour,
                'min': minute,
                'sec': sec,
                'msec': msec}
        
    
    def sync_system_time(self):
        done = False
        t1 = time.time()
        
        while True:
            timestamp = self.get_current_datetime()
            
            if timestamp['msec'] == 0:
                if not done:
                    t2 = time.time()
                    dt = (1 - (t2 - t1)) * 1000
                    t1 = time.time()
                    
                    ts = '{year:04d}-{month:02d}-{day:02d} {hour:02d}:{min:02d}:{sec:02d}'.format(**timestamp)
                    
                    if (timestamp['sec'] % 10) == 0:
                        cmd = ['date', '-s', ts]
                        subprocess.run(cmd, stdout=subprocess.PIPE)
                        msg = '* ' + ts + ' (delta: {dt:5.2f} ms)'.format(dt=dt)                        
                        
                    else:
                        msg = '  ' + ts + ' (delta: {dt:5.2f} ms)'.format(dt=dt)                        
                        pass
                    
                    print(msg)
                    done = True
                    
                else:
                    pass
                
            else:
                done = False
                pass
            
            time.sleep(0.0001)
            continue
        


