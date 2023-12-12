import sys
from PyQt5.QtWidgets import (QApplication, 
                             QMainWindow, 
                             QVBoxLayout, 
                             QHBoxLayout, 
                             QWidget, 
                             QLabel, 
                             QPushButton,
                             QFileDialog)
from PyQt5.QtGui import (QImage, 
                         QPixmap, 
                         QPainter, 
                         QPen, 
                         QColor)
from PyQt5.QtCore import Qt
import fitz  # PyMuPDF


class PDFViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('PDF Viewer')
        self.setGeometry(100, 100, 400, 300)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.navigation_layout = QHBoxLayout()
        self.layout.addLayout(self.navigation_layout)

        self.load_button = QPushButton('Загрузить файл', self.central_widget)
        self.load_button.clicked.connect(self.loadPDF)
        self.load_button.setFixedSize(100, 30)
        self.navigation_layout.addWidget(self.load_button)

        self.prev_button = QPushButton('<', self.central_widget)
        self.prev_button.clicked.connect(self.showPreviousPage)
        self.prev_button.setFixedSize(100, 30)
        self.navigation_layout.addWidget(self.prev_button)

        self.next_button = QPushButton('>', self.central_widget)
        self.next_button.clicked.connect(self.showNextPage)
        self.next_button.setFixedSize(100, 30)
        self.navigation_layout.addWidget(self.next_button)

        self.label = QLabel(self.central_widget)
        self.layout.addWidget(self.label)

        self.current_page = 0
        self.rect_start = None       
        self.rect_end = None


    def loadPDF(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "Open PDF File", "", "PDF Files (*.pdf);;All Files (*)", options=options)

        if file_name:
            self.doc = fitz.open(file_name)
            self.showPage(self.current_page)


    def showPage(self, page_number):
        if 0 <= page_number < len(self.doc):
            # Render the first page of the PDF document
            page = self.doc[page_number]
            image = page.get_pixmap()
            
            # Convert to QImage
            qimage = QImage(image.samples, image.width, image.height, image.stride, QImage.Format_RGB888)
            # Set the image to QLabel
            self.label.setPixmap(QPixmap.fromImage(qimage))
            # Resize the main window to fit the PDF content
            self.resize(image.width, image.height)
            self.current_page = page_number
    

    def showPreviousPage(self):
        self.showPage(self.current_page - 1)
    

    def showNextPage(self):
        self.showPage(self.current_page + 1)

    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.rect_start = event.pos()


    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.rect_end = event.pos()
            self.drawRectangle()


    def drawRectangle(self):
        if self.rect_start and self.rect_end:
            painter = QPainter(self.label.pixmap())
            painter.setPen(QPen(QColor(255, 0, 0), 2, Qt.SolidLine))
            painter.drawRect(self.rect_start.x(), self.rect_start.y(), self.rect_end.x() - self.rect_start.x(), self.rect_end.y() - self.rect_start.y())
            painter.end()
            self.label.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = PDFViewer()
    viewer.show()
    sys.exit(app.exec_())
