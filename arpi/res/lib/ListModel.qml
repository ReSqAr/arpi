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
        root.back();
    }
    
    // delegate
    Component {
        id: listDelegate
        
        Rectangle {
            id: wrapper

            width: root.width
            height: Math.max(root.height / listView.model.length, root.height / 5)
            
            color: wrapper.ListView.isCurrentItem ? global_style.background_color_focus : global_style.background_color
            
            Text {
                anchors.fill: parent
                fontSizeMode: Text.Fit
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                text: modelData
                font.pixelSize: 1000
                color: wrapper.ListView.isCurrentItem ? global_style.text_color_focus : global_style.text_color
            }
            Keys.onReturnPressed: {
                root.activated(index);
            }
        }
    }

    // list view
    ListView {
        id: listView
        anchors.fill: parent
        model: stringList
        delegate: listDelegate
        focus: true
        //keyNavigationEnabled: true
        keyNavigationWraps: true
        
        onCurrentIndexChanged: {
            root.selected(currentIndex);
            positionViewAtIndex(currentIndex, ListView.Center);
        }
    }
}
