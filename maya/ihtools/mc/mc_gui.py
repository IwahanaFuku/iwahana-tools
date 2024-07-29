import sys
from imp import reload

sys.path.append('../')
from ihtools.mc import modelcheck
from ihtools.gui import guibasemaya
from ihtools.gui import guimodules
pyside_version, QtCore, QtGui, QtWidgets = guimodules.import_pyside()

class MCGUI(guibasemaya.MayaUIBase):
    def __init__(self, parent):   
        self.check = modelcheck.Checker()

        self.init_check_box = True
        self.init_result = "--"

        self.func_dic = {"シーン名とディレクトリ名が同一かチェック" : {"func" : self.check.check_file_name},
                         "シーンファイルの拡張子をチェック" : {"func" : self.check.check_scene_extension},
                         "選択したモデルの三角ポリゴン数をチェック" : {"func" : self.check.check_tris},
                         "不適切なモデルがないかチェック" : {"func" : self.check.cleanup_arg_list},
                         "初期カメラ以外のカメラがOutliner上にないかチェック" : {"func" : self.check.check_cameras},
                         "選択したモデルのpivotsに値が入っていないかチェック" : {"func" : self.check.check_pivot_zero},
                         "選択したモデルのTransformに値が入っていないかチェック" : {"func" : self.check.check_transform_attr},
                         "レイヤーが残っていないかチェック" : {"func" : self.check.check_layer,}}

        func_dic_common = {"is_check_box" : self.init_check_box, "kwargs_dic" : {}}
        self.init_dics(func_dic_common)

        super(MCGUI, self).__init__(parent)

    def base_window(self):
        self.setGeometry(500, 300, 450, 270)
        self.setObjectName('modelcheck')        
        self.setWindowTitle("モデルチェックツール") 


    def main_functions_layout(self):
        root_layout = QtWidgets.QVBoxLayout(self)
        
        root_layout.addLayout(self.common_label_check_box_layout("シーン名とディレクトリ名が同一かチェック", self.init_result))
        root_layout.addLayout(self.check_scene_extension_layout("シーンファイルの拡張子をチェック", self.init_result))
        root_layout.addLayout(self.check_tris_layout("選択したモデルの三角ポリゴン数をチェック", self.init_result))        
        root_layout.addLayout(self.common_label_check_box_layout("初期カメラ以外のカメラがOutliner上にないかチェック", self.init_result))
        root_layout.addLayout(self.common_label_check_box_layout("選択したモデルのpivotsに値が入っていないかチェック", self.init_result))
        root_layout.addLayout(self.common_label_check_box_layout("選択したモデルのTransformに値が入っていないかチェック", self.init_result))
        root_layout.addLayout(self.common_label_check_box_layout("レイヤーが残っていないかチェック", self.init_result))
        root_layout.addLayout(self.common_label_check_box_layout("不適切なモデルがないかチェック", self.init_result))

        return root_layout


    def main_functions(self):
        self.transform_setting(["選択したモデルの三角ポリゴン数をチェック",
                                "選択したモデルのpivotsに値が入っていないかチェック",
                                "選択したモデルのTransformに値が入っていないかチェック"])

        for key in self.func_dic:
            if self.func_dic[key]["is_check_box"] == True:
                result = self.func_dic[key]["func"](**self.func_dic[key]["kwargs_dic"])
                self.func_dic[key]["label"].setText(self.bool2str(result))


    def common_label_check_box_layout(self, key, result):
        dic = self.func_dic[key]
        #ルート
        layout = QtWidgets.QHBoxLayout(self)
        
        #チェックボックス
        dic["label"] = QtWidgets.QLabel(result, self)
        check_box = QtWidgets.QCheckBox(key, self)
        check_box.setChecked(self.init_check_box)
        
        layout.addWidget(dic["label"])
        layout.addWidget(check_box)
        layout.addStretch(1)

        check_box.stateChanged.connect(lambda: self.checkbox_change(check_box.checkState(), dic["name"]))

        return layout

    def check_scene_extension_layout(self, key, result):
        dic = self.func_dic[key]
        #ルート
        layout = QtWidgets.QHBoxLayout(self)
        
        #チェックボックス
        dic["label"] = QtWidgets.QLabel(result, self)
        check_box = QtWidgets.QCheckBox(key, self)
        check_box.setChecked(self.init_check_box)

        layout.addWidget(dic["label"])
        layout.addWidget(check_box)

        extension_layout = QtWidgets.QGridLayout()
        extension_label = QtWidgets.QLabel("拡張子")
        extension_line = QtWidgets.QLineEdit("ma")
        extension_layout.addWidget(extension_label, 0, 0)
        extension_layout.addWidget(extension_line, 0, 1)
        layout.addStretch(1)
        layout.addLayout(extension_layout)

        check_box.stateChanged.connect(lambda: self.checkbox_change(check_box.checkState(), dic["name"]))

        dic["kwargs_dic"]["extension"] = extension_line.text()
        extension_line.textChanged.connect(lambda: self.dic_text_change("extension", extension_line.text(), dic["name"]))


        return layout

    def check_tris_layout(self, key, result):
        dic = self.func_dic[key]
        #ルート
        layout = QtWidgets.QHBoxLayout(self)
        
        #チェックボックス
        dic["label"] = QtWidgets.QLabel(result, self)
        check_box = QtWidgets.QCheckBox(key, self)
        check_box.setChecked(self.init_check_box)

        layout.addWidget(dic["label"])
        layout.addWidget(check_box)

        upper_limit_layout = QtWidgets.QGridLayout()
        upper_limit_label = QtWidgets.QLabel("三角ポリゴン以下")
        upper_limit_line = QtWidgets.QLineEdit("8000")
        upper_limit_layout.addWidget(upper_limit_label, 0, 0)
        upper_limit_layout.addWidget(upper_limit_line, 0, 1)
        layout.addStretch(1)
        layout.addLayout(upper_limit_layout)

        check_box.stateChanged.connect(lambda: self.checkbox_change(check_box.checkState(), dic["name"]))

        dic["kwargs_dic"]["upper_limit"] = upper_limit_line.text()
        upper_limit_line.textChanged.connect(lambda: self.dic_text_change("upper_limit", upper_limit_line.text(), dic["name"]))


        return layout        

    def bool2str(self, bo):
        if bo == True:
            return "OK"
        else:
            return "NG"

def main(*args):
    maya_window_instance = MCGUI(parent = guibasemaya.get_maya_main_window())
    maya_window_instance.show()

if __name__ == "__main__": 
    main() 