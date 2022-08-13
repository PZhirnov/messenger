import sys
from PyQt5.QtWidgets import QApplication, QWidget       # [1]

if __name__ == '__main__':
    app = QApplication(sys.argv)                        # [2]

    w = QWidget()                                       # [3]
    w.resize(250, 150)                                  # [4]
    w.move(300, 300)                                    # [5]
    w.setWindowTitle('Simple')                          # [6]
    w.show()                                            # [7]

    sys.exit(app.exec_())
