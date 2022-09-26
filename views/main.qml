import QtQuick 2.11
import QtQuick.Window 2.2
import QtQuick.Controls 2.2

ApplicationWindow {
    id: mainWindow
    visible: true
    width: 640
    height: 750

   /* signal reemitted()
    Component.onCompleted: controller.dataReady.connect(mainWindow.reemitted)
    onReemitted: {
        console.log("dataReady from qml")
    //    controller.handleMessage()
    }*/

    signal change(int state)
    Component.onCompleted: controller.stateChanged.connect(mainWindow.change)
    onChange: {
    //    controller.handleMessage()
        //volumeText.text = state.toString()
        switch(state){
            //press to speak
            case 1:
                tipText.text = "Press the button to speak."
                spinImg.visible = false
                backButton.color = "#1D71B8"
            break;
            //speak
            case 2:
                tipText.text = "Speak"
//                spinImg.visible = false
                backButton.color = "#54ff47"
            break;
            //processing message
            case 3:
                tipText.text = "Processing message, please wait..."
                backButton.color = "#bababa"
            break;
            //answering
            case 4:
                tipText.text = "Thinking answer..."
                spinImg.visible = true
            break;
        }
    }

     Rectangle{
            id: topTitle
            width: parent.width
            height: 150
            anchors.top: parent.top
            anchors.left: parent.left
            color: "#f9f6e8"
            Image{
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.top: parent.top
                anchors.bottom: parent.bottom
                width: 450
                anchors.topMargin: 10
                anchors.bottomMargin: 10
                source: "title_apollo.png"
            }
     }
    Item{
        id:content
        anchors.bottom: parent.bottom
        anchors.top: topTitle.bottom
        anchors.left: parent.left
        anchors.right: parent.right


        Image {
            width: parent.width
            anchors.top: parent.top
            anchors.bottom: buttonsArea.top
            anchors.left: parent.left
            fillMode: Image.TileVertically
            verticalAlignment: Image.AlignTop
            source: "bg.png"
        }
        Rectangle{
            id: chatArea
            width: parent.width
            anchors.top: parent.top
            anchors.bottom: buttonsArea.top
            anchors.left: parent.left
            color: "#00000000"
            clip: true
            ListView {
                id: messagesList
                model: controller.model
                anchors.fill: parent
                delegate: Rectangle{
                    width: parent.width
                    height: avatar.height > textContent.height ? (avatar.height + 20) : (textContent.height + 50)
                    color: "#00000000"

                    Image {
                        id: avatar
                        anchors.left: agent ? parent.left : undefined
                        anchors.right: agent ? undefined : parent.right
                        anchors.bottom: parent.bottom
                        height: 70
                        width: 70
                        source: agent ? "apolo.png" : "user.png"
                        anchors.margins: 10
                    }
                    Rectangle{
                        id: messageContent
                        height: textContent.height
                        anchors.left: agent ? avatar.right : undefined
                        anchors.right: agent ? undefined : avatar.left
                        width: ghostText.width < parent.width - avatar.width - 50 ? ghostText.width : parent.width - avatar.width - 50
                        anchors.bottom: parent.bottom
                        anchors.leftMargin: 10
                        anchors.rightMargin: 10
                        anchors.bottomMargin: 30
                        color: agent ? "#64b038" : "#5e7bd1"
                        radius: 10
                        Text {
                            id: textContent
                            text: message
                            width: parent.width
                            wrapMode: Text.WordWrap
                            padding: 10
                        }
                        Text {
                            id: ghostText
                            height: 0
                            text: message
                            padding: 10
                            color: "#00000000"
                        }
                    }

                    onWidthChanged: function() {
//                        vscroll.position = vscroll.size
                    }
                    ListView.onAdd: {
//                        vscroll.position = vscroll.size
                    }
                }

                ScrollBar.vertical: ScrollBar {
                    id: vscroll
                    active: true
                }

                add:
                    Transition {
                        NumberAnimation { property: "opacity"; from: 0; to: 1.0; duration: 400 }
                        NumberAnimation { property: "scale"; from: 0; to: 1.0; duration: 400 }
                    }

            }
        }
        /*Image {
            width: parent.width
            height: 150
            anchors.bottom: parent.bottom
            anchors.left: parent.left
            fillMode: Image.TileHorizontally
            verticalAlignment: Image.AlignLeft
            source: "piano.jpg"
        }*/
       Rectangle{
            id: buttonsArea
            width: parent.width
            height: 150
            anchors.bottom: parent.bottom
            anchors.left: parent.left
            color: "#f9f6e8"
            FontLoader { id: fixedFont; source: "Roboto-Regular.ttf" }
            Text{
                id: tipText
                anchors.verticalCenter: parent.verticalCenter
                anchors.right: parent.right
                anchors.rightMargin: 50
                text: "Press the button to speak."
                visible: true
                font.family: fixedFont.name
                font.pointSize: 7
            }
            Rectangle{
                id: backButton
                height: 75
                width: height
                radius: width*0.5
                color: "#1D71B8" //"#54ff47"
                anchors.centerIn: parent

            }
            Image {
                id:spinImg
                height: 75
                width: height
                source: "load.png"
                anchors.centerIn: parent
                visible: false
                RotationAnimation on rotation {
                    loops: Animation.Infinite
                    from: 0
                    to: 360
                    duration: 1000
                }
            }
            Image {
                id:iconImage
                height: backButton.height - 2
                width: height
                source: "icon.png"
                anchors.centerIn: parent
            }
            MouseArea{
                id: buttonArea
                height: backButton.height
                width: height
                cursorShape: Qt.PointingHandCursor
                anchors.centerIn: parent
                onClicked: {
                        backButton.color = "#1D71B8"
                        controller.startRecording()
                }
            }
        }
    }
}