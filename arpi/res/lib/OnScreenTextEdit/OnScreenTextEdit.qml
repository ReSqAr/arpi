import QtQuick 2.0
import QtQuick.Layouts 1.3
import "../../style"

Rectangle {
    id: root
    
    Style{
        id: global_style
    }
    
    property var alphabet: "ABCDEFGHIJKLMNOPQRSTUVWXYZ-"
    property var rowCount: 3
    
    // signals
    signal keyinput(string keyid)
    signal selected(string keyid)
    signal back()

    // connect escape to onEscapePressed
    Keys.onEscapePressed: {
        root.back()
    }
    
    // text input logic
    onKeyinput: {
        if( keyid == 'backspace' )
        {
            if( textEdit.text.length > 0 )
                textEdit.text = textEdit.text.slice(0, -1);
        }
        else
        {
            textEdit.text += keyid;
        }
        var text = textEdit.text;
        keyboardgrid.capitalisation = ( 
                                            (text.length == 0)
                                        ||
                                            (text[text.length-1] === ' ')
                                        ||
                                            (text[text.length-1] === '-')
                                      );
    }

    Column{
        Rectangle {
            // centered text edit
            width: root.width
            height: 0.2 * root.height
            
            color: global_style.background_color
            
            Text {
                id: textEdit
                anchors.fill: parent
                fontSizeMode: Text.Fit
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                text: ""
                font.pixelSize: 1000
                color: global_style.text_color
            }
        }
        Rectangle {
            // keyboard (a-z, auto capitalisation, -, backspace, space + special characters (umlaute, accented characters)) 
            id: keyboard
            color: "green"
            width: root.width
            height: 0.8 * root.height
            
            
            Column{
                height: parent.height
                width: parent.width
                spacing: 0
                
                
                GridLayout{
                    id: keyboardgrid
                    height: 0.75 * parent.height
                    width: parent.width
                    columnSpacing: 0
                    rowSpacing: 0
                    columns : Math.ceil( alphabet.length / rowCount )

                    property var capitalisation : false

                    
                    Repeater {
                        model: alphabet.split("")
                        Key{
                            keytext: keyboardgrid.capitalisation ? modelData.toUpperCase() : modelData.toLowerCase()
                            keyid: keyboardgrid.capitalisation ? modelData.toUpperCase() : modelData.toLowerCase()
                            Layout.fillHeight: true
                            Layout.fillWidth: true
                            focus: (index == 0)
                        }
                    }
                    Component.onCompleted: {
                        for( var i = 0; i < alphabet.length; i++ ) {
                            // up
                            var up = i - columns;
                            if( up >= 0 )
                                children[i].KeyNavigation.up = children[up];
                            
                            // left
                            var left = i - 1;
                            if( (i % columns) > 0 )
                                children[i].KeyNavigation.left = children[left];
                        }
                    }
                }
                
                Rectangle {
                    id: keyboardbar
                    height: 0.25 * parent.height
                    width: parent.width
                    
                    Row{
                        height: parent.height
                        width: parent.width
                        Key{
                            id: spacebar
                            height: parent.height
                            width: 0.75 * parent.width
                            keytext: 'Space'
                            keyid: ' '
                            Layout.fillHeight: true
                            Layout.fillWidth: true
                        }
                        Key{
                            id: backspace
                            height: parent.height
                            width: 0.25 * parent.width
                            keytext: 'Backspace'
                            keyid: 'backspace'
                            Layout.fillHeight: true
                            Layout.fillWidth: true
                            KeyNavigation.left: spacebar
                        }
                    }
                    
                    // TODO: finish = enter, reading text in full
                    
                    Component.onCompleted: {
                        for( var i = alphabet.length - (rowCount-1) * keyboardgrid.columns - 1; i >= 0 ; i-- ) {
                            keyboardgrid.children[i+(rowCount-1)*keyboardgrid.columns].KeyNavigation.down = (i / keyboardgrid.columns <= 0.75) ? spacebar : backspace;
                        }
                    }
                }
            }
        }        
    }
}
