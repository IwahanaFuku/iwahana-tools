import sys

sys.path.append('../')
from ihtools.ms import modelsetup
from ihtools.gui import guibasemaya
from ihtools.gui import guimodules
pyside_version, QtCore, QtGui, QtWidgets = guimodules.import_pyside()

class MSGUI(guibasemaya.MayaUIBase):
    def __init__(self, parent):
        self.arsc = modelsetup.ArrangeScene()
        self.armd = modelsetup.ArrangeModels()
        self.pamd = modelsetup.ProjectArrangeModels()

        self.init_check_box = False

        self.func_dic = {"カメラセッティング" : {"func" : self.arsc.camela_settings},
                         "レイヤーを削除" : {"func" : self.arsc.delete_layer},
                         "使用していないノードを削除" : {"func" : self.arsc.deleat_unused_nodes},
                         "place2dTextureノードを削除" : {"func" : self.arsc.deleat_place_2D_textures},
                         "選択したトランスフォームと削除不可ノード以外を削除" : {"func" : self.arsc.deleat_not_select_transforms},
                         "トランスフォームの原点をモデルの重心地点の底面に移動" : {"func" : self.armd.pivots_to_bottom},
                         "ワールドの原点にトランスフォームを移動" : {"func" : self.armd.move_to_origin}, 
                         "トランスフォームのヒストリを削除" : {"func" : self.armd.deleat_history}, 
                         "トランスフォームのアトリビュートをフリーズ" : {"func" : self.armd.identity_mesh}, 
                         "ShadingEngineノードの名前をマテリアル名SGに変更" : {"func" : self.armd.rename_SGs}, 
                         "トランスフォームをリセット" : {"func" : self.armd.reset_transforms}, 
                         "mayaSwatchesフォルダを削除" : {"func" : self.arsc.remove_maya_swatches}, 
                         "マテリアルの名前を設定" : {"func" : self.pamd.rename_material_texture_name},
                         "uvをリネーム" : {"func" : self.armd.mold_uv}}

        func_dic_common = {"is_check_box" : self.init_check_box, "kwargs_dic" : {}}
        self.init_dics(func_dic_common)

        super(MSGUI, self).__init__(parent)

    def base_window(self):
        self.setGeometry(500, 300, 600, 270)
        self.setObjectName('modelsetup')        
        self.setWindowTitle("モデルセットアップツール") 

    def main_functions_layout(self):
        root_layout = QtWidgets.QVBoxLayout(self)
        
        root_layout.addLayout(self.camela_settings_check_box_layout("カメラセッティング"))       
        root_layout.addLayout(self.common_check_box_layout("レイヤーを削除")) 
        root_layout.addLayout(self.common_check_box_layout("使用していないノードを削除")) 
        root_layout.addLayout(self.common_check_box_layout("place2dTextureノードを削除")) 
        root_layout.addLayout(self.common_check_box_layout("選択したトランスフォームと削除不可ノード以外を削除")) 
        root_layout.addLayout(self.common_check_box_layout("トランスフォームの原点をモデルの重心地点の底面に移動")) 
        root_layout.addLayout(self.common_check_box_layout("ワールドの原点にトランスフォームを移動")) 
        root_layout.addLayout(self.common_check_box_layout("トランスフォームのヒストリを削除")) 
        root_layout.addLayout(self.common_check_box_layout("トランスフォームのアトリビュートをフリーズ")) 
        root_layout.addLayout(self.common_check_box_layout("トランスフォームをリセット"))
        root_layout.addLayout(self.common_check_box_layout("ShadingEngineノードの名前をマテリアル名SGに変更"))
        root_layout.addLayout(self.common_check_box_layout("mayaSwatchesフォルダを削除"))
        root_layout.addLayout(self.rename_material_texture_name_layout("マテリアルの名前を設定"))
        root_layout.addLayout(self.mold_uv_layout("uvをリネーム"))


        return root_layout


    def main_functions(self):
        self.transform_setting(["選択したトランスフォームと削除不可ノード以外を削除",
                                "トランスフォームの原点をモデルの重心地点の底面に移動",
                                "ワールドの原点にトランスフォームを移動",
                                "トランスフォームのヒストリを削除",
                                "トランスフォームのアトリビュートをフリーズ",
                                "ShadingEngineノードの名前をマテリアル名SGに変更",
                                "トランスフォームをリセット" ,
                                "マテリアルの名前を設定",
                                "uvをリネーム"])
        
        for key in self.func_dic["カメラセッティング"]["kwargs_dic"].keys():
            
            self.func_dic["カメラセッティング"]["kwargs_dic"][key] = float(self.func_dic["カメラセッティング"]["kwargs_dic"][key])

        for key in self.func_dic:
            if self.func_dic[key]["is_check_box"] == True:
                self.func_dic[key]["func"](**self.func_dic[key]["kwargs_dic"])


    def camela_settings_check_box_layout(self, key):
        dic = self.func_dic[key]
             
        #ルート
        layout = QtWidgets.QHBoxLayout(self)
        
        #チェックボックス
        check_box = QtWidgets.QCheckBox(dic["name"].ljust(57), self)
        layout.addWidget(check_box)
        check_box.setChecked(self.init_check_box)

        #オプション入力欄
        option_layout = QtWidgets.QVBoxLayout(self)

        #回転レイアウト
        rotate_grid_layout = QtWidgets.QGridLayout()
        rotate_label = QtWidgets.QLabel("回転：")

        rotate_x_line = QtWidgets.QLineEdit("-25.000")
        rotate_y_line = QtWidgets.QLineEdit("45.000")
        rotate_z_line = QtWidgets.QLineEdit("0.000")

        rotate_grid_layout.addWidget(rotate_label, 0, 0)
        rotate_grid_layout.addWidget(rotate_x_line, 0, 1)
        rotate_grid_layout.addWidget(rotate_y_line, 0, 2)
        rotate_grid_layout.addWidget(rotate_z_line, 0, 3)
        option_layout.addLayout(rotate_grid_layout)

        #焦点距離レイアウト
        focal_grid_layout = QtWidgets.QGridLayout()
        focal_label = QtWidgets.QLabel("焦点距離：")

        focal_length_line = QtWidgets.QLineEdit("135")

        focal_grid_layout.addWidget(focal_label, 0, 0)
        focal_grid_layout.addWidget(focal_length_line, 0, 1)
        option_layout.addLayout(focal_grid_layout)

        #クリッププレーンレイアウト
        clip_grid_layout = QtWidgets.QGridLayout()
        near_clip_label = QtWidgets.QLabel("ニアクリッププレーン：")
        near_clip_plane_line = QtWidgets.QLineEdit("1.000")
        far_clip_label = QtWidgets.QLabel("ファークリッププレーン：")
        far_clip_plane_line = QtWidgets.QLineEdit("10000.000")

        clip_grid_layout.addWidget(near_clip_label, 0, 0)
        clip_grid_layout.addWidget(near_clip_plane_line, 0, 1)
        clip_grid_layout.addWidget(far_clip_label, 1, 0)
        clip_grid_layout.addWidget(far_clip_plane_line, 1, 1)
        option_layout.addLayout(clip_grid_layout)

        #オプションレイアウトを配置        
        layout.addLayout(option_layout)

        #部品のふるまいを追加
        check_box.setCheckable(True)
        check_box.stateChanged.connect(lambda: self.checkbox_change(check_box.checkState(), dic["name"]))

        #それぞれ値を初期化
        dic["kwargs_dic"]["rotate_x"] = rotate_x_line.text()
        dic["kwargs_dic"]["rotate_y"] = rotate_y_line.text()
        dic["kwargs_dic"]["rotate_z"] = rotate_z_line.text()
        dic["kwargs_dic"]["focal_length"] = focal_length_line.text()
        dic["kwargs_dic"]["near_clip_plane"] = near_clip_plane_line.text()
        dic["kwargs_dic"]["far_clip_plane"] = far_clip_plane_line.text()

        #それぞれ値をに変化があったときに辞書に登録
        rotate_x_line.textChanged.connect(lambda: self.dic_text_change("rotate_x", rotate_x_line.text(), dic["name"]))
        rotate_y_line.textChanged.connect(lambda: self.dic_text_change("rotate_y", rotate_y_line.text(), dic["name"]))
        rotate_z_line.textChanged.connect(lambda: self.dic_text_change("rotate_z", rotate_z_line.text(), dic["name"]))
        focal_length_line.textChanged.connect(lambda: self.dic_text_change("focal_length", focal_length_line.text(), dic["name"]))
        near_clip_plane_line.textChanged.connect(lambda: self.dic_text_change("near_clip_plane", near_clip_plane_line.text(), dic["name"]))
        far_clip_plane_line.textChanged.connect(lambda: self.dic_text_change("far_clip_plane", far_clip_plane_line.text(), dic["name"]))
        

        return layout           

    def rename_material_texture_name_layout(self, key):
        dic = self.func_dic[key]
        #ルート
        layout = QtWidgets.QHBoxLayout(self)
        
        #チェックボックス
        check_box = QtWidgets.QCheckBox(dic["name"].ljust(50), self)
        layout.addWidget(check_box)
        check_box.setChecked(self.init_check_box)

        #オプション入力欄
        option_layout = QtWidgets.QVBoxLayout(self)

        material_name_layout = QtWidgets.QGridLayout()
        color_label = QtWidgets.QLabel("テクスチャが接続されたアトリビュート")
        color_line = QtWidgets.QLineEdit("color")
        name_position_label = QtWidgets.QLabel('取得したいテクスチャ内の "_" で囲まれたブロック')
        name_position_line = QtWidgets.QLineEdit("0")
        head_label = QtWidgets.QLabel("接頭辞")
        head_line = QtWidgets.QLineEdit("MAT")
        tail_end_label = QtWidgets.QLabel("接尾辞")
        tail_end_line = QtWidgets.QLineEdit("Opaque")
        
        material_name_layout.addWidget(color_label, 0, 0)
        material_name_layout.addWidget(color_line, 0, 1)
        material_name_layout.addWidget(name_position_label, 1, 0)
        material_name_layout.addWidget(name_position_line, 1, 1)
        material_name_layout.addWidget(head_label, 2, 0)
        material_name_layout.addWidget(head_line, 2, 1)
        material_name_layout.addWidget(tail_end_label, 3, 0)
        material_name_layout.addWidget(tail_end_line, 3, 1)
        option_layout.addLayout(material_name_layout)

        layout.addLayout(option_layout)

        #部品のふるまいを追加
        check_box.setCheckable(True)
        check_box.stateChanged.connect(lambda: self.checkbox_change(check_box.checkState(), dic["name"]))

        #それぞれ値を初期化
        dic["kwargs_dic"]["attr"] = color_line.text()
        dic["kwargs_dic"]["name_position"] = name_position_line.text()
        dic["kwargs_dic"]["head"] = head_line.text()
        dic["kwargs_dic"]["tail_end"] = tail_end_line.text()

        #それぞれ値をに変化があったときに辞書に登録
        color_line.textChanged.connect(lambda: self.dic_text_change("attr", color_line.text(), dic["name"]))
        name_position_line.textChanged.connect(lambda: self.dic_text_change("name_position", name_position_line.text(), dic["name"]))
        head_line.textChanged.connect(lambda: self.dic_text_change("head", head_line.text(), dic["name"]))
        tail_end_line.textChanged.connect(lambda: self.dic_text_change("tail_end", tail_end_line.text(), dic["name"]))
        return layout

    def mold_uv_layout(self, key):
        dic = self.func_dic[key]
        #ルート
        layout = QtWidgets.QHBoxLayout(self)

        #チェックボックス
        check_box = QtWidgets.QCheckBox(dic["name"].ljust(50), self)
        layout.addWidget(check_box)
        check_box.setChecked(self.init_check_box)

        #オプション入力欄
        option_layout = QtWidgets.QVBoxLayout(self)

        uv_name_layout = QtWidgets.QGridLayout()
        uv1_label = QtWidgets.QLabel("UV1")
        uv1_line = QtWidgets.QLineEdit("map1")
        uv2_label = QtWidgets.QLabel("UV2")
        uv2_line = QtWidgets.QLineEdit("uvSet")

        uv_name_layout.addWidget(uv1_label, 0, 0)
        uv_name_layout.addWidget(uv1_line, 0, 1)
        uv_name_layout.addWidget(uv2_label, 1, 0)
        uv_name_layout.addWidget(uv2_line, 1, 1)
        option_layout.addLayout(uv_name_layout)

        layout.addLayout(option_layout)

        #部品のふるまいを追加
        check_box.setCheckable(True)
        check_box.stateChanged.connect(lambda: self.checkbox_change(check_box.checkState(), dic["name"]))

        #それぞれ値を初期化
        dic["kwargs_dic"]["uv_list"] = [uv1_line.text(), uv2_line.text()]
        print(dic["kwargs_dic"]["uv_list"] )

        #それぞれ値をに変化があったときに辞書に登録
        uv1_line.textChanged.connect(lambda: self.dic_list_change("uv_list", uv1_line.text(), dic["name"],0))
        uv2_line.textChanged.connect(lambda: self.dic_list_change("uv_list", uv2_line.text(), dic["name"],1))

        return layout

def main(*args):
    maya_window_instance = MSGUI(parent = guibasemaya.get_maya_main_window())
    maya_window_instance.show()

if __name__ == "__main__": 
    main() 