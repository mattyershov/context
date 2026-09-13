import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Window {
    width: 800
    height: 480
    visible: true
    title: "Context"
    color: '#000000'

    ColumnLayout {
        id: mainLayout
        anchors.fill: parent
        anchors.margins: 10
        spacing: 20

        ColumnLayout {
            id: radioData
            Layout.alignment: Qt.AlignHCenter
            Layout.fillWidth: true
            spacing: 20

            RowLayout {
                id: mainRDRow
                // anchors.margins: 20
                Layout.alignment: Qt.AlignHCenter
                Layout.fillWidth: true
                spacing: 20

                ColumnLayout {
                    id: filA
                    Layout.alignment: Qt.AlignHCenter
                    spacing: 50

                    Text {
                        id: filALabel
                        text: "A"
                        font.pointSize: 15
                        color: "#ffffff"
                        Layout.alignment: Qt.AlignHCenter
                    }
                }

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
                        text: radio.freq_a
                        font.pointSize: 25
                        color: "#ffffff"
                        Layout.alignment: Qt.AlignHCenter
                    }
                    
                    RowLayout {
                        id: focusA
                        spacing: 0

                        Rectangle {
                            id: focusA1
                            width: 80
                            height: 5
                            color: {
                                if (radio.rx_focus == "A") {
                                    return "#00ff00"
                                } else if (radio.tx_focus == "A" && radio.rx_focus == "B"){
                                    return "#ff0000"
                                }
                                return '#000000ff'
                            }
                        }

                        Rectangle {
                            id: focusA2
                            width: 80
                            height: 5
                            color: {
                                if (radio.rx_focus == "A" && radio.tx_focus == "B") {
                                    return "#00ff00"
                                } else if (radio.tx_focus == "A"){
                                    return "#ff0000"
                                }
                                return '#000000ff'
                            }
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
                        text: radio.freq_b
                        font.pointSize: 25
                        color: "#ffffff"
                        Layout.alignment: Qt.AlignHCenter
                    }

                    RowLayout {
                        id: focusB
                        spacing: 0

                        Rectangle {
                            id: focusB1
                            width: 75
                            height: 5
                            color: {
                                if (radio.rx_focus == "B") {
                                    return "#00ff00"
                                } else if (radio.tx_focus == "B" && radio.rx_focus == "A"){
                                    return "#ff0000"
                                }
                                return '#000000ff'
                            }
                        }

                        Rectangle {
                            id: focusB2
                            width: 75
                            height: 5
                            color: {
                                if (radio.rx_focus == "B" && radio.tx_focus == "A") {
                                    return "#00ff00"
                                } else if (radio.tx_focus == "B"){
                                    return "#ff0000"
                                }
                                return '#000000ff'
                            }
                        }
                    }
                }

                ColumnLayout {
                    id: filB
                    Layout.alignment: Qt.AlignHCenter
                    spacing: 50

                    Text {
                        id: filBLabel
                        text: "A"
                        font.pointSize: 15
                        color: "#ffffff"
                        Layout.alignment: Qt.AlignHCenter
                    }
                }
            }

            RowLayout {
                id: miscData
                Layout.alignment: Qt.AlignHCenter

                Text {
                    id: keyApeed
                    text: "KEY: " + radio.key_speed
                    color: "#ffffff"
                    font.pointSize: 15
                }
            }
        }

    



        ColumnLayout {
            id: antennas
            anchors.margins: 20
            spacing: 10

            RowLayout {
            id: tx_antennas
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
                id: rx_antennas
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