# call_x_api_by_python
- PythonでXのAPIを呼び出す。認証から取得(GET)まで。
- 自分のXでの投稿を、自動化するため。

# 概要
- main_asNativeApp.py:
    - X Developer PortalのAppの設定で、Type of Appを「Native app」にした場合の認証方法
- main_asAutomatedApp.py:
    - X Developer PortalのAppの設定で、Type of Appを「Web App, Automated App or Bot」にした場合の認証方法

# メモ
- PKCEは、Type of Appによらず、いずれにせよ必要
- "Type of App"の選択
    - "Type of App"の、Native Appは、スマホなどにインストールされるアプリのことなので、趣旨である"自動化"とは合っておらず、Xにバンされる可能性がある
    - そのため、"Web App, Automated App or Bot"を選択する
- make.comとlocalhostを使って、試行するときは、X Developer Portalの”App info"＞"Callback URI / Redirect URL"を変更することを忘れないようにすること
- コードの作成順
    - `main_asAutomatedApp.py`を作った後、それをコピーして`main_asNativeApp.py`を作ったため、`main_asNativeApp.py`の方がコーディングが進んでいる
    - `main_asAutomatedApp.py`は、一度動いた後メンテしていないので、汚いままになっているかもしれない（でも動くはず）

