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
        spacing: 0

        ColumnLayout {
            id: radioData
            Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
            Layout.fillWidth: true
            spacing: 20

            RowLayout {
                id: mainRDRow
                // anchors.margins: 20
                Layout.alignment: Qt.AlignHCenter
                spacing: 20

                Text {
                    id: modeA
                    text: radio.mode_a
                    font.pointSize: 15
                    color: {
                        switch (radio.mode_a) {
                            case "CW":
                                return '#00ff00'

                            case "CW-R":
                                return '#ff7300'

                            case "LSB" || "USB":
                                return '#006eff'

                            default:
                                return "#ffffff"
                        }
                    }
                }

                Rectangle {
                    id: filA
                    width: 50
                    height: 30
                    color:{
                        if (radio.fil_a == "A"){
                            return '#0066ff'
                        } else if (radio.fil_a == "B") {
                            return '#ff0000'
                        } else return '#000000'
                    }
                    Text {
                        id: filAText
                        text: radio.fil_a
                        font.pointSize: 15
                        color: "#ffffff"
                        anchors.centerIn: parent
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
                Rectangle {
                    id: filB
                    width: 50
                    height: 30
                    color:{
                        if (radio.fil_b == "A"){
                            return '#0066ff'
                        } else if (radio.fil_b == "B") {
                            return '#ff0000'
                        } else return '#000000'
                    }
                    Text {
                        id: filBText
                        text: radio.fil_b
                        font.pointSize: 15
                        color: "#ffffff"
                        anchors.centerIn: parent

                    }
                }

                Text {
                    id: modeB
                    text: radio.mode_b
                    font.pointSize: 15
                    color: {
                        switch (radio.mode_b) {
                            case "CW":
                                return '#00ff00'

                            case "CW-R":
                                return '#ff7300'

                            case "LSB" || "USB":
                                return '#006eff'

                            default:
                                return "#ffffff"
                        }
                    }
                }
                
            }
        }

        RowLayout {
            id: midSection
            Layout.alignment: Qt.AlignHCenter
            Layout.fillHeight: true

            RowLayout {
                id: smIndicators
                Layout.fillWidth: false
                spacing: 0

                Rectangle {
                    id: smListenIndicator
                    implicitHeight: 50
                    implicitWidth: 50
                    Layout.fillWidth: true
                    border.width: 3
                    border.color: "#00f7ff"
                    color: radio.sm_status === "LISTEN" ? "#00f7ff" : "#000000"

                    Text {
                        id: smListenText
                        anchors.centerIn: parent
                        text: "L"
                        color: radio.sm_status === "LISTEN" ? "#000000" : "#00f7ff"
                        font.pointSize: 14
                    }
                }

                    Rectangle {
                    id: molIndicator
                    implicitHeight: 50
                    implicitWidth: 50
                    Layout.fillWidth: true
                    border.width: 3
                    border.color: '#ff0000'
                    color: radio.mol_status == 1 ? '#ff0000' : "#000000"

                    Text {
                        id: molText
                        anchors.centerIn: parent
                        text: "M"
                        color: radio.mol_status == 1 ? "#000000" : '#ff0000'
                        font.pointSize: 14
                    }
                }

                Rectangle {
                    id: smWorkIndicator
                    implicitHeight: 50
                    implicitWidth: 50
                    Layout.fillWidth: true
                    border.width: 3
                    border.color: '#ffffff'
                    color: radio.sm_status === "WORK" ? '#ffffff' : "#000000"

                    Text {
                        id: smWorkText
                        anchors.centerIn: parent
                        text: "W"
                        color: radio.sm_status === "WORK" ? "#000000" : "#ffffff"
                        font.pointSize: 14
                    }
                }
            }
        }
        RowLayout {
            id: bottomIndicators
            implicitHeight: 50
            Layout.fillWidth: true
            spacing: 0
            Layout.alignment: Qt.AlignBottom

            Rectangle {
                id: preAmpIndicator
                implicitHeight: 50
                implicitWidth: 100
                Layout.fillWidth: true
                border.width: 3
                border.color: '#00ff20'
                color: radio.mol_status == 1 ? '#00ff20' : "#000000"

                Text {
                    id: preAmpText
                    anchors.centerIn: parent
                    text: "PRE"
                    color: radio.mol_status == 1 ? "#000000" : '#00ff20'
                    font.pointSize: 14
                }
            }
            Rectangle {
                id: attIndicator
                implicitHeight: 50
                implicitWidth: 100
                Layout.fillWidth: true
                border.width: 3
                border.color: '#00ff20'
                color: radio.mol_status == 1 ? '#00ff20' : "#000000"

                Text {
                    id: attText
                    anchors.centerIn: parent
                    text: "ATT"
                    color: radio.mol_status == 1 ? "#000000" : '#00ff20'
                    font.pointSize: 14
                }
            }
            Rectangle {
                id: nrIndicator
                implicitHeight: 50
                implicitWidth: 100
                Layout.fillWidth: true
                border.width: 3
                border.color: '#00ff20'
                color: radio.mol_status == 1 ? '#00ff20' : "#000000"

                Text {
                    id: nrText
                    anchors.centerIn: parent
                    text: "NR"
                    color: radio.mol_status == 1 ? "#000000" : '#00ff20'
                    font.pointSize: 14
                }
            }
            Rectangle {
                id: esmIndicator
                implicitHeight: 50
                implicitWidth: 100
                Layout.fillWidth: true
                border.width: 3
                border.color: '#00ff20'
                color: radio.mol_status == 1 ? '#00ff20' : "#000000"

                Text {
                    id: esmText
                    anchors.centerIn: parent
                    text: "ESM"
                    color: radio.mol_status == 1 ? "#000000" : '#00ff20'
                    font.pointSize: 14
                }
            }
        }
    }
}