import QtQuick 2.0
import "../style"

Rectangle {
    id: root
    
    Style{
        id: global_style
    }
    
    // signals
    signal activated(int index)
    signal selected(int index)
    signal back()
    
    // connect escape to onEscapePressed
    Keys.onEscapePressed: {
        root.back()
    }
        
    // cache row count
    property var rowCount : listView.model.rowCount()
    
    // delegate
    Component {
        id: listDelegate
        
        Rectangle {
            id: wrapper
            
            // cache model data
            property var c_index : index
            property var c_text : display

            width: root.width
            height: Math.max(root.height / rowCount, root.height / 5)
            
            color: wrapper.ListView.isCurrentItem ? global_style.background_color_focus : global_style.background_color
            
            Text {
                anchors.fill: parent
                fontSizeMode: Text.Fit
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                text: c_text
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
        model: listModel
        delegate: listDelegate
        focus: true
        onCurrentItemChanged: {
            root.selected(currentIndex)
        }
    }
}
