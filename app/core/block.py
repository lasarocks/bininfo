import threading
from app.core.boothpop import boooothPOP



class bootLocker(object):
    def __init__(self):
        self.resource_lock = threading.Lock()
        self.inst_boot = None
        self.prepare()
    def prepare(self):
        temp = boooothPOP(timeout=5)
        cc_test = '4032034877498884|09|29|788'
        response = temp.check_bin(cc=cc_test)
        if response:
            self.inst_boot = temp
    def check_bin(self, cc):
        with self.resource_lock:
            if not self.inst_boot:
                print(f'sem boooth')
                return False
            return self.inst_boot.check_bin(cc=cc)





pb = bootLocker()



def get_boot():
    return pb
