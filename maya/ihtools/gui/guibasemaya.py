import sys
from maya import OpenMayaUI as omui
from maya import cmds

sys.path.append('../')
from ihtools.gui import guibase
from ihtools.gui import guimodules
pyside_version, QtCore, QtGui, QtWidgets = guimodules.import_pyside()
shiboken_version, wrapInstance = guimodules.import_shiboken()


# SimpleButtonUIBase継承したMaya用のクラス
class MayaUIBase(guibase.UIBase):
    def __init__(self, parent):
        super(MayaUIBase, self).__init__(parent)

    def transform_setting(self, key_lis):
        for key in key_lis:
            self.func_dic[key]["kwargs_dic"]["transforms"] = cmds.ls(sl=True)


# mayaのメインウインドウを取得する
def get_maya_main_window():
    omui.MQtUtil.mainWindow()
    ptr = omui.MQtUtil.mainWindow()
    widget = wrapInstance(int(ptr), QtWidgets.QWidget)
    return widget