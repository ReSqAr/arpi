 
import QtQuick 2.5
import QtQuick.VirtualKeyboard 1.0

InputPanel {
    id: inputPanel
    visible: active
    y: active ? parent.height - inputPanel.height : parent.height
    anchors.left: parent.left
    anchors.right: parent.right
}
