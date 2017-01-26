import QtQuick 2.0
import "../../../res/style"

Column {
    id: root

    Style{
        id: global_style
    }
    
    // signals
    signal activated(int appid)
    signal selected(int appid)
    
    Rectangle {
        id: row1
        width: root.width
        height: root.height * 0.5
        color: focus ? global_style.background_color_focus : global_style.background_color
        focus: true
        border.width: root.width * 0.05

        Text {
            anchors.fill: parent
            fontSizeMode: Text.Fit
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            text: "Row1"
            font.pixelSize: 1000
            color: wrapper.ListView.isCurrentItem ? global_style.text_color_focus : global_style.text_color
        }

        KeyNavigation.down: row2
        Keys.onReturnPressed: {
            root.activated(row1)
        }
    }

    Rectangle {
        id: row2
        width: root.width
        height: root.height * 0.5
        color: focus ? global_style.background_color_focus : global_style.background_color
        border.width: root.width * 0.05

        Text {
            anchors.fill: parent
            fontSizeMode: Text.Fit
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            text: "Row2"
            font.pixelSize: 1000
            color: wrapper.ListView.isCurrentItem ? global_style.text_color_focus : global_style.text_color
        }
        KeyNavigation.up: row1
        KeyNavigation.down: row3
        Keys.onReturnPressed: {
            root.activated(row1)
        }
    }

    Rectangle {
        id: row3
        width: root.width
        height: root.height * 0.5
        color: focus ? global_style.background_color_focus : global_style.background_color
        border.width: root.width * 0.05

        Text {
            anchors.fill: parent
            fontSizeMode: Text.Fit
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            text: "Row3"
            font.pixelSize: 1000
            color: wrapper.ListView.isCurrentItem ? global_style.text_color_focus : global_style.text_color
        }
        KeyNavigation.up: row2
        Keys.onReturnPressed: {
            root.activated(row1)
        }
    }



} 
