import QtQuick 2.0
import QtQuick.Layouts 1.3
import "../../style"

Rectangle {
    id: root
    
    Style{
        id: global_style
    }
    
    property var alphabet: "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    property var rowCount: 3
    property var autoCapitalisation: false
    
    // signals
    signal finished(string text)
    signal keyTriggered(string keyid)
    signal selected(string keyid)
    signal back()
    signal reinitialiseKeyboard()

    // connect escape to onEscapePressed
    Keys.onEscapePressed: {
        root.back()
    }
    
    // text input logic
    onKeyTriggered: {
        if( keyid == "enter" )
        {
            root.finished( textEdit.text );
        }
        else if( keyid == 'delete' )
        {
            if( textEdit.text.length > 0 )
                textEdit.text = textEdit.text.slice(0, -1);
        }
        else
        {
            textEdit.text += keyid;
        }
        var text = textEdit.text;
        
        if( autoCapitalisation )
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
            height: 0.3 * root.height
            
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
            width: root.width
            height: 0.7 * root.height
            color: global_style.background_color
            
            Row{
                height: parent.height
                width: parent.width
                spacing: 0
                Column{
                    height: parent.height
                    width: parent.width * keyboardgrid.columns / (keyboardgrid.columns+1)
                    spacing: 0
                    
                    
                    GridLayout{
                        id: keyboardgrid
                        height: 0.75 * parent.height
                        width: parent.width
                        columnSpacing: 0
                        rowSpacing: 0
                        columns : Math.ceil( alphabet.length / rowCount )

                        property var capitalisation : autoCapitalisation

                        
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
                                keytext: qsTr('Space')
                                keyid: ' '
                                Layout.fillHeight: true
                                Layout.fillWidth: true
                            }
                            Key{
                                id: backspace
                                height: parent.height
                                width: 0.25 * parent.width
                                keytext: qsTr('Delete')
                                keyid: 'delete'
                                Layout.fillHeight: true
                                Layout.fillWidth: true
                                KeyNavigation.left: spacebar
                            }
                        }
                    }
                }
                
                
                
                Rectangle {
                    height: parent.height
                    width: parent.width
                    
                    Key{
                        id: enterkey
                        height: parent.height
                        width: parent.width / (keyboardgrid.columns+1)
                        keytext: qsTr('OK')
                        keyid: 'enter'
                    }
                }
            }
        }        
    }
    
    Component.onCompleted: {
        _reinitialiseKeyboard();
    }
    
    onReinitialiseKeyboard: {
        _reinitialiseKeyboard();
    }
    
    function _reinitialiseKeyboard(){
        // keyboard grid
        for( var i = 0; i < alphabet.length; i++ ) {
            // up
            var up = i - keyboardgrid.columns;
            if( up >= 0 )
                keyboardgrid.children[i].KeyNavigation.up = keyboardgrid.children[up];
            
            // left
            var left = i - 1;
            if( (i % keyboardgrid.columns) > 0 )
                keyboardgrid.children[i].KeyNavigation.left = keyboardgrid.children[left];
        }
        
        // spacebar / backspace
        for( var i = alphabet.length; i >= 0 ; i-- ) {
            if( keyboardgrid.children[i].KeyNavigation.down === null ){
                var column = i % keyboardgrid.columns;
                keyboardgrid.children[i].KeyNavigation.down = (column < 0.75*keyboardgrid.columns) ? spacebar : backspace;
            }
        }
        
        // enterkey
        backspace.KeyNavigation.right = enterkey;
        for( var i = alphabet.length; i >= 0 ; i-- ) {
            if( keyboardgrid.children[i].KeyNavigation.right === null )
                keyboardgrid.children[i].KeyNavigation.right = enterkey;
        }
    }
}
