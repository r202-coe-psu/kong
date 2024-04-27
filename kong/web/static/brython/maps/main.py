from datetime import datetime, timezone, timedelta

from browser import ajax, document, html, window, timer
import javascript as js

from .map import Map


class MainMap(Map):
    def __init__(
        self,
        center,
        zoom,
        min_zoom,
        lang_code,
    ):
        super().__init__(center, zoom, min_zoom)

        self.lang_code = lang_code

        self.markers_layer = {}
        self.gimsin_markers = {}
        self.gimsin_marker_layers = {}

        self.gimsin_view_url = "/gimsins/{gimsin_id}"

    async def render(self):
        self.map.on(
            "click", lambda ev: print(f"location: {ev.latlng.lat}, {ev.latlng.lng}")
        )  # map clicked will print mouse location

    async def update(self, data):
        await self.update_gimsin_markers(data)

    def remove_all_gimsin_marker(self, marker_id):
        if marker_id in self.gimsin_marker_layers.keys():
            self.map.removeLayer(self.gimsin_marker_layers.get(marker_id))

    def set_all_gimsin_marker(self, marker_id):
        if marker_id in self.gimsin_marker_layers.keys():
            self.gimsin_marker_layers[marker_id] = self.leaflet.layerGroup(
                self.markers_layer[marker_id]
            ).addTo(self.map)

    def on_click_gimsin(self, gimsin_id):
        url = self.gimsin_view_url.format(gimsin_id=gimsin_id)
        window.open(url)

    async def get_obj_name(self, obj):
        name = obj["name"]
        for key in ["name_zh", "name_en"]:
            if obj[key]:
                name = f"{name} | {obj[key]}"

        return name

    async def update_gimsin_markers(self, gimsins):

        markers = []

        for gimsin in gimsins:
            image_html = ""
            if gimsin["cover_image_url"]:
                image_html = f"""<img class="ui medium image" src="{ gimsin['cover_image_url'] }" style="max-height:150px;overflow: hidden;">"""

            gimsin_name = await self.get_obj_name(gimsin)
            shrine_name = await self.get_obj_name(gimsin["shrine"])
            kong_name = await self.get_obj_name(gimsin["kong"])

            tooltip_detail = f"""
                <div style="width:250px;">
                   <h3>{ gimsin_name }</h3>
                   <div>
                        { image_html }
                        <div class="ui divider"></div>
                        <div class="ui large text">
                            <i class="torii gate icon"></i> {kong_name} <br/>
                            <i class="yin yang icon"></i> {shrine_name} <br/>
                        <div>
                   </div>
                </div>
                """

            coordinates = gimsin["coordinates"]["coordinates"]
            red_icon = self.leaflet.divIcon(
                dict(
                    html="""<i class="ui map marker alternate icon fitted huge red"
                    style="position:absolute;left:-0.8rem;top:-2.2rem">
                    </i>""",
                    className="dummy",
                )
            )

            gimsin_marker = self.leaflet.marker(
                coordinates,
                dict(
                    icon=red_icon,
                    gimsin_id=gimsin["id"],
                ),
            )

            marker = (
                gimsin_marker.bindTooltip(
                    tooltip_detail,
                    {"offset": (0, 30), "className": "tooltip-marker"},
                )
                .addTo(self.map)
                .on(
                    "click",
                    lambda e: self.on_click_gimsin(e.sourceTarget.options.gimsin_id),
                )
            )

            markers.append(marker)
            self.gimsin_markers[gimsin["id"]] = marker
            marker.setTooltipContent(tooltip_detail)

        self.markers_layer["gimsins"] = markers
        layer = self.gimsin_marker_layers.get("gimsins")

        if not layer:
            print(f"add layer", "gimsins")
            self.gimsin_marker_layers["gimsins"] = self.leaflet.layerGroup(
                self.markers_layer["gimsins"]
            ).addTo(self.map)
