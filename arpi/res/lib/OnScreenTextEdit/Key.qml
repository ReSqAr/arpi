import QtQuick 2.0
import "../../style"

Rectangle {
    Style{
        id: global_style
    }
    property var keytext : ""
    property var keyid : ""
    
    color: focus ? global_style.background_color_focus : global_style.background_color
    
    border.color: "black"
    border.width: 5
    
    Text {
        anchors.fill: parent
        fontSizeMode: Text.Fit
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        text: keytext
        font.pixelSize: 1000
        color: parent.focus ? global_style.text_color_focus : global_style.text_color
    }

    onFocusChanged:{
        if( activeFocus ){
            root.selected(keyid)
        }
    }

    
    Keys.onReturnPressed: {
        root.keyinput(keyid)
    }
    
}
