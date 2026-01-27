import QtQuick
import QtPositioning
import QtLocation

Item {
    id: root

    property var mapPins: ({})
    property string selectedPinUid: ""

    MapView {
        id: view
        anchors.fill: parent
        focus: true


        TapHandler {
            acceptedButtons: Qt.LeftButton
            onTapped: (event) => {
                root.selectedPinUid = ""   // deselect pins
            }
        }

        map {
            id: map

            plugin: Plugin {
                name: "osm"
                parameters: [
                    PluginParameter {
                        name: "osm.mapping.providersrepository.disabled"
                        value: true
                    },
                    PluginParameter {
                        name: "osm.mapping.cache.directory"
                        value: cachePath
                    }
                ]
            }

            center: QtPositioning.coordinate(0.0, 0.0)
            zoomLevel: 5
        }

        Shortcut {
            sequences: [ StandardKey.ZoomIn ]
            enabled: view.map.zoomLevel < view.map.maximumZoomLevel
            onActivated: view.map.zoomLevel = Math.round(view.map.zoomLevel + 1)
        }

        Shortcut {
            sequences: [ StandardKey.ZoomOut ]
            enabled: view.map.zoomLevel > view.map.minimumZoomLevel
            onActivated: view.map.zoomLevel = Math.round(view.map.zoomLevel - 1)
        }


        Component {
            id: markerComponent

            MapQuickItem {
                id: marker

                property string uid: ""
                property string title: ""
                property string subtitle: ""

                coordinate: QtPositioning.coordinate(0.0, 0.0)
                anchorPoint.x: 5
                anchorPoint.y: 5
                visible: true
                z: 100

                sourceItem: Item {
                    Rectangle {
                        id: pinDot
                        width: 10
                        height: 10
                        radius: 5
                        border.width: 1
                        color: root.selectedPinUid === marker.uid ? "blue" : "red"

                        MouseArea {
                            anchors.centerIn: parent
                            width: pinDot.width + 10
                            height: pinDot.height + 10
                            onClicked: {
                                root.selectedPinUid = marker.uid
                                bridge.pinClicked(marker.uid)
                            }
                        }
                    }

                    Column {
                        anchors.horizontalCenter: pinDot.horizontalCenter
                        anchors.bottom: pinDot.top
                        spacing: 0

                        Text {
                            text: marker.title
                            font.bold: true
                            color: root.selectedPinUid === marker.uid ? "blue" : "black"
                        }

                        Text {
                            text: marker.subtitle
                            font.pointSize: 10
                            color: root.selectedPinUid === marker.uid ? "blue" : "gray"
                        }
                    }
                }
            }
        }
    }

    function setCenter(lat, lon) {
        view.map.center = QtPositioning.coordinate(lat, lon)
    }

    function getCenter() {
        return "LatLng(" + view.map.center.latitude + "," + view.map.center.longitude + ")"
    }

    function setZoom(z) {
        view.map.zoomLevel = z
    }

    function getZoom() {
        return view.map.zoomLevel
    }

    function addPin(uid, lat, lon, title, subtitle) {
        if (mapPins[uid])
            return

        var obj = markerComponent.createObject(view.map, {
            uid: uid,
            coordinate: QtPositioning.coordinate(lat, lon),
            title: title || "",
            subtitle: subtitle || ""
        })
        view.map.addMapItem(obj)

        mapPins[uid] = obj
        return
    }

    function updatePin(uid, lat, lon, title, subtitle) {
        var m = mapPins[uid]
        if (!m)
            return

        if (lat !== undefined && lon !== undefined)
            m.coordinate = QtPositioning.coordinate(lat, lon)

        if (title !== undefined) m.title = title
        if (subtitle !== undefined) m.subtitle = subtitle
    }

    function removePin(uid) {
        var m = mapPins[uid]
        view.map.removeMapItem(m)
        m.destroy()
    }

    function listPins() {
        var arr = "Array["
        for (var k in view.map.mapItems)
            arr += ","
        return arr + "]"
    }

    function getMapRegionString() {
        var topLeft = map.toCoordinate(Qt.point(0, 0))
        var bottomRight = map.toCoordinate(Qt.point(map.width, map.height))
        return topLeft.latitude + "," + topLeft.longitude + "," +
        bottomRight.latitude + "," + bottomRight.longitude
    }
}
