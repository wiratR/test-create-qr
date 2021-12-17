import os
from re import I
from PyQt5 import QtWidgets, QtCore, QtGui
import qrcode
from PIL import Image
from utils.callapi import CallApi
import uuid


class Image(qrcode.image.base.BaseImage):

    # taking image which user wants
    # in the QR code center
    # Logo_link = 'g4g.jpg'
    # logo = Image.open(Logo_link)

    def __init__(self, border, width, box_size):
        self.border = border
        self.width = width
        self.box_size = box_size
        size = (width + border * 2) * box_size
        self._image = QtGui.QImage(
            size, size, QtGui.QImage.Format_RGB16)
        self._image.fill(QtCore.Qt.white)
        # self._logoFile = Image.open(os.path.join(
        #     os.path.abspath(__file__), "image", "logo-square-1080.jpeg"))

    def pixmap(self):
        return QtGui.QPixmap.fromImage(self._image)

    def drawrect(self, row, col):
        painter = QtGui.QPainter(self._image)
        painter.fillRect(
            (col + self.border) * self.box_size,
            (row + self.border) * self.box_size,
            self.box_size, self.box_size,
            QtCore.Qt.black)

    def save(self, stream, kind=None):
        pass


class Window(QtWidgets.QWidget):

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.label = QtWidgets.QLabel(self)
        self.edit = QtWidgets.QLineEdit(self)
        # self.edit.returnPressed.connect(self.handleTextEntered)

        self.editTimer = QtWidgets.QLabel(self)

        # QTimer

        self.button = QtWidgets.QPushButton('Pay QR', self)
        # self.button.setToolTip('This is an example button')
        self.button.move(100, 70)
        self.button.clicked.connect(self.button_clicked)

        # Other
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.LCDEvent)
        self.s = 59

        self.requestId = 0

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.edit)
        layout.addWidget(self.button)
        layout.addWidget(self.editTimer)

    def timeGo(self):
        print("timeGo")
        self.timer.start(1000)

    def timeStop(self):
        print("timeStop")
        self.timer.stop()

    def LCDEvent(self):

        # print("LCDEvent")
        self.s -= 1
        # self.editTimer.text()
        self.editTimer.setText(str(self.s))
        if self.s == 0:
            self.timeStop()
            # clearing the data
            self.label.clear()
            self.label.setText('Payment Expired.')
        else:
            # Call reques
            confirm = CallApi(self.requestId).get_confirm_status()
            if confirm == True:
                self.timeStop()
                self.editTimer.setText('0')
                self.label.clear()
                self.label.setText('Payment Sucesss.')

    def button_clicked(self):
        self.requestId = uuid.uuid4()
        self.label.clear()
        print("clicked")
        self.s = 59
        self.editTimer.setText(str(self.s))
        self.timeGo()
        # self.timer.start(1000)

        txtAmount = self.edit.text()  # text = unicode(self.edit.text())
        print(f"{txtAmount}")
        # Call reques
        payment = CallApi(self.requestId)

        qrRowData = payment.run(txtAmount)

        self.label.setPixmap(
            qrcode.make(qrRowData, image_factory=Image).pixmap())


if __name__ == '__main__':

    import sys
    import signal
    app = QtWidgets.QApplication(sys.argv)
    # implement to shutdown gracefully on Ctrl-C
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    window = Window()
    window.setGeometry(500, 300, 200, 200)
    window.show()
    sys.exit(app.exec_())
