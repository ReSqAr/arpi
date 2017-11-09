import QtQuick 2.1
import QtQuick.Controls 1.1
import QtWebEngine 1.0


WebEngineView {
    id: webview

    property string callUrl : ""

    url: callUrl
    anchors.fill: parent

    function updateCallUrl(newCallUrl){
        webview.callUrl = newCallUrl
    }

    signal back()

    // https://bugreports.qt.io/browse/QTBUG-46251
    Action {
        shortcut: "Escape"
        onTriggered: {
            console.log("Escape pressed.");
            webview.back();
        }
    }
}
