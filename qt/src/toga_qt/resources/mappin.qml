import QtQuick
import QtPositioning
import QtLocation

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
