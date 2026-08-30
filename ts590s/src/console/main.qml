import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Window {
    width: 800
    height: 480
    visible: true
    title: "PiStationManager Console"
    color: '#000000'

    ColumnLayout {
        id: mainLayout
        anchors.fill: parent
        anchors.margins: 10
        spacing: 20

        RowLayout {
            id: radioData
            // anchors.margins: 20
            Layout.alignment: Qt.AlignHCenter
            Layout.fillWidth: true
            spacing: 20

            ColumnLayout {
                id: vfoA
                Layout.alignment: Qt.AlignHCenter
                Text {
                    id: vfoALabel
                    text: "VFO A"
                    font.pointSize: 10
                    color: "#ffffff"
                    Layout.alignment: Qt.AlignHCenter
                }

                Text {
                    id: freqA
                    text: freqA
                    font.pointSize: 25
                    color: "#ffffff"
                    Layout.alignment: Qt.AlignHCenter
                }
                
                RowLayout {
                    id: focusA
                    spacing: 0

                    Rectangle {
                        id: focusA1
                        width: 50
                        height: 5
                        color: '#00ff00'
                    }

                    Rectangle {
                        id: focusA2
                        width: 50
                        height: 5
                        color: '#ff0000'
                    }
                }
                
            }


            ColumnLayout {
                id: vfoB
                Layout.alignment: Qt.AlignHCenter

                Text {
                    id: vfoBLabel
                    text: "VFO B"
                    font.pointSize: 10
                    color: "#ffffff"
                    Layout.alignment: Qt.AlignHCenter
                }

                Text {
                    id: freqB
                    text: "7003"
                    font.pointSize: 25
                    color: "#ffffff"
                    Layout.alignment: Qt.AlignHCenter
                }

                RowLayout {
                    id: focusB
                    spacing: 0

                    Rectangle {
                        id: focusB1
                        width: 50
                        height: 5
                        color: '#00ff00'
                    }

                    Rectangle {
                        id: focusB2
                        width: 50
                        height: 5
                        color: '#ff0000'
                    }
                }
            }
        }

    


        ColumnLayout {
            id: antennas
            anchors.margins: 20
            spacing: 10

            RowLayout {
            id: txAntennas
            anchors.margins: 20
            spacing: 5



                Button {
                    id: ant1
                    Layout.fillWidth: true
                    Layout.preferredHeight: 80
                    text: "ANT 1"
                    font.pointSize: 15

                    background: Rectangle {
                        color: ant1.down ? "#388e3c" : "#4caf50"
                        // radius: 8
                    }

                    onClicked: {
                        console.log("ANT 1 Selected")
                    }
                }

                Button {
                    id: ant2
                    Layout.fillWidth: true
                    Layout.preferredHeight: 80
                    text: "ANT 2"
                    font.pointSize: 15

                    background: Rectangle {
                        color: ant2.down ? "#388e3c" : "#4caf50"
                        // radius: 8
                    }

                    onClicked: {
                        console.log("ANT 2 Selected")
                    }
                }
            }

                RowLayout {
                id: rxAntennas
                anchors.margins: 20
                spacing: 5



                    Button {
                        id: rxAnt1
                        Layout.fillWidth: true
                        Layout.preferredHeight: 80
                        text: "RX ANT 1"
                        font.pointSize: 15

                        background: Rectangle {
                            color: rxAnt1.down ? "#2049a1" : "#1652c2"
                            // radius: 8
                        }

                        onClicked: {
                            console.log("RX ANT 1 Selected")
                        }
                    }

                    Button {
                        id: rxAnt2
                        Layout.fillWidth: true
                        Layout.preferredHeight: 80
                        text: "RX ANT 2"
                        font.pointSize: 15

                        background: Rectangle {
                            color: rxAnt2.down ? '#2049a1' : '#1652c2'
                            // radius: 8
                        }

                        onClicked: {
                            console.log("RX ANT 2 Selected")
                        }
                    }
                }
                
        }
    }
}