import sys
from maya import cmds
from maya import mel
import os
import shutil

sys.path.append('../')
from .general import getter


class Commomn():

    def convert_None(befores):
        """文字列

        Parameters:
        ----------
        extension : str
            同一とするべきシーンファイルの拡張子
        Returns:
        ----------
        bool
            シーンファイルの拡張子が、引数のものと同一であればTrue
            同一でなければFalse
        ----------
        """

        list_befores = list(befores)

        for list_str in list_befores:
            list_str = str(list_str)
            list_str = "None"
        return  list_befores

    def save_scene(self):
        """
        スクリプトからシーンを保存
        """

        cmds.file(save=True)
        return None