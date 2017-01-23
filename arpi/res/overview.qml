import QtQuick 2.0

// Grid {
//     id: root
//     width: 300; height: 300
//     columns: 1
// 
//     signal activated(string id)
//     signal read(string text)
//     
//     Rectangle {
//         id: topLeft
//         width: root.width * 0.5
//         height: root.height * 0.5
//         color: focus ? "red" : "lightgray"
//         focus: true
//         border.width: root.width * 0.05
// 
//         KeyNavigation.right: topRight
//         KeyNavigation.down: bottomLeft
//         Text {
//             anchors.centerIn: parent
//             text: "The string I want to display"
//         }
//         Keys.onReturnPressed: {
//             root.activated(topLeft)
//         }
//     }
// 
//     Rectangle {
//         id: topRight
//         width: root.width * 0.5
//         height: root.height * 0.5
//         color: focus ? "red" : "lightgray"
//         border.width: root.width * 0.05
// 
//         KeyNavigation.left: topLeft
//         KeyNavigation.down: bottomRight
//     }
// 
//     Rectangle {
//         id: bottomLeft
//         width: root.width * 0.5
//         height: root.height * 0.5
//         color: focus ? "red" : "lightgray"
//         border.width: root.width * 0.05
// 
//         KeyNavigation.right: bottomRight
//         KeyNavigation.up: topLeft
//     }
// 
//     Rectangle {
//         id: bottomRight
//         width: root.width * 0.5
//         height: root.height * 0.5
//         color: focus ? "red" : "lightgray"
//         border.width: root.width * 0.05
// 
//         KeyNavigation.left: bottomLeft
//         KeyNavigation.up: topRight
//     }
// } 

Rectangle {
    id: root

    // signal which controls which panel is selected
    signal activated(string id)

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
            border.width: 2
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
