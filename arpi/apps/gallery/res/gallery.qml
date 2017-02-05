import QtQuick 2.0

Image {
    id: 'root'
    
    // signals
    signal back()
    
    // internal state
    property var photos : []
    property var index : 0
    
    // connect escape to onEscapePressed
    Keys.onEscapePressed: {
        root.back()
    }
    
    Keys.onLeftPressed: {
        index = (index + photos.length - 1) % photos.length;
        console.log("index:" + index);
    }
    
    Keys.onRightPressed: {
        index = (index + 1) % photos.length;
        console.log("index:" + index);
    }
    
    focus: true
    fillMode: Image.PreserveAspectFit
    source: photos.length > 0 ? photos[index] : ""
}
