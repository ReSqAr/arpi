import QtQuick 2.1
import QtQuick.Controls 1.1
import QtWebEngine 1.1

import "../../../res/style"



Rectangle {
    id: root_webview
    
    Style{
        id: global_style
    }

    signal back()

    function updateCallUrl(newCallUrl){
        webview.callUrl = newCallUrl
    }

    WebEngineView {
        id: webview

        property string callUrl : ""

        url: callUrl
        anchors.fill: parent

        // https://forum.qt.io/topic/55365/allow-webrtc-webcam-request-using-when-qtwebengine/2
        onFeaturePermissionRequested: {
            grantFeaturePermission(securityOrigin, feature, true);
        }
        
        // https://bugreports.qt.io/browse/QTBUG-46251
        Action {
            shortcut: "Escape"
            onTriggered: {
                console.log("Escape pressed.");
                root_webview.back();
            }
        }
    }

}
