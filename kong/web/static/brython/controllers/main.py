# import datetime

from browser import ajax, document, html, window, timer, aio

import javascript as js

from maps import MainMap

# from kongs import kong


class MainController:
    def __init__(self, lang_code):
        self.lang_code = lang_code

        self.get_shrines_url = f"/api/shrines"
        self.get_kongs_url = f"/api/kongs"
        self.get_gimsins_url = f"/api/gimsins"

        self.kongs = dict()
        self.map = None

    async def get_gimsins(self):
        response = await aio.get(self.get_gimsins_url)
        gimsins = js.JSON.parse(response.data)
        await self.map.update(gimsins)

    async def run(self):
        await self.setup()
        await self.get_gimsins()

    async def setup(self):
        # response = await aio.get(self.get_token_url)
        # response = js.JSON.parse(response.data)
        # self.token = response["access_token"]

        # headers = {"Authorization": f"Bearer {self.token}"}
        # response = await aio.get(self.get_system_setting_url, headers=headers)
        # self.system_setting = js.JSON.parse(response.data)

        # center = self.system_setting["center"]["coordinates"]
        # zoom = self.system_setting["zoom"]
        # min_zoom = self.system_setting["min_zoom"]

        zoom = 5
        min_zoom = 0
        self.map = MainMap([10, 100], zoom, min_zoom, self.lang_code)

        await self.map.render()

    def start(self):
        aio.run(self.run())
