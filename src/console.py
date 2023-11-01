from datetime  import datetime
from threading import RLock

import os

class Console:
    lock = RLock()
    
    black = "\033[90m"
    white = "\033[97m"
    
    def clear(self):
        os.system("cls")
    
    def log(self, log_type: str, text: str = "", var: dict = {}, time: float = 0.0):
        with self.lock:
            now = datetime.now()
            current_time = now.strftime("%H:%M")
            
            if log_type == "INP":
                print(f"{self.white}{current_time} {self.black}{log_type} {self.white}{text} » ", end="")
                return input()
            
            elif var != {}:
                text += f"{self.black} |"
                
                i = 0
                for v,k in var.items():
                    text += f" {self.white}{v} » {self.black}{k}"
                    if i != len(var)-1:
                        text += f"{self.white},"
                        
                    i += 1
                
                if time == 0.0:
                    print(f"{self.white}{current_time} {self.black}{log_type} {self.white}{text}{self.white}")
                else:
                    print(f"{self.white}{current_time} {self.black}{log_type} {self.white}{text} {self.black}({self.white}{time:.2f}s{self.black}){self.white}")