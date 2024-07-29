# -*- coding: utf-8 -*-
import sys
from maya import cmds
from maya import mel
import os

sys.path.append('../')
from ihtools.general import getter

class Checker():
    
    def check_file_name(self, **kwargs):
        """シーンファイルの名称と、シーンファイルの親ディレクトリの名称が同一かチェック
        
        Returns:
        ----------
        bool
            新ファイルの名称と、シーンファイルの親ディレクトリの名称が同一であればTrue
            同一でなければFalse
        ----------
        """
        get_dir_path = getter.GetDirPath()
        dir_name = get_dir_path.get_dir_name()
        file_name = get_dir_path.get_file_name()

        if dir_name != file_name:
            return False
        else:
            return True


    def check_scene_extension(self, **kwargs):
        """シーンファイルの拡張子が、extensionに設定した値と同一かチェック

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
        extension = "." + kwargs["extension"]
        file_path = cmds.file(q = True, sceneName= True)
        
        if os.path.basename(file_path)[-(len(extension)):] != extension:
            return False
        else:
            return True
        

    def check_tris(self, **kwargs):
        """選択したモデルの三角ポリゴン数がupper_limitで設定した値以下かチェック

        Parameters:
        ----------
        transforms : str
            確認したいモデルのトランスフォーム
        upper_limit : int
            それ以下としたい値
        
        Returns:
        ----------
        bool
            シーンファイルの拡張子が、引数のものと同一であればTrue
            同一でなければFalse
        ----------
        """
        upper_limit = int(kwargs["upper_limit"])
        transforms = kwargs["transforms"]

        cmds.select(transforms)
        mel.eval('setPolyCountVisibility(1);')
        tris = cmds.polyEvaluate(t=1)
        
        if tris > upper_limit:
            return False
        else:
            return True

    def cleanup_arg_list(self, **kwargs):
        """シーン上のモデルに不適切なモデルがないかチェック

        Returns:
        ----------
        bool
            シーン状のモデルに不適切なモデルがなければTrue
            あればFalse
        ----------
        """
        mel.eval('polyCleanupArgList 4 { "1","2","1","0","1","1","1","0","1","1e-05","1","1e-05","0","1e-05","0","1","1","0" };')
        
        if bool(cmds.ls(sl = True)) == True:
            return False
        else:
            cmds.select(cmds.ls(sl = True))
            return True


    def check_cameras(self, **kwargs):
        """初期カメラ以外のカメラがOutliner上にないかチェック

        Returns:
        ----------
        bool
            初期カメラ以外のカメラがOutliner上になければTrue
            あればFalse
        ----------
        """
        cams = set(cmds.ls(cameras = True))
        fourCams = {"perspShape", "topShape", "frontShape", "sideShape"}
        otherCams = cams - fourCams
        
        if bool(otherCams) == True:
            return False
        else:
            return True
            
            
    def check_history(self, **kwargs):
        """選択したモデルのヒストリが残っているかチェック

        Parameters:
        ----------
        transforms : str
            確認したいモデルのトランスフォーム
        ----------

        Returns:
        ----------
        bool
            選択したモデルにヒストリが残ってなければTrue
            残っていればFalse
        ----------
        """
        transforms = kwargs["transforms"]
        all_history = cmds.listHistory(transforms)
        shape = cmds.listRelatives(transforms)[0]
        history = [his for his in all_history if his != shape]
        
        if bool(history) == True:
            return False
        else:
            print("True")
            


    def check_pivot_zero(self, **kwargs):
        """選択したモデルのpivotsに初期値以外の値が入っていないかチェック

        Parameters:
        ----------
        transforms : str
            確認したいモデルのトランスフォーム
        
        Returns:
        ----------
        bool
            選択したモデルのpivotsに初期値以外の値が入っていないなければTrue
            入っていればFalse
        ----------
        """
        transforms = kwargs["transforms"]
        
        for node in transforms:
            lrp = cmds.xform(node, q = True, sp = True)
            lsp = cmds.xform(node, q = True, sp = True)
            wrp = cmds.xform(node, q = True, sp = True, ws = True)
            wsp = cmds.xform(node, q = True, sp = True, ws = True)
            zero_double_three = [0.0, 0.0, 0.0]
            
            if lrp != zero_double_three\
                or lsp != zero_double_three\
                or wsp != zero_double_three\
                or wsp != zero_double_three:
               
                return False
            else:
                return True
               
    def check_transform_attr(self, **kwargs):
        """選択したモデルのTransformに初期値以外の値が入っていないかチェック

        Parameters:
        ----------
        transforms : str
            確認したいモデルのトランスフォーム

        Returns:
        ----------
        bool
            選択したモデルのTransformに初期値以外の値が入っていないなければTrue
            入っていればFalse
        ----------
        """
        transforms = kwargs["transforms"]
        for node in transforms:
            tra = cmds.getAttr("{}.translate".format(node))[0]
            rot = cmds.getAttr("{}.rotate".format(node))[0]
            sca = cmds.getAttr("{}.scale".format(node))[0]

            if tra != (0.0, 0.0, 0.0)\
                or rot != (0.0, 0.0, 0.0)\
                or sca != (1.0, 1.0, 1.0):
                return False
            else:
                return True
               
    def check_layer(self, **kwargs):
        """defaultLayer以外のDisplay Layerもしくは、Anim Layerが存在しないかチェック

        Returns:
        ----------
        bool
            defaultLayer以外のDisplay Layerもしくは、Anim Layerが存在していなかったらTrue
            存在していればFalse
        ----------
        """
        all_dis_layers = cmds.ls(type = "displayLayer")
        dis_layers = [layer for layer in all_dis_layers if layer != 'defaultLayer']
        anim_layers = cmds.ls(type = "animLayer")
        
        if bool(dis_layers) == True or bool(anim_layers) == True:
            return False
        else:
            return True


    def check_texture_name(self,
                                transforms,
                                attr = ".color",
                                head = "",
                                tail_end = ""):
        """テクスチャの命名規則が正しいものかチェック
        
        Parameters:
        ----------
        transforms : str
            確認したいモデルのトランスフォーム
        attr : str
            該当のテクスチャに接続されているアトリビュートの名称
        head : str
            テクスチャの接頭辞
        tail_end :
            テクスチャの接尾辞

        Returns:
        ----------
        bool
            テクスチャの接頭辞、接尾辞が指定したものと同一であればTrue
            同一でなければFalse
        ----------
        """
        get_dir_path = getter.GetDirPath()        
        texture_path = get_dir_path.get_texture_path(transforms, attr)
        texture_file_name= os.path.basename(os.path.splitext(texture_path)[0])
        split_file_name  = list(texture_file_name.split("_"))
        
        if split_file_name[0] != head:
            if head == "": return True
            print("***ファイル名の接頭辞が {} ではありません。***".format(head))
            return False

        if split_file_name[-1] != tail_end:
            if tail_end == "": return True
            print("***ファイル名の接尾辞が {} ではありません。***".format(tail_end))
            return False
            
        return True
    
    def check_texture_extension(self,
                                transforms,
                                attr = "color",
                                extension = ".png"):
        """テクスチャの拡張子が指定したものと同一かチェック
        Parameters:
        ----------
        transforms : str
            確認したいモデルのトランスフォーム
        attr : str
            該当のテクスチャに接続されているアトリビュートの名称
        extension : str
            テクスチャの拡張子

        Returns:
        ----------
        bool
            拡張子が指定したものと同一であればTrue
            同一でなければFalse
        ----------
        """
        get_dir_path = getter.GetDirPath()        
        texture_path = get_dir_path.get_texture_path(transforms, attr)

        if os.path.splitext(texture_path)[1] != extension:
            print("***拡張子が .{} ではありません。***".format(extension))
            return False