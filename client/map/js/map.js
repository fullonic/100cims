const terrain_tails =
  "https://stamen-tiles-{s}.a.ssl.fastly.net/terrain/{z}/{x}/{y}.png";
const attribution =
  "Map tiles by <a href='http://stamen.com'>Stamen Design</a>, under <a href='http://creativecommons.org/licenses/by/3.0'>CC BY 3.0</a>. Data by <a href='http://openstreetmap.org'>OpenStreetMap</a>, under <a href='http://www.openstreetmap.org/copyright'>ODbL</a>";

const osm_tiles = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png?{foo}";
var mymap = L.map("mapid").setView([41.0, 1.3], 8);
L.tileLayer(terrain_tails, {
  foo: "bar", attribution: attribution,
  maxZoom: 18,
  // tileSize: 5,
}).addTo(
  mymap
);
