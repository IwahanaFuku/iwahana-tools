import sys

sys.path.append('../')
from ihtools.atvw import attributeviewer
from ihtools.gui import guibasemaya
from ihtools.gui import guimodules
pyside_version, QtCore, QtGui, QtWidgets = guimodules.import_pyside()

class ATVGUI(guibasemaya.MayaUIBase):
    def __init__(self, parent):
        self.atvw = attributeviewer.SearchAttribute()

        self.init_check_box = True
        self.func_dic = {"アトリビュートを取得" : {"func" : self.atvw.search_attr_name}}
        func_dic_common = {"is_check_box" : self.init_check_box, "kwargs_dic" : {}}
        self.init_dics(func_dic_common)

        super(ATVGUI, self).__init__(parent)

    def base_window(self):
        self.setGeometry(500, 300, 300, 150)
        self.setObjectName('attributeviewer')        
        self.setWindowTitle("アトリビュートビューワー") 


    def base_futter(self):
        futter_layout = QtWidgets.QHBoxLayout(self)
        close_button = QtWidgets.QPushButton("閉じる", self)
        futter_layout.addWidget(close_button)
        close_button.clicked.connect(self.close_func)

        return futter_layout

    def main_functions_layout(self):
        root_layout = QtWidgets.QVBoxLayout(self)
        
        root_layout.addLayout(self.search_attr_name_layout("アトリビュートを取得"))        

        return root_layout
        
    def search_attr_name_layout(self, key):
        dic = self.func_dic[key]
        #ルート
        layout = QtWidgets.QVBoxLayout(self)
        
        #アトリビュートを持ったマテリアル名レイアウト
        search_key_layout = QtWidgets.QGridLayout()
        destination_node_label = QtWidgets.QLabel("アトリビュートを持ったノード名：")
        destination_node_line = QtWidgets.QLineEdit("Lambert1")
        source_node_label = QtWidgets.QLabel("接続されたノード名：")
        source_node_line = QtWidgets.QLineEdit("file1")

        search_key_layout.addWidget(destination_node_label, 0, 0)
        search_key_layout.addWidget(destination_node_line, 0, 1)
        search_key_layout.addWidget(source_node_label, 1, 0)
        search_key_layout.addWidget(source_node_line, 1, 1)
        layout.addLayout(search_key_layout)

        #検索ボタンレイアウト
        search_layout = QtWidgets.QHBoxLayout()
        search_button = QtWidgets.QPushButton("    検索    ", self)

        result = QtWidgets.QLineEdit("")

        search_layout.addWidget(search_button)
        search_layout.addWidget(result)

        layout.addStretch(1)
        layout.addLayout(search_layout)

        #それぞれ値を初期化
        dic["kwargs_dic"]["destination_node"] = destination_node_line.text()
        dic["kwargs_dic"]["source_node"] = source_node_line.text()

        #それぞれ値をに変化があったときに辞書に登録
        destination_node_line.textChanged.connect(lambda: self.dic_text_change("destination_node", destination_node_line.text(), dic["name"]))
        source_node_line.textChanged.connect(lambda: self.dic_text_change("source_node", source_node_line.text(), dic["name"]))
 
        #部品のふるまいを追加
        search_button.clicked.connect(lambda : result.setText(", ".join((dic["func"](**dic["kwargs_dic"])))))

        return layout

def main(*args):
    maya_window_instance = ATVGUI(parent = guibasemaya.get_maya_main_window())
    maya_window_instance.show()

if __name__ == "__main__": 
    main() 