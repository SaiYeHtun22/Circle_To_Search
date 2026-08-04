import sys
import io
import re
from PyQt6 import QtWidgets, QtCore, QtGui
from PIL import ImageGrab
from google import genai
from google.genai import types

def markdown_to_html(md_text):
    html = md_text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    html = re.sub(r'\*\*(.*?)\*\*', r'<b style="color: #ffffff;">\1</b>', html)
    html = re.sub(r'\*(.*?)\*', r'<i>\1</i>', html)
    html = re.sub(r'`(.*?)`', r'<code style="background-color: #1e1e24; color: #a6e3a1; padding: 2px 5px; border-radius: 4px;">\1</code>', html)
    html = html.replace('\n', '<br>')
    return html

class UnifiedAIWindow(QtWidgets.QWidget):
    def __init__(self, img_bytes):
        super().__init__()
        self.img_bytes = img_bytes
        
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint | 
            QtCore.Qt.WindowType.WindowStaysOnTopHint |
            QtCore.Qt.WindowType.Tool
        )
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(550, 480)
        
        self.init_ui()
        self.center_on_screen()
        
        # Auto-focus input box as soon as the window appears
        QtCore.QTimer.singleShot(50, self.focus_input)

    def focus_input(self):
        self.input_field.setFocus()

    # Close instantly on ESC key
    def keyPressEvent(self, event: QtGui.QKeyEvent):
        if event.key() == QtCore.Qt.Key.Key_Escape:
            QtWidgets.QApplication.quit()
        else:
            super().keyPressEvent(event)

    def center_on_screen(self):
        screen_geometry = QtWidgets.QApplication.primaryScreen().geometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)

    def init_ui(self):
        container = QtWidgets.QFrame(self)
        container.setObjectName("MainContainer")
        container.setStyleSheet("""
            QFrame#MainContainer {
                background-color: #0d0d0e;
                border: 1px solid #27272a;
                border-radius: 12px;
            }
            QLabel {
                color: #a1a1aa;
                font-family: 'Segoe UI', sans-serif;
                font-size: 13px;
            }
            QLineEdit {
                background-color: #161618;
                color: #f4f4f5;
                border: 1px solid #27272a;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #52525b;
            }
            QTextBrowser {
                background-color: #161618;
                color: #d4d4d8;
                border: 1px solid #27272a;
                border-radius: 8px;
                padding: 12px;
                font-size: 14px;
                line-height: 1.6;
            }
            QPushButton#ActionBtn {
                background-color: #f4f4f5;
                color: #09090b;
                border: none;
                border-radius: 8px;
                padding: 8px 18px;
                font-weight: 600;
                font-size: 13px;
            }
            QPushButton#ActionBtn:hover {
                background-color: #e4e4e7;
            }
            QPushButton#CloseBtn {
                background-color: transparent;
                color: #71717a;
                border: none;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton#CloseBtn:hover {
                color: #f4f4f5;
            }
        """)

        layout = QtWidgets.QVBoxLayout(container)
        layout.setContentsMargins(16, 14, 16, 16)
        layout.setSpacing(12)

        header = QtWidgets.QHBoxLayout()
        header_title = QtWidgets.QLabel("Selection")
        header_title.setStyleSheet("font-weight: 600; color: #71717a; font-size: 11px; text-transform: uppercase; letter-spacing: 1px;")
        
        close_btn = QtWidgets.QPushButton("✕")
        close_btn.setObjectName("CloseBtn")
        close_btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        close_btn.clicked.connect(QtWidgets.QApplication.quit)
        
        header.addWidget(header_title)
        header.addStretch()
        header.addWidget(close_btn)
        layout.addLayout(header)

        # Render Pixmap directly from bytes
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(self.img_bytes)
        
        self.image_label = QtWidgets.QLabel()
        self.image_label.setPixmap(pixmap.scaled(518, 140, QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation))
        self.image_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("background-color: #161618; border: 1px solid #27272a; border-radius: 8px; padding: 6px;")
        layout.addWidget(self.image_label)

        self.input_field = QtWidgets.QLineEdit()
        self.input_field.setPlaceholderText("Ask anything about this selection...")
        self.input_field.returnPressed.connect(self.send_query)
        layout.addWidget(self.input_field)

        self.response_browser = QtWidgets.QTextBrowser()
        self.response_browser.hide()
        layout.addWidget(self.response_browser)

        self.bottom_bar = QtWidgets.QHBoxLayout()
        self.status_label = QtWidgets.QLabel("")
        
        self.submit_btn = QtWidgets.QPushButton("Ask AI")
        self.submit_btn.setObjectName("ActionBtn")
        self.submit_btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.submit_btn.clicked.connect(self.send_query)

        self.bottom_bar.addWidget(self.status_label)
        self.bottom_bar.addStretch()
        self.bottom_bar.addWidget(self.submit_btn)
        layout.addLayout(self.bottom_bar)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(container)

    def send_query(self):
        prompt = self.input_field.text().strip()
        if not prompt:
            return

        self.status_label.setText("Thinking...")
        self.submit_btn.setEnabled(False)
        QtWidgets.QApplication.processEvents()

        try:
            client = genai.Client()
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=[
                    types.Part.from_bytes(data=self.img_bytes, mime_type='image/png'),
                    prompt
                ]
            )
            
            self.response_browser.setHtml(markdown_to_html(response.text))
            self.response_browser.show()
            self.image_label.hide()
            self.status_label.setText("")
            self.submit_btn.setText("Close")
            self.submit_btn.setEnabled(True)
            self.submit_btn.clicked.disconnect()
            self.submit_btn.clicked.connect(QtWidgets.QApplication.quit)
            self.resize(600, 420)

        except Exception as e:
            self.status_label.setText("Error!")
            QtWidgets.QMessageBox.critical(self, "Error", str(e))
            self.submit_btn.setEnabled(True)


class SnippingWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint |
            QtCore.Qt.WindowType.WindowStaysOnTopHint |
            QtCore.Qt.WindowType.Tool
        )
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setCursor(QtCore.Qt.CursorShape.CrossCursor)
        self.setGeometry(QtWidgets.QApplication.primaryScreen().geometry())
        
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.is_drawing = False

    # Close snipping on ESC key too if canceled
    def keyPressEvent(self, event: QtGui.QKeyEvent):
        if event.key() == QtCore.Qt.Key.Key_Escape:
            QtWidgets.QApplication.quit()
        else:
            super().keyPressEvent(event)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.fillRect(self.rect(), QtGui.QColor(0, 0, 0, 110))

        if self.is_drawing:
            rect = QtCore.QRect(self.begin, self.end).normalized()
            painter.setCompositionMode(QtGui.QPainter.CompositionMode.CompositionMode_Clear)
            painter.fillRect(rect, QtGui.QColor(0, 0, 0, 0))
            
            painter.setCompositionMode(QtGui.QPainter.CompositionMode.CompositionMode_SourceOver)
            pen = QtGui.QPen(QtGui.QColor(255, 255, 255), 2)
            painter.setPen(pen)
            painter.drawRect(rect)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.begin = event.pos()
            self.end = event.pos()
            self.is_drawing = True
            self.update()

    def mouseMoveEvent(self, event):
        if self.is_drawing:
            self.end = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton and self.is_drawing:
            self.is_drawing = False
            rect = QtCore.QRect(self.begin, self.end).normalized()
            self.hide()
            
            if rect.width() > 10 and rect.height() > 10:
                bbox = (rect.x(), rect.y(), rect.x() + rect.width(), rect.y() + rect.height())
                img = ImageGrab.grab(bbox=bbox)
                
                img_byte_arr = io.BytesIO()
                img.save(img_byte_arr, format='PNG')
                img_bytes = img_byte_arr.getvalue()
                
                global ai_window
                ai_window = UnifiedAIWindow(img_bytes)
                ai_window.show()
                ai_window.raise_()
                ai_window.activateWindow()
            else:
                QtWidgets.QApplication.quit()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    
    snipper = SnippingWidget()
    snipper.show()
    sys.exit(app.exec())
