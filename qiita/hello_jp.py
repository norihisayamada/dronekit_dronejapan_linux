#!usr/bin/env python
# -*- coding: utf-8 -*-
print( "SITLスタート" )    # 開始メッセージ

# 必要なライブラリをインポート
import dronekit_sitl            # シミュレータをインポート
from dronekit import connect    # フライトコントローラやシミュレータへ接続するのがdronekit内にあるconnect
import time                     # ウェイト関数time.sleepを使うために必要

# SITLの起動
sitl = dronekit_sitl.start_default()            # sitlをデフォルト設定で起動
connection_string = sitl.connection_string()    # 起動したsitlから，接続設定用の文字列を入手する

# フライトコントローラ(FC)へ接続
# 実機ドローンだとconnection_stringは"/dev/ttyUSB0,57600"の様になる
print( "FCへ接続: %s" % (connection_string) )    # 接続設定文字列を表示
vehicle = connect(connection_string, wait_ready=True)    # 接続

#Ctrl+cが押されるまでループ
try:
    while True:
        # vehicleオブジェクト内のステータスを表示
        print("--------------------------" )
        print(" GPS: %s" % vehicle.gps_0 )
        print(" Battery: %s" % vehicle.battery )
        print(" Last Heartbeat: %s" % vehicle.last_heartbeat )
        print(" Is Armable?: %s" % vehicle.is_armable )
        print(" System status: %s" % vehicle.system_status.state )
        print(" Mode: %s" % vehicle.mode.name )

        time.sleep(1)

except( KeyboardInterrupt, SystemExit):    # Ctrl+cが押されたら離脱
    print( "SIGINTを検知" )

# フライトコントローラとの接続を閉じる
vehicle.close()

# SITLを終了させる
sitl.stop()


print("終了．")    # 終了メッセージ
