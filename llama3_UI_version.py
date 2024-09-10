import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QPushButton, QLabel
from PyQt6.QtCore import Qt, QObject, pyqtSignal
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

class LLMStreamingCallback(StreamingStdOutCallbackHandler, QObject):
    new_token = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        QObject.__init__(self)

    def on_llm_new_token(self, token: str, **kwargs: any):
        token = token.replace('\n', '')
        self.new_token.emit(token)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Llama3 UI")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        title = QLabel("Local Llama3 test")
        title.setStyleSheet("background-color: yellow; font-size: 24px; padding: 10px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)  # 添加這行來置中文本
        layout.addWidget(title)

        self.system_prompt = QTextEdit(" Always response in Chinese(中文), not English")
        self.system_prompt.setFixedHeight(100)
        layout.addWidget(self.system_prompt)

        self.response = QTextEdit()
        self.response.setReadOnly(True)
        self.response.setStyleSheet("background-color: lightblue;")
        layout.addWidget(self.response)

        input_layout = QHBoxLayout()
        self.user_input = QLineEdit()
        self.user_input.returnPressed.connect(self.send_message)  # 添加這行
        input_layout.addWidget(self.user_input)
        
        send_button = QPushButton("Send")
        send_button.clicked.connect(self.send_message)
        input_layout.addWidget(send_button)
        
        layout.addLayout(input_layout)

        self.callback = LLMStreamingCallback()
        self.callback.new_token.connect(self.update_response)
        self.llm = Ollama(model='llama3', callback_manager=CallbackManager([self.callback]))

    def send_message(self):
        user_prompt = self.user_input.text().strip()  # 使用 strip() 去除首尾空白
        if not user_prompt:  # 如果輸入為空，直接返回
            return
        
        system_prompt = self.system_prompt.toPlainText()
        self.response.append(f"\nUser: {user_prompt}")
        self.response.append("AI: ")
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", user_prompt),
        ])
        chain = prompt | self.llm
        chain.invoke({"user_prompt": user_prompt})
        
        self.user_input.clear()

    def update_response(self, token):
        self.response.insertPlainText(token)
        self.response.ensureCursorVisible()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

