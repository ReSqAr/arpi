import QtQuick 2.0

Image {
    id: 'root'
    
    // signals
    signal back()
    signal selected(int currentIndex)
    
    // internal state
    property var photos : []
    property var currentIndex : 0
    
    // connect escape to onEscapePressed
    Keys.onEscapePressed: {
        root.back()
    }
    
    Keys.onLeftPressed: {
        currentIndex = (currentIndex + photos.length - 1) % photos.length;
        root.selected(currentIndex);
        console.log("currentIndex:" + currentIndex);
    }
    
    Keys.onRightPressed: {
        currentIndex = (currentIndex + 1) % photos.length;
        root.selected(currentIndex);
        console.log("currentIndex:" + currentIndex);
    }
    
    focus: true
    fillMode: Image.PreserveAspectFit
    source: photos.length > 0 ? photos[currentIndex] : ""
}
