import QtQuick 2.0

Rectangle {
    id: root

    // signal which controls which panel is selected
    signal activated(string appid)

    // empty model
    ListModel {
        id: appModel
    }
    
    // function which adds apps to the list model
    function appModel_append( app ){
        appModel.append({appname : app[0], appid : app[1]})
    }
    
    // delegate
    Component {
        id: appDelegate
        Rectangle {
            id: wrapper
            width: root.width
            height: root.height / appModel.count
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
