import json

from discord import Client, Member
from datetime import datetime, timedelta

from typing import Dict

class BansDataController():
    def __init__(self):
        self.bansFile: str = "bans.json"

    async def get_bans(self) -> Dict[str, any]:
        try:
            with open(self.bansFile, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, IOError):
            with open(self.bansFile, 'a+') as f:
                json.dump({"ban-id": 0, "list": {}}, f, ensure_ascii=True, indent=4)

    async def save(self, data: Dict[str, any]) -> None:
        with open(self.bansFile, 'w') as f:
            json.dump(data, f, ensure_ascii=True, indent=4)

class Ban():
    def __init__(self):
        self.bansData: BansDataController = BansDataController()

    async def temp(self, client: Client, member: Member, admin, reason, time) -> None:
        bans: Dict[str, any] = await self.bansData.get_bans()

        if not member.guild_permissions.administrator:
            if not str(member.id) in bans['list']:
                bans['ban-id'] += 1

                bans['list'].update({
                    bans['ban-id']: {
                        "member-name": member.name,
                        "member-id": member.id,
                        "unban-date": str(datetime.now() + timedelta(seconds=time)),
                        "when-banned": str(datetime.now()),
                        "reason": reason,
                        "active": True,
                        "banned-by": admin
                    }
                })

            await self.bansData.save(data=bans)
            await member.ban(reason=f"{reason}  duration: {time/60} in minutes")

