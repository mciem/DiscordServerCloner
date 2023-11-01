from threading import RLock
from random    import choice
from base64    import b64encode
from json      import dumps

class Utils:
    def __init__(self) -> None:
        self.__lock    = RLock()
    
    def buildXSuperProperties(self, buildnum: int) -> str:
        return b64encode(dumps({"os":"Windows","browser":"Chrome","device":"","system_locale":"pl-PL","browser_user_agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36","browser_version":"117.0.0.0","os_version":"10","referrer":"","referring_domain":"","referrer_current":"","referring_domain_current":"","release_channel":"stable","client_build_number":9999,"client_event_source":None}).encode()).decode()
    