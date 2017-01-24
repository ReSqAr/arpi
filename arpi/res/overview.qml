import QtQuick 2.0

Rectangle {
    id: root

    // signal which controls which panel is selected
    signal activated(string appid)

    
    property var rowCount : listView.model.rowCount()
    
    // delegate
    Component {
        id: appDelegate
        Rectangle {
            id: wrapper
            width: root.width
            //height: Math.max(root.height / appModel.rowCount(), 0.2 * root.height) //crashes?
            height: Math.max(root.height / rowCount, 0.2 * root.height)
            color: wrapper.ListView.isCurrentItem ? "red" : "lightgray"
            Text {
                anchors.centerIn: parent
                text: appname
            }
            Keys.onReturnPressed: {
                root.activated(appid)
            }
        }
    }

    // list view
    ListView {
        id: listView
        anchors.fill: parent
        model: appModel
        delegate: appDelegate
        focus: true
    }
}
