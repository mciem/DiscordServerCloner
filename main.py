from src.console import Console
from src.discord import Discord
from src.utils   import Utils

from time import sleep

class Cloner:
    def __init__(self) -> None:
        self.cns = Console()
        self.uts = Utils()
        
        self.token = self.cns.log("INP", "token")
        self.guildID = self.cns.log("INP", "guildID")
        self.serverName = self.cns.log("INP", "choose new server name")
        
        self.dc = Discord(self.token, "", 9999, self.uts.buildXSuperProperties(9999))
        
    def clone(self):
        cServerResponse = self.dc.createServer(self.serverName)
        if cServerResponse["success"]:
            cServerJson = cServerResponse["json"]
            serverID = cServerJson["id"]
            
            self.cns.log("SCC", "created server", {"guildID": serverID})
        else:
            self.cns.log("ERR", "failed to create server", {"json": cServerResponse["json"]})
            
            return
        
        cResponse = self.dc.getChannels(serverID)
        if cResponse["success"]:
            channels = cResponse["json"]
            
            self.cns.log("SCC", "got channels from new server", {"amount": len(channels)})
        else:
            self.cns.log("ERR", "failed to get channels from new server", {"json": cResponse["json"]})
            
            return

        for channel in channels:
            dChannelResponse = self.dc.deleteChannel(serverID, channel["id"])
            
            if dChannelResponse["success"]:
                self.cns.log("SCC", "deleted channel in new server", {"name": channel["name"], "id": channel["id"]})
            
            else:
                self.cns.log("ERR", "failed to delete channel in new server", {"json": dChannelResponse["json"]})
            
            sleep(1)
        
        rResponse = self.dc.getRoles(self.guildID)
        if rResponse["success"]:
            roles = rResponse["json"]
            
            self.cns.log("SCC", "got roles", {"amount": len(roles)})
        else:
            self.cns.log("ERR", "failed to get channels", {"json": rResponse["json"]})
            
            return
        
        roles = sorted(roles, key=lambda x: x["position"], reverse=True)
        
        for role in roles:
            rJson = role.copy()
            
            for p in ("id", "icon", "position", "managed", "flags"):
                rJson.pop(p)
            
            rCreateResponse = self.dc.createRole(serverID, rJson)
            if rCreateResponse["success"]:
                rResponseJson = rCreateResponse["json"]
                
                self.cns.log("SCC", "created role", rResponseJson)
            else:
                self.cns.log("ERR", "failed to create role", {"json": rCreateResponse["json"]})
                
                continue
            
            sleep(1)
                    
        
        cResponse = self.dc.getChannels(self.guildID)
        if cResponse["success"]:
            channels = cResponse["json"]
            
            self.cns.log("SCC", "got channels", {"amount": len(channels)})
        else:
            self.cns.log("ERR", "failed to get channels", {"json": cResponse["json"]})
            
            return

        #channels = sorted(channels, key=lambda x: x["position"]) not needed i think
        channels_ord = []

        categories = {}
        for channel in channels:
            if channel["type"] == 4:
                categories[channel["id"]] = channel
                categories[channel["id"]]["channels"] = []
        
        without_category = []
        for channel in channels:
            if channel["type"] != 4:
                if channel["parent_id"] is not None:
                    categories[channel["parent_id"]]["channels"].append(channel)
                else:
                    without_category.append(channel)
        
        for cID, category in categories.items():
            categories[cID]["channels"] = sorted(categories[cID]["channels"], key=lambda x: x["position"])
        
        sortd = sorted(without_category+list(categories.values()), key=lambda x: x["position"])
        for channel in sortd:
            if channel["type"] == 4:
                ch = channel.copy()
                ch.pop("channels")

                channels_ord.append(ch)

                for channel2 in channel["channels"]:
                    channel2["parent_id"] = True
                    channels_ord.append(channel2)
                
            else:
                channel["parent_id"] = False
                channels_ord.append(channel)
            

        parentID = None
        for channel in channels_ord:
            cJson = channel.copy()
            
            if cJson["type"] in (11, 12):
                self.cns.log("DBG", "thread detected, skipping...")
                
                continue
            
            cChannelResponse = self.dc.createChannel(serverID, {
                "type": cJson.get("type"),
                "permission_overwrites": cJson.get("permission_overwrites"),
                "name": cJson.get("name"),
                "topic": cJson.get("topic"),
                "nsfw": cJson.get("nsfw"),
                "bitrate": cJson.get("bitrate"),
                "user_limit": cJson.get("user_limit"),
                "rate_limit_per_user": cJson.get("rate_limit_per_user"),
                "parent_id": parentID if cJson["type"] != 4 and cJson["parent_id"] else None,
                "rtc_region": cJson.get("rtc_region"),
                "video_quality_mode": cJson.get("video_quality_mode"),
                "permissions": cJson.get("permissions")
            })
            
            if cChannelResponse["success"]:
                chann = cChannelResponse["json"]
                
                self.cns.log("SCC", "created channel", chann)
                
                if channel["type"] == 4:
                    parentID = chann["id"]
                    
                    self.cns.log("DBG", "category detected setting parentID", {"id": parentID})
                
            else:
                self.cns.log("ERR", "failed to create channel", {"json": cChannelResponse["json"]})
            
            sleep(1)
        

if __name__ == "__main__":
    clr = Cloner()
    clr.clone()
        