/* context_map.js */

var MTID = 'aw';
var infoWindow = new google.maps.InfoWindow();
var map = null;
var where = null;
var rWhere = null;
var roughOverlays = [];
var contextOverlays = [];
var p_neighbors = null;

var worldBounds = new google.maps.LatLngBounds(
  new google.maps.LatLng(-90.0, -180.0), new google.maps.LatLng(90.0, 180.0));

var placeIcon = new google.maps.MarkerImage(
    "http://google-maps-icons.googlecode.com/files/justice.png");

var cloudIcon = new google.maps.MarkerImage(
    "http://atlantides.org/images/cloud-marker.png",
    null,
    null,
    new google.maps.Point(34, 29)
    );

function getJSON(rel) {
  var documentNode = document;
  var linkNode = documentNode.evaluate(
      '//link[@rel="' + rel + '" and @type="application/json"]',
      documentNode,
      null,
      XPathResult.FIRST_ORDERED_NODE_TYPE,
      null).singleNodeValue;
  if (linkNode != null) {
    var uri = linkNode.getAttribute("href");
    var json = unescape(uri.split(',').pop());
    return jq.parseJSON(json);
  }
  else {
    return null;
  }
}

function getKML(rel) {
  var documentNode = document;
  var linkNode = documentNode.evaluate(
      '//link[@rel="' + rel 
        + '" and @type="application/vnd.google-earth.kml+xml"]',
      documentNode,
      null,
      XPathResult.FIRST_ORDERED_NODE_TYPE,
      null).singleNodeValue;
  if (linkNode != null) {
    var uri = linkNode.getAttribute("href");
    return uri;
  }
  else {
    return null;
  }
}

function getBounds(collection) {
  if (collection.hasOwnProperty('bbox') == true) {
    return collection.bbox;
  }
  else {
    return null;
  }
}

function clearContextOverlays() {
  if (contextOverlays) {
    for (var i=0; i<contextOverlays.length; i++) {
      contextOverlays[i].setMap(null);
      }
    }
  }

function showContextOverlays() {
  if (contextOverlays) {
    for (var i=0; i<contextOverlays.length; i++) {
      contextOverlays[i].setMap(map);
    }
  }
}

function deleteContextOverlays() {
  if (contextOverlays) {
    for (var i=0; i<contextOverlays.length; i++) {
      contextOverlays[i].setMap(null);
    }
    contextOverlays.length = 0;
  }
}

function showRoughOverlays() {
  if (roughOverlays) {
    for (var i=0; i<roughOverlays.length; i++) {
      roughOverlays[i].setMap(map);
    }
  }
}

function popupKMLNeighbor(evt) {
  /* Uses the global info window */
  var msg = document.createElement("div");
  msg.setAttribute("style", "overflow:auto");
  var head = document.createElement("h3");
  var tail = document.createElement("p");
  var details = document.createElement("a");
  details.setAttribute("href", evt.featureData.author.uri);
  jq(details).text("Details");
  jq(tail).append(details);
  jq(head).text(evt.featureData.name);
  jq(msg).append(head);
  jq(msg).append(unescape(unescape(evt.featureData.description)));
  jq(msg).append(tail);
  infoWindow.close();
  infoWindow.setOptions({position: evt.latLng, content: msg});
  infoWindow.open(map);
}

function popupContext(context) {
  /* Uses the global info window */
  var msg = document.createElement("div");
  msg.setAttribute("style", "overflow:auto");
  var head = document.createElement("h3");
  var tail = document.createElement("p");
  var details = document.createElement("a");
  details.setAttribute("href", context.link);
  jq(details).text("Details");
  jq(tail).append(details);
  jq(head).text(context.title);
  jq(msg).append(head);
  jq(msg).append(context.description);
  jq(msg).append(tail);
  infoWindow.close();
  infoWindow.setOptions({position: context.position, content: msg});
  infoWindow.open(map);
}

function registerFeatureClick(marker, xy, properties) {
  google.maps.event.addListener(
    marker, 'click', function(e) {
      popupContext({
        position: xy,
        title: properties.title,
        link: properties.link,
        description: properties.description
      });
    });
}

function registerMarkerClick(marker, properties) {
  google.maps.event.addListener(
    marker, 'click', function(e) {
      popupContext({
        position: marker.getPosition(),
        title: properties.title,
        link: properties.link,
        description: properties.description
      });
    });
}

function registerCloudMouseover(marker, box) {
  google.maps.event.addListener(
    marker, 'mouseover', function(e) {
      box.setMap(map);
    });
}

function registerCloudMouseout(marker, box) {
  google.maps.event.addListener(
    marker, 'mouseout', function(e) {
      box.setMap(null);
    });
}

function cloudPosition(feature, mapBounds) {
  // Cloud's anchor point approaches context origin as we zoom in,
  // approaches other end of the line as we zoom out
  var coords = feature.geometry.coordinates;
  var bbox = feature.bbox;
  var mapLL = mapBounds.getSouthWest();
  var mapUR = mapBounds.getNorthEast();
  var mapDiameter = Math.sqrt(
    (mapUR.lat() - mapLL.lat())*(mapUR.lat() - mapLL.lat()) +
    (mapUR.lng() - mapLL.lng())*(mapUR.lng() - mapLL.lng()));
  var diameter = Math.sqrt(
    (bbox[2]-bbox[0])*(bbox[2]-bbox[0]) +
    (bbox[3]-bbox[1])*(bbox[3]-bbox[1]));
  var scale = mapDiameter/diameter;
  var c = 0.8;
  var f = c*scale/2.0;
  f = Math.min(1.0, f);
  var cloudLat = (1.0-f)*coords[0][1] + f*coords[1][1];
  var cloudLon = (1.0-f)*coords[0][0] + f*coords[1][0];
  return new google.maps.LatLng(cloudLat, cloudLon);
}

function initialize() {
  /*
   * 1. Get the KML of precisely located neighbors, register mouse listeners
   * 2. Populate a global array of roughly located neighbor aggregations, 
   *    with mouse listeners
   * 3. Populate a global array of context features, with mouse listeners
   * 4. Render map (Precise, rough, context)
   * 5. Register bounds change listener that redraws rough markers
   */

  var mapOptions = {
    mapTypeId: google.maps.MapTypeId.TERRAIN
  };

  map = new google.maps.Map(
          document.getElementById("map"),
          mapOptions);

  var p_kml = getKML("nofollow alternate p-neighbors");
  if (p_kml != null && p_kml.substring(0, 16) != "http://localhost") {
    p_neighbors = new google.maps.KmlLayer(
        p_kml, {preserveViewport: true, suppressInfoWindows: true});
    google.maps.event.addListener(
      p_neighbors, 'click', function(evt) {
        popupKMLNeighbor(evt);
      });
    google.maps.event.addListener(
      p_neighbors, 'metadata_changed', function() {
        var pBounds = p_neighbors.getDefaultViewport();
        if (
          pBounds != null && 
          !pBounds.equals(worldBounds) &&
          map.getBounds() != null) {
          map.fitBounds(pBounds.union(map.getBounds()));
        }
      });
  }

  rWhere = getJSON('r-where');
  for (var i=0; i<rWhere.features.length; i++) {
    var f = rWhere.features[i];
    var geom = f.geometry;
    if (geom == null) {
      continue;
    }
    if (f.type == "pleiades.stoa.org.BoxBoundedRoughFeature") {
      var cloudMark = new google.maps.Marker({
                position: null, 
                icon: cloudIcon,
                });
      var cloudBox = new google.maps.Rectangle({
          bounds: new google.maps.LatLngBounds(
            new google.maps.LatLng(f.bbox[1], f.bbox[0]),
            new google.maps.LatLng(f.bbox[3], f.bbox[2])),
          strokeColor: "#cc6633",
          strokeOpacity: 0.5,
          strokeWeight: 2,
          strokeColor: "#cc6633",
          fillOpacity: 0.25
          });
      registerMarkerClick(cloudMark, f.properties);
      registerCloudMouseover(cloudMark, cloudBox);
      registerCloudMouseout(cloudMark, cloudBox);
      roughOverlays.push(cloudMark);
    }
  }

  where = getJSON('where');
  for (var i=0; i<where.features.length; i++) {
    var f = where.features[i];
    var geom = f.geometry;
    if (geom == null) {
      continue;
    }
    var relation = null;
    if (geom.hasOwnProperty('relation')) {
      relation = geom.relation;
    }
    var color = "#0000FF";
    var opacity = 1.0;
    if (relation != null) {
      opacity = 0.5;
    }
    if (f.type == "Feature") {
      if (f.geometry.type == 'Point') {
        var xy = new google.maps.LatLng(
                  geom.coordinates[1], geom.coordinates[0]);
        var whereMark = new google.maps.Marker({
                  position: xy, 
                  icon: placeIcon,
                  });
        registerMarkerClick(whereMark, f.properties);
        contextOverlays.push(whereMark);
      }
      else if (geom.type == 'LineString') {
        var coords = [];
        var cx = 0.0;
        var cy = 0.0;
        var v = null;
        for (var j=0; j<geom.coordinates.length; j++) {
          v = geom.coordinates[j];
          coords.push(new google.maps.LatLng(v[1], v[0]));
          cx += v[0];
          cy += v[1];
        }
        cx = cx/coords.length;
        cy = cy/coords.length;
        xy = new google.maps.LatLng(cy, cx);
        var polyline = new google.maps.Polyline({
          path: coords,
          strokeColor: color,
          strokeOpacity: opacity,
          strokeWeight: 3,
          });
        registerFeatureClick(
            polyline, new google.maps.LatLng(cy, cx), f.properties);
        contextOverlays.push(polyline);
      }
      else if (f.geometry.type == 'Polygon') {
        var exterior = f.geometry.coordinates[0];
        var ring = [];
        var cx = 0.0;
        var cy = 0.0;
        var v = null;
        for (var j=0; j<exterior.length; j++) {
          v = exterior[j];
          ring.push(new google.maps.LatLng(v[1], v[0]));
          cx += v[0];
          cy += v[1];
        }
        cx = cx/exterior.length;
        cy = cy/exterior.length;
        var polygon = new google.maps.Polygon({
          paths: ring,
          strokeColor: color,
          strokeOpacity: opacity,
          strokeWeight: 3,
          strokeColor: color,
          fillOpacity: opacity/2.0
          });
        registerFeatureClick(polygon, new google.maps.LatLng(cy, cx), f.properties);
        contextOverlays.push(polygon);
      }
    }
  }

  google.maps.event.addListener(
    map, 'bounds_changed', function() {
      var mapBounds = map.getBounds();
      for (i=0; i<roughOverlays.length; i++) {
        var marker = roughOverlays[i];
        marker.setMap(null);
        marker.setPosition(cloudPosition(rWhere.features[i], mapBounds));
        marker.setMap(map);
      }
    });

  var bounds = getBounds(where);
  var latlng = new google.maps.LatLng(0.0, 0.0);
  var zoom = 1;

  if (bounds != null) {
    var latlng = new google.maps.LatLng(
      (bounds[1]+bounds[3])/2.0, (bounds[0]+bounds[2])/2.0);
    zoom = 10;
  }

  map.setCenter(latlng);
  map.setZoom(zoom);

  if (bounds != null && (bounds[2]-bounds[0])*(bounds[3]-bounds[1]) >= 0.001) {
    map.fitBounds(
      new google.maps.LatLngBounds(
        new google.maps.LatLng(bounds[1], bounds[0]), 
        new google.maps.LatLng(bounds[3], bounds[2])));
  }

  if (p_neighbors != null) {
    p_neighbors.setMap(map);
  }

  showRoughOverlays();
  showContextOverlays();
}

function overlayIndexOf(elem) {
  for (var i=0;i<contextOverlays.length;i++) {
    var f = where.features[i];
    if (f.id == elem.id) {
      return i;
    }
  }
  return -1;
}

function raiseInMap() {
  var i = overlayIndexOf(this);
  var marker = contextOverlays[i];
  var f = where.features[i];
  var properties = f.properties;
  var geom = f.geometry;
  var xy = null;
  if (geom.type == 'Point') {
    xy = new google.maps.LatLng(geom.coordinates[1], geom.coordinates[0]);
  }
  else if (geom.type == 'LineString') {
    var coords = geom.coordinates;
    var cx = 0.0;
    var cy = 0.0;
    var v = null;
    for (var j=0; j<coords.length; j++) {
      cx += v[0];
      cy += v[1];
    }
    cx = cx/coords.length;
    cy = cy/coords.length;
    xy = new google.maps.LatLng(cy, cx);
  }
  else if (geom.type == 'Polygon') {
    var exterior = geom.coordinates[0];
    var cx = 0.0;
    var cy = 0.0;
    var v = null;
    for (var j=0; j<exterior.length; j++) {
      v = exterior[j];
      cx += v[0];
      cy += v[1];
    }
    cx = cx/exterior.length;
    cy = cy/exterior.length;
    xy = new google.maps.LatLng(cy, cx);
  }
  popupContext({
    position: xy,
    title: properties.title,
    link: properties.link,
    description: properties.description
  });
}

registerPloneFunction(initialize);