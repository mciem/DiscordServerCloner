from random      import choices, randint
from functools   import wraps
from threading   import Thread

from tls_client.response import Response

from .client import buildClient

import json

def response(func):
    """
    Convert response to a dict
    """
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        data: Response = func(*args, **kwargs)
        
        response = {
            "success": data.status_code in (200,201,203,204),
            "status_code": data.status_code
        }
        
        try:   response["json"] = data.json()
        except json.JSONDecodeError: response["json"] = data.text
        
        return response
    
    return wrapper

class Discord:
    def __init__(
        self, 
        token: str,
        proxy: str,
        build_number: str,
        x_super_prop: str,
    ) -> None:
        
        self.client  = buildClient(proxy)
        
        self.build_n = build_number
        self.super_p = x_super_prop
        
        self.initSession(token)
    
    def __websocket(
            self,
            token: str
        ):
        
        self.ws = DiscordSocket(token, self.build_n)
        self.ws.run()
    
    def initSession(
            self,
            token: str,
        ):
        
        self.client.headers["authorization"] = token
        self.client.headers["x-super-properties"] = self.super_p
        self.client.headers["referer"] = "https://discord.com/channels/@me"
        
        #Thread(target=self.__websocket, args=(token,)).run()
    
    @response
    def sendMessage(
            self,
            channelID: str,
            guildID: str,
            message: str
        ):
        
        headers = self.client.headers.copy()
        headers["referer"] = f"https://discord.com/channels/{guildID}/{channelID}"
        
        return self.client.post(
            f"https://discord.com/api/v9/channels/{channelID}/messages",
            headers=headers,
            json={
                "content": message,
                "tts": False
            }
        )
    
    @response
    def createServer(
            self,
            name: str
        ):
        
        return self.client.post(
            "https://discord.com/api/v9/guilds",
            json={
                "channels": [],
                "guild_template_code": "2TffvPucqHkN",
                "icon": None,
                "name": name,
                "system_channel_id": None
            }
        )
    
    @response
    def createChannel(
            self,
            guildID: str,
            rJson: dict,
        ):
        
        
        return self.client.post(
            f"https://discord.com/api/v9/guilds/{guildID}/channels",
            json=rJson
        )
    
    @response
    def deleteChannel(
            self,
            guildID: str,
            channelID: str,
        ):
        
        headers = self.client.headers.copy()
        headers["referer"] = f"https://discord.com/channels/{guildID}/{channelID}"
        
        return self.client.delete(
            f"https://discord.com/api/v9/channels/{channelID}",
            headers=headers,
        )  
    
    @response
    def getChannels(
            self,
            guildID: str,
        ):
        
        return self.client.get(
            f"https://discord.com/api/v9/guilds/{guildID}/channels"
        )
    
    @response
    def getRoles(
            self,
            guildID: str
        ):
        
        return self.client.get(
            f"https://discord.com/api/v9/guilds/{guildID}/roles"
        )
    
    @response
    def createRole(
            self,
            guildID: str,
            rJson: dict,
        ):
        
        return self.client.post(
            f"https://discord.com/api/v9/guilds/{guildID}/roles",
            json=rJson,
        )
    
    @response
    def changeRolePostition(
            self,
            guildID: str,
            roleID: str,
            position: int,
        ):
        
        return self.client.patch(
            f"https://discord.com/api/v9/guilds/{guildID}/roles",
            json=[
                {
                    "id": roleID,
                    "position": position,
                },
            ]
        )
    
    @response
    def changeChannelPostition(
            self,
            guildID: str,
            channelID: str,
            position: int,
            parentID: str
        ):
        
        return self.client.patch(
            f"https://discord.com/api/v9/guilds/{guildID}/channels",
            json=[
                {
                    "id": channelID,
                    "position": position,
                    "parent_id": parentID
                },
            ]
        )