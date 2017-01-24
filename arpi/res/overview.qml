import QtQuick 2.0
import "style"

Rectangle {
    id: root
    
    Style{
        id: global_style
    }
    
    // signals
    signal activated(int appid)
    signal selected(int appid)
    
    // cache row count
    property var rowCount : listView.model.rowCount()
    
    // delegate
    Component {
        id: appDelegate
        Rectangle {
            id: wrapper
            
            // cache model data
            property var c_index : index
            property var c_appname : display

            width: root.width
            height: Math.max(root.height / rowCount, 0.2 * root.height)
            
            color: wrapper.ListView.isCurrentItem ? global_style.background_color_focus : global_style.background_color
            
            Text {
                anchors.fill: parent
                fontSizeMode: Text.Fit
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                text: c_appname
                font.pixelSize: 1000
                color: wrapper.ListView.isCurrentItem ? global_style.text_color_focus : global_style.text_color
            }
            Keys.onReturnPressed: {
                root.activated(c_index)
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
        onCurrentItemChanged: {
            root.selected(currentIndex)
        }
    }
}
