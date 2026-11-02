(function () {
  var el = document.getElementById("access-map");
  if (!el || typeof L === "undefined") return;

  var venue = {
    name: "会場 · 岡崎公園（平安神宮前）",
    nameEn: "Venue · Okazaki Park",
    lat: 35.0142667,
    lng: 135.7828559,
    kind: "venue"
  };

  var stops = [
    {
      name: "岡崎公園　美術館・平安神宮前",
      nameEn: "Okazaki Koen / Bijutsukan, Heian Jingu-mae",
      lat: 35.0123428,
      lng: 135.7825848
    },
    {
      name: "岡崎公園　ロームシアター京都・みやこめっせ前",
      nameEn: "Rohm Theatre Kyoto / Miyakomesse-mae",
      lat: 35.0135884,
      lng: 135.7806229
    },
    {
      name: "東山二条",
      nameEn: "Higashiyama Nijo",
      lat: 35.0130469,
      lng: 135.7782755
    }
  ];

  var map = L.map(el, {
    scrollWheelZoom: false,
    attributionControl: true
  });

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
  }).addTo(map);

  function icon(kind) {
    var cls = kind === "venue" ? "map-pin map-pin--venue" : "map-pin map-pin--stop";
    var label = kind === "venue" ? "会場" : "バス";
    return L.divIcon({
      className: "map-pin-wrap",
      html: '<span class="' + cls + '">' + label + "</span>",
      iconSize: [52, 28],
      iconAnchor: [26, 28],
      popupAnchor: [0, -24]
    });
  }

  var bounds = [];

  function addMarker(place, kind) {
    var m = L.marker([place.lat, place.lng], { icon: icon(kind) }).addTo(map);
    var gmaps =
      "https://www.google.com/maps?q=" +
      encodeURIComponent(place.lat + "," + place.lng) +
      "&ll=" +
      place.lat +
      "," +
      place.lng +
      "&z=18&hl=ja";
    m.bindPopup(
      "<strong>" +
        place.name +
        "</strong><br><span lang=\"en\">" +
        place.nameEn +
        '</span><br><a href="' +
        gmaps +
        '" target="_blank" rel="noopener">Googleマップで開く</a>'
    );
    bounds.push([place.lat, place.lng]);
  }

  addMarker(venue, "venue");
  stops.forEach(function (s) {
    addMarker(s, "stop");
  });

  map.fitBounds(bounds, { padding: [36, 36], maxZoom: 16 });
})();
