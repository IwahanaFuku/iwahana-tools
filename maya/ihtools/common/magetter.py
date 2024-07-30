"""
   maya内のノード、ファイルパス、確認用コードを取得するクラスを集めたモジュール
"""

from maya import cmds
import os


class GetNode:
    """
    maya内のノードを取得する関数群を集めたクラス
    """

    @staticmethod
    def get_SGs(transform):
        """選択したモデルにアサインされているshadingEngineノードの名称を取得します
        Parameters:
        ----------
        transforms : str[]
            shadingEngineノードの名称を取得するモデルのトランスフォーム

        Returns:
        ----------
        str[]
            shadingEngineノードの名称
        ----------
        """
        shapenodes = cmds.listRelatives(transform)
        SGs = cmds.listConnections(shapenodes,
                                   s=False,
                                   d=True,
                                   t="shadingEngine"
                                   )
        SGs = list(set(SGs))
        return SGs

    @staticmethod
    def get_material(SG):
        """選択したShadingGroupにアサインされているマテリアルの名称を取得します

        Parameters:
        ----------
        SG : str
            マテリアルの名称を取得するモデルのトランスフォーム

        Returns:
        ----------
        str[]
            マテリアルの名称
        ----------
        """
        mat_name = cmds.ls(
            cmds.listConnections(SG, s=True, d=False), mat=True)[0]

        return mat_name


class GetDirPath:
    """
    mayaのシーンを構成するうえで関連するファイル、ファイルまでのパスを取得するための関数群を集めたクラス
    """

    @staticmethod
    def get_dir_name():
        """シーンが格納されているディレクトリまでのフルパスを取得
        Returns:
        ----------
        str
            シーンが格納されているディレクトリまでのフルパス
        ----------
        """
        file_path = cmds.file(q=True, sceneName=True)
        dir_name = os.path.basename(os.path.split(file_path)[0])

        return dir_name

    @staticmethod
    def get_file_name():
        """開いているシーンファイルの名称を取得
        Returns:
        ----------
        str
            開いているシーンファイルの名称を取得
        ----------
        """
        file_path = cmds.file(q=True, sceneName=True)
        file_name = os.path.basename(os.path.splitext(file_path)[0])

        return file_name

    @staticmethod
    def get_texture_file(materials, attr):
        """マテリアルの指定のアトリビュートに接続されているノードの名称を取得

        Parameters:
        ----------
        materials :attr
            マテリアルの名称
        attr : str
            取得したいアトリビュートの名称（Lambertマテリアルのカラーなら、".color"など）

        Returns:
        ----------
        str
            マテリアルの指定のアトリビュートに接続されているノードの名称を取得
        ----------
        """
        attr_node_name = "{}.{}".format(materials, attr)
        texture_file_name = cmds.listConnections(attr_node_name)[0]

        return texture_file_name

    @staticmethod
    def get_texture_path(texture_file_name):
        """ファイルのアトリビュートに接続されているテクスチャのフルパスを取得

        Parameters:
        ----------
        texture_file_name : str
            テクスチャが接続されているファイルの名称

        Returns:
        ----------
        str
            ファイルのアトリビュートに接続されているテクスチャのフルパス
        ----------
        """
        texture_path = cmds.getAttr(
            "{}.fileTextureName".format(texture_file_name))

        return texture_path


class ShowAttr:
    """
    mayaのスクリプトを書く上でノードやアトリビュートの確認のための関数を集めたクラス
    """

    @staticmethod
    def show_material_attr():
        """マテリアルのアトリビュート一覧を取得します

        Returns:
        ----------
        str[]
            マテリアルのアトリビュート一覧を取得します
        ----------
        """

        material_attr = cmds.listAttr(GetNode.get_material())

        return material_attr
