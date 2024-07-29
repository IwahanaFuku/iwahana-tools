import sys
import copy
sys.path.append('../')
from ihtools.gui import guimodules
pyside_version, QtCore, QtGui, QtWidgets = guimodules.import_pyside()

class UIBase(QtWidgets.QMainWindow):
    def __init__(self, parent=None, *args, **kwargs):
        super(UIBase, self).__init__(parent, *args, **kwargs)

        self.initUI()

    def initUI(self):
        self.base_window()
        self.base_menu_bar()
        self.central_widget()

    def base_window_setting(self):
        self.setWindowFlags(Qt.Window)

    def base_window(self):
        self.setGeometry(500, 300, 400, 270)
        self.setObjectName("guibase")
        self.setWindowTitle("GUI Base")

    def base_menu_bar(self):
        open_menu = QtWidgets.QMenu("Open")
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("編集")
        help_menu = menu_bar.addMenu("ヘルプ")

        return None

    def central_widget(self):
        # 縦型レイアウト
        central_layout = QtWidgets.QVBoxLayout()
        central_layout.addLayout(self.main_functions_layout())

        # フッター
        central_layout.addStretch(1)
        central_layout.addLayout(self.base_futter())

        # ウェジットに追加
        widget = QtWidgets.QWidget(self)
        widget.setLayout(central_layout)
        self.setCentralWidget(widget)

    def base_futter(self):
        # レイアウト作成
        futter_layout = QtWidgets.QHBoxLayout(self)

        # 部品を作成
        apply_and_close_button = QtWidgets.QPushButton("適用して閉じる", self)
        apply_button = QtWidgets.QPushButton("適用", self)
        close_button = QtWidgets.QPushButton("閉じる", self)

        # 部品をレイアウトに追加
        futter_layout.addWidget(apply_and_close_button)
        futter_layout.addWidget(apply_button)
        futter_layout.addWidget(close_button)

        # 部品のふるまいを追加
        apply_and_close_button.clicked.connect(self.apply_and_close_func)
        apply_button.clicked.connect(self.apply_func)
        close_button.clicked.connect(self.close_func)

        return futter_layout

    def main_functions_layout(self):
        # レイアウト作成
        root_layout = QtWidgets.QHBoxLayout(self)

        # 部品を作成
        main_functions_button = QtWidgets.QPushButton("サンプル", self)

        # 部品をレイアウトに追加
        root_layout.addWidget(main_functions_button)

        # 部品のふるまいを追加
        main_functions_button.clicked.connect(self.main_functions)

        return root_layout

    def main_functions(self):
        print("メイン機能")

    def apply_and_close_func(self):
        self.main_functions()
        self.close()

        return None

    def apply_func(self):
        self.main_functions()

        return None

    def close_func(self):
        self.close()

        return None

    def common_check_box_layout(self, key):
        # ルート
        layout = QtWidgets.QHBoxLayout(self)

        # チェックボックス
        check_box = QtWidgets.QCheckBox(key, self)
        layout.addWidget(check_box)

        check_box.stateChanged.connect(
            lambda: self.checkbox_change(check_box.checkState(), key)
        )

        return layout

    def checkbox_change(self, state, key):
        if state == QtCore.Qt.Checked:
            self.func_dic[key]["is_check_box"] = True
            return self.func_dic
        else:
            self.func_dic[key]["is_check_box"] = False
            return self.func_dic

    def dic_text_change(self, value, text, key):
        self.func_dic[key]["kwargs_dic"][value] = text

    def dic_list_change(self, value, text, key, i):
        self.func_dic[key]["kwargs_dic"][value][i] = text

    def init_dics(self, add_dic):
        for key in self.func_dic.keys():
            copy_add_dic = copy.deepcopy(add_dic)
            self.func_dic[key]["name"] = key
            self.func_dic[key].update(**copy_add_dic)
