from .ms import ms_gui
from .mc import mc_gui
from .atvw import atvw_gui
import maya.cmds as cmds
import maya.mel as mel


def main():
    gMainWindow = mel.eval('$gmw = $gMainWindow')
    iwahana_tools_menu = cmds.menu(parent=gMainWindow,
                                   tearOff=True,
                                   label='Iwahana Tools'
                                   )
    cmds.menuItem(parent=iwahana_tools_menu,
                  label="モデルセットアップツール",
                  command=ms_gui.main
                  )
    cmds.menuItem(parent=iwahana_tools_menu,
                  label="モデルチェックツール",
                  command=mc_gui.main
                  )
    cmds.menuItem(parent=iwahana_tools_menu,
                  label="アトリビュートビューワー",
                  command=atvw_gui.main
                  )


if __name__ == "__main__":
    main()
