import os
import sys


class EnvManager:
    @staticmethod
    def _get_windows_user_maya_env(maya_version: str) -> str:
        """
        Windowsでユーザーのダウンロードフォルダを取得する

        Parameters
        ----------
        maya_version : str
            書き込みたい対象のMayaバージョン

        Returns
        -------
        maya_env : str
            Maya.envまでのフォルダパス
        """
        user_folder = os.path.expanduser("~")
        maya_env = os.path.join(user_folder,
                                "Documents",
                                "maya",
                                maya_version,
                                "Maya.env")
        return maya_env

    @staticmethod
    def _comb_cwd_relative_path(relative_path: str) -> str:
        """
        現在のカレントディレクトリと引数で指定した相対パスを結合したパスを取得する

        Parameters
        ----------
        relative_path : str
            スクリプトを実行したカレントディレクトリから対象までの相対パス

        Returns
        -------
        path : str
            現在のカレントディレクトリと引数で指定した相対パスを結合したパス
        """
        cwd = os.getcwd()
        combined_path = os.path.join(cwd, relative_path)
        path = os.path.abspath(combined_path)
        return path

    @staticmethod
    def _write_env_parameter(env_path: str, additional_param: tuple):
        """
        .envファイルにparameterを書き込む

        Parameters
        ----------
        env_path : str
            書き込みたい.envファイルまでのファイルパス
        additional_param : tuple
            追加したい変数のkeyとvalue
        """
        # 追加する文字列
        additional_str = f"{additional_param[0]} = {additional_param[1]}"

        # ファイルの内容を読み込んで確認する
        if os.path.exists(env_path):
            with open(env_path, 'r', encoding='utf-8') as file:
                content = file.read()
        else:
            content = ""

        # 指定した文字列がファイル内に存在しない場合にのみ書き込む
        if additional_str not in content:
            # 追記モードでファイルを開く（'a'は追記モード）
            with open(env_path, 'a', encoding='utf-8') as file:
                if content:  # ファイルが空でない場合のみ改行を追加
                    file.write('\n')
                # 文字列を書き込む
                file.write(additional_str)
            print("ファイルに文字列を書き込みました。")
        else:
            print("指定した文字列は既にファイル内に存在します")

    @staticmethod
    def _check_os():
        """
        OSが対応しているかどうかをチェックして、対応しない場合は、スクリプトを終了する。
        """
        if os.name != 'nt':
            print("Warning: This script Windows OS only.")
            sys.exit(1)  # スクリプトを終了する
        else:
            print("Running on Windows OS.")

    @staticmethod
    def _check_file_exist(file_path: str):
        """
        対象のファイルが存在しているかどうかをチェックして、存在しない場合は、スクリプトを終了する。
        Parameters
        ----------
        file_path : str
            チェックしたいファイルのパス
        """
        if not os.path.exists(file_path):
            print("Warning: This file not exist.")
            sys.exit(1)  # スクリプトを終了する
        else:
            print("Exist file.")

    @staticmethod
    def write_env_script_path(maya_version: str):
        """
        指定バージョンのMaya.envに環境変数を書き込む

        Parameters
        ----------
        maya_version : str
            追加したいMayaのバージョン
        """
        relative_path = r"."
        EnvManager._check_os()
        env_file_path = EnvManager._get_windows_user_maya_env(maya_version)
        EnvManager._check_file_exist(env_file_path)
        maya_script_param = ("MAYA_SCRIPT_PATH",
                             EnvManager._comb_cwd_relative_path(relative_path))
        EnvManager._write_env_parameter(env_file_path, maya_script_param)
        py_script_param = ("PYTHONPATH ",
                           EnvManager._comb_cwd_relative_path(relative_path))
        EnvManager._write_env_parameter(env_file_path, py_script_param)
