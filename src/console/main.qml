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
        anchors.margins: 20
        spacing: 20

        RowLayout {

            id: leftDataSlot
            Layout.fillWidth: true
            spacing: 20

            ColumnLayout {
                id: radioData
                Layout.fillWidth: true
                spacing: 20

                Text {
                    id: freq
                    text: "14.024"
                    font.pointSize: 25
                    color: "#ffffff"
                }

                ProgressBar {
                    id: powerMeter
                    Layout.preferredWidth: mainLayout.width * 0.5
                    value: 0.5


                    background: Rectangle {
                        implicitHeight: 20
                        color: "#1f1f1f"
                    }
                    
                    contentItem: Item {
                        implicitHeight: 20

                        Rectangle {
                            width: powerMeter.visualPosition * parent.width
                            height: parent.height
                            color: '#ff0000'
                        }
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
                            color: ant1.down ? "#2049a1" : "#1652c2"
                            // radius: 8
                        }

                        onClicked: {
                            console.log("ANT 1 Selected")
                        }
                    }

                    Button {
                        id: rxAnt2
                        Layout.fillWidth: true
                        Layout.preferredHeight: 80
                        text: "RX ANT 2"
                        font.pointSize: 15

                        background: Rectangle {
                            color: ant2.down ? '#2049a1' : '#1652c2'
                            // radius: 8
                        }

                        onClicked: {
                            console.log("ANT 2 Selected")
                        }
                    }
                }
                
        }
    }
}