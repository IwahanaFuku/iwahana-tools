from maya import cmds
from imp import reload
import os
import sys
from ihtools.general import getter
from ihtools.gui import guibase, guibasemaya
from ihtools.ms import modelsetup, ms_gui
from ihtools.mc import modelcheck, mc_gui
from ihtools.atvw import attributeviewer, atvw_gui
from ihtools import main as ma

def main():
    reload(getter)
    reload(guibase)
    reload(guibasemaya)
    
    #モデルセットアップ
    reload(modelsetup)
    reload(ms_gui)
    #ms_gui.main()


    #モデルチェック
    reload(modelcheck)
    reload(mc_gui)
    #mc_gui.main()


    #アトリビュートビューワー
    reload(atvw_gui)
    reload(attributeviewer)
    #atvw_gui.main()
        
    #reload(ma)
    #ma.main()

