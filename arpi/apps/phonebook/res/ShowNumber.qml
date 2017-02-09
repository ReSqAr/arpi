import QtQuick 2.0
import "../../../res/style"

Column {
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
    
    Rectangle {
        id: row1
        width: root.width
        height: root.height * 0.2
        color: focus ? global_style.background_color_focus : global_style.background_color

        Text {
            anchors.fill: parent
            fontSizeMode: Text.Fit
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            text: name
            font.pixelSize: 1000
            color: parent.focus ? global_style.text_color_focus : global_style.text_color
        }
        
        onFocusChanged:{
            if( activeFocus ){
                root.selected(0)
            }
        }
        
        KeyNavigation.down: row2
        Keys.onReturnPressed: {
            root.activated(0)
        }
    }

    Rectangle {
        id: row2
        width: root.width
        height: root.height * 0.8
        color: focus ? global_style.background_color_focus : global_style.background_color
        focus: true

        Text {
            anchors.fill: parent
            fontSizeMode: Text.Fit
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            text: number
            font.pixelSize: 1000
            color: parent.focus ? global_style.text_color_focus : global_style.text_color
        }

        onFocusChanged:{
            if( activeFocus ){
                root.selected(1)
            }
        }
        
        KeyNavigation.up: row1
        Keys.onReturnPressed: {
            root.activated(1)
        }
    }
}
