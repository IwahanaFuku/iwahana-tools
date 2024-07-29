chcp 65001

@echo off
setlocal

echo Maya.envの設定

REM ユーザーからMAYA_VERSIONを入力させる
set /p MAYA_VERSION=使用しているMayaのバージョンを入力してください。例:2025:

REM setupモジュールを実行する
python -m setup %MAYA_VERSION%

endlocal
