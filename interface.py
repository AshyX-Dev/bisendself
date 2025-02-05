from typing import Union, List, Dict, Tuple
import json

class Session(object):
    def __init__(self, uinp: Tuple = ()):
        self.uinp = uinp
        self.uinp_len = len(uinp)
        if self.uinp_len != 0:
            self.sid = 0
            self.exists = True
            
            self.uptime: int = uinp[1]
            self.locks: List[int] = json.loads(uinp[2])
            self.locks_length: int = len(self.locks)
            self.alpha_range: int = uinp[3]
        
        else:
            self.sid = 1
            self.exists = False
            
            self.uptime: int = 0
            self.locks: List[int] = []
            self.locks_length: int = 0
            self.alpha_range: int = 0

    def __str__(self):
        return json.dumps(self.uinp, indent=2)
