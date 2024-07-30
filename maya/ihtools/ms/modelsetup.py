"""
   シーンやモデルの整理を行うためのクラスを集めたモジュール
"""

import sys
from maya import cmds
from maya import mel
import os
import shutil

sys.path.append("../")
from ihtools.common.magetter import GetNode # noqa
from ihtools.common.magetter import GetDirPath # noqa


class ArrangeScene:
    """
    シーンの整理を行うためのクラスを集めたモジュール
    """

    def camela_settings(self, **kwargs):
        """
        maya起動時の初期カメラ、perspに指定の数値を入力
        persp, top, front, sideがモデルを中央に収めるように調整

        Parameters:
        ----------
        rotate_x : float
            perspのrotateXに入力する値
        rotate_y : float
            perspのrotateXに入力する値
        rotate_z : float
            perspのrotateXに入力する値
        focal_length : froat
            perspのfocal_length（焦点距離）に入力する値
        near_clip_plane : froat
            perspのnearClipPlane（ニアクリッププレーン）に入力する値
        far_clip_plane : froat
            perspのfarClipPlane（ファークリッププレーン）に入力する値

        Returns:
        ----------
        None
            None
        ----------
        """
        rotate_x = kwargs["rotate_x"]
        rotate_y = kwargs["rotate_y"]
        rotate_z = kwargs["rotate_z"]
        focal_length = kwargs["focal_length"]
        near_clip_plane = kwargs["near_clip_plane"]
        far_clip_plane = kwargs["far_clip_plane"]

        cams = set(cmds.ls(cameras=True))
        perspcameras = [s for s in cams if "persp" in s]

        for perspcamera in perspcameras:
            nodeParent = cmds.listRelatives(perspcamera, p=True)[0]

            cmds.setAttr("{}.rotateX".format(nodeParent), rotate_x)
            cmds.setAttr("{}.rotateY".format(nodeParent), rotate_y)
            cmds.setAttr("{}.rotateZ".format(nodeParent), rotate_z)

            cmds.setAttr("{}.focalLength".format(perspcamera), focal_length)
            cmds.viewPlace(perspcamera, p=True)

        for cam in cams:
            cmds.setAttr("{}.nearClipPlane".format(cam), near_clip_plane)
            cmds.setAttr("{}.farClipPlane".format(cam), far_clip_plane)
            cmds.viewFit(cam, all=True)

        return None

    def remove_maya_swatches(self, **kwargs):
        """
        .mayaSwatchesフォルダを削除
        """

        file_path = cmds.file(q=True, sceneName=True)
        maya_swatches_path = "{}/.mayaSwatches".format(
            os.path.split(file_path)[0])

        if os.path.isdir(maya_swatches_path):
            shutil.rmtree(maya_swatches_path)

        return None

    def delete_layer(self, **kwargs):
        """
        defaultLayer以外で設定されているレイヤーを削除
        """

        all_dis_layers = cmds.ls(type="displayLayer")
        dis_layers = [
            layer for layer in all_dis_layers if layer != "defaultLayer"
            ]
        anim_layers = cmds.ls(type="animLayer")

        for dis_layer in dis_layers:
            try:
                cmds.delete(dis_layer)
            except ValueError as error:
                print(error)

        for anim_layer in anim_layers:
            try:
                cmds.delete(anim_layer)
            except ValueError as error:
                print(error)

        return None

    def deleat_unused_nodes(self, **kwargs):
        """
        使用していないノード削除
        """

        mel.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes");')  # noqa

        return None

    def deleat_place_2D_textures(self, **kwargs):
        """
        fileノードに接続されているplace2dTextureノードを削除
        """

        place_2D_textures = [
            pt for pt in cmds.ls(st=1) if "place2dTexture" in pt
            ]

        for place_2D_texture in place_2D_textures:
            try:
                cmds.delete(place_2D_texture)
            except ValueError as error:
                print(error)

        return None

    def deleat_not_select_transforms(self, **kwargs):
        """
        transformsと、削除不可ノード以外を削除

        Parameters:
        ----------
        transforms : str[]
            削除の必要のないトランスフォーム
        """

        select_transforms = set(kwargs["transforms"])
        all_transforms = set(cmds.ls(type="transform"))
        other_transforms = list(all_transforms - select_transforms)

        for select_transform in select_transforms:
            long_select_transform = cmds.ls(select_transform, long=True)[0]
            if len(long_select_transform.split("|")) > 2:
                cmds.parent(select_transforms, w=True)

        cmds.delete(other_transforms)

        return None


class ArrangeModels:
    """
    モデルの整理を行うためのクラスを集めたモジュール
    """

    def pivots_to_bottom(self, **kwargs):
        """
        トランスフォームの原点をモデルの重心地点の底面に移動

        ----------
        attr : str[]
            原点を移動させたいモデル
        """

        transforms = kwargs["transforms"]

        bbox = cmds.exactWorldBoundingBox(transforms)
        bottom = [(bbox[0] + bbox[3]) / 2, bbox[1], (bbox[2] + bbox[5]) / 2]
        cmds.xform(transforms, piv=bottom, ws=True)

        return None

    def move_to_origin(self, **kwargs):
        """
        トランスフォームの原点位置を中心にワールドの原点にトランスフォームを移動

        Parameters:
        ----------
        attr : str[]
            原点を移動させたいモデル
        """

        transforms = kwargs["transforms"]

        for transform in transforms:
            pp = cmds.xform(transform, q=True, sp=True, ws=True)

            trs = list(cmds.getAttr("{}.translate".format(transform))[0])

            for i in range(3):
                pp[i] *= -1

                cmds.setAttr(
                    "{}.translate".format(transform),
                    trs[0] + pp[0],
                    trs[1] + pp[1],
                    trs[2] + pp[2],
                    type="double3",
                )
                cmds.setAttr(
                    "{}.rotate".format(transform), 0, 0, 0, type="double3"
                    )
                cmds.setAttr(
                    "{}.scale".format(transform), 1, 1, 1, type="double3"
                    )

        return None

    def deleat_parent(self, **kwargs):
        """
        トランスフォームの親を削除してシーン直下にトランスフォームを移動

        Parameters:
        ----------
        attr : str[]
            シーン直下に移動させたいトランスフォーム
        """

        transforms = kwargs["transforms"]

        path = cmds.ls(transforms[0], long=True)[0]
        split_path = path.split("|")

        if len(split_path) >= 3:
            cmds.parent(split_path[-1], w=True)
            cmds.delete(split_path[1])

        return None

    def deleat_history(self, **kwargs):
        """
        ノードのヒストリを削除

        Parameters:
        ----------
        nodes : str[]
            ヒストリを削除したいノード
        """

        nodes = kwargs["transforms"]

        for node in nodes:
            cmds.delete(node, constructionHistory=True)

        return None

    def identity_mesh(self, **kwargs):
        """
        トランスフォームのアトリビュートをフリーズ

        Parameters:
        ----------
        nodes : str[]
            ヒストリを削除したいノード
        """

        transforms = kwargs["transforms"]

        for transform in transforms:
            cmds.makeIdentity(transform, a=True, t=True, r=True, s=True)

        return None

    def rename_SGs(self, **kwargs):
        """
        モデルにアサインされている、ShadingEngineノードの名前をマテリアル名+SGに変更

        Parameters:
        ----------
        transforms : str[]
            マテリアルを取得するモデルのトランスフォーム
        """

        transforms = kwargs["transforms"]

        SGs = GetNode.get_SGs(transforms)
        for SG in SGs:
            mat_name = GetNode.get_material(SG)
            print(mat_name)
            cmds.rename(SG, "{}SG".format(mat_name))

        return None

    def reset_transforms(self, **kwargs):
        """
        トランスフォームをスクリプトからリセット

        Parameters:
        ----------
        transforms : str[]
            トランスフォームのリセットを行いたいトランスフォーム
        """
        transforms = kwargs["transforms"]

        if not transforms:
            pass
        else:
            mel.eval("ResetTransformations;")

        return None

    def mold_uv(self, **kwargs):
        """
        transformsのuvをリスト順にリネーム

        Parameters:
        ----------
        transforms : str[]
            uvを設定したいトランスフォーム

        uv_list : uvリネームリスト
        """

        select_transforms = set(kwargs["transforms"])
        uv_list = kwargs["uv_list"]

        print(select_transforms)
        print(uv_list)

        for peace_selected in select_transforms:
            cmds.select(peace_selected)
            select_uv_list = cmds.polyUVSet(query=True, allUVSets=True)
            for i, uvli in enumerate(select_uv_list):
                if i >= len(uv_list):
                    break
                if uv_list[i] == uvli:
                    continue
                cmds.polyUVSet(rename=True, newUVSet=uv_list[i], uvSet=uvli)
        cmds.select(select_transforms)

        return None


class ProjectArrangeModels:
    """
    プロジェクトごとに既定の数値を入力する関数群を集めたクラス
    """

    def material_set_attr(self, **kwargs):
        """指定したマテリアルのアトリビュートに値を入力。"""
        transforms = kwargs["transforms"]
        mat_attr = kwargs["mat_attr"]
        value = float(kwargs["value"])

        SGs = GetNode.get_SGs(transforms)

        for SG in SGs:
            mat_name = GetNode.get_material(SG)
            cmds.setAttr("{}.{}".format(mat_name, mat_attr), value)

        return None

    def mesh_structure(self, transforms, mesh_name="Other", group_name="Mesh"):
        """
        選択したトランスフォームをグループ化して、モデル、グループをリネーム

        Parameters:
        ----------
        transforms : str[]
            グループ化した時の子になるモデル
        mesh_name : str
            子になるモデルの名前
        group_name : str
            親になるグループの名前
        """

        cmds.group(name=group_name)
        self.reset_transforms()
        cmds.select(cmds.listRelatives(group_name)[0])

        return None

    def rename_material_texture_name(self, **kwargs):
        """
        選択したモデルにアサインされているマテリアルの名前の"_"囲われた一か所を選択して、マテリアルの名前をリネーム
        接頭辞と、接尾辞を"_"で囲って設定

        Parameters:
        ----------
        transforms : str[]
            リネームしたいマテリアルがアサインされているモデル
        attr : str
            リネームしたいマテリアルがアサインされているアトリビュート
        name_position : int
            テクスチャの名称のうち、"_"の何番目の文字列を取得するか。
        head : str
            マテリアルに設定する接頭辞
        tail_end : str
            マテリアルに設定する接尾辞
        """

        transforms = kwargs["transforms"]
        attr = kwargs["attr"]
        name_position = int(kwargs["name_position"])
        head = kwargs["head"]
        tail_end = kwargs["tail_end"]

        SGs = GetNode.get_SGs(transforms)

        for SG in SGs:
            mat_name = GetNode.get_material(SG)
            texture_path = GetDirPath.get_texture_path(
                GetDirPath.get_texture_file(mat_name, attr)
            )
            texture_name = os.path.splitext(os.path.basename(texture_path))[0]
            split_file_name = list(texture_name.split("_"))

            if (not head or head == "") and (not tail_end or tail_end == ""):
                new_mat_name = split_file_name[name_position]

            elif not head or head == "":
                new_mat_name = "_".join(
                    [split_file_name[name_position]] + [tail_end]
                    )

            elif not tail_end or tail_end == "":
                new_mat_name = "_".join(
                    [head] + [split_file_name[name_position]]
                    )

            else:
                new_mat_name = "_".join(
                    [head] + [split_file_name[name_position]] + [tail_end]
                )

            cmds.rename(mat_name, new_mat_name)

        return None

    def rename_file_image_name(self, **kwargs):
        """
        マテリアルのアトリビュートに接続されているファイルの名前を"file_"を接頭辞にして、マテリアルの名前と同一に変更

        Parameters:
        ----------
        transforms : str[]
            リネームしたいマテリアルがアサインされているモデル
        attr : str
            リネームしたいマテリアルがアサインされているアトリビュート
        """

        transforms = kwargs["transforms"]
        attr = kwargs["attr"]

        SGs = GetNode.get_SGs(transforms)

        for SG in SGs:
            mat_name = GetNode.get_material(SG)
            file_name = GetDirPath.get_texture_file(mat_name, attr)
            cmds.rename(file_name, "file_" + mat_name)

        return None
