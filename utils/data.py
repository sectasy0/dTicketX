import json
import sys

import asyncio

from typing import Dict
        
class DataController(object):
    def __init__(self):
        self.dataFile: str = "data.json"
        self.settingsFile: str = "settings.json"

    async def get_data(self) -> Dict[str, any]:
        try:
            with open(self.dataFile, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, IOError):
            print("\x1b[1;31m[ERROR]:\x1b[0m data.json file not found, create a new.")
            jsonData: Dict[str, any] = {
                "warns": {},
                "ticket-channel-ids": [],
                "ticket-id-counter": 0,
                "users-with-active-tickets": []
            }
            with open(self.dataFile, 'w') as f:
                json.dump(jsonData, f, ensure_ascii=True, indent=4)
            
            return jsonData

    async def get_settings(self) -> Dict[str, any]:
        try:
            with open(self.settingsFile, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, IOError):
            print("\x1b[1;31m[ERROR]:\x1b[0m settings.json not found, create a new with default data, please fill data with yours")
            jsonSettings: Dict[str, any] = {
                "warns":{
                    "ban-warns-reach": True,
                    "max-warns": 3,
                    "ban-time": 10800
                },
                "channels": {
                    "support-channel-id": "000000000000000000",
                    "support-category-id": "000000000000000000",
                    "support-log-channeld-id": "000000000000000000"
                },
                "support-role": "ADMIN",
                "enable-channel-logger": True
            }

            with open(self.settingsFile, 'w+') as f:
                json.dump(jsonSettings, f, ensure_ascii=True, indent=4)
            
            return jsonSettings

    async def save_data(self, data: dict) -> None:
        with open(self.dataFile, 'w') as f:
            json.dump(data, f, ensure_ascii=True, indent=4)
