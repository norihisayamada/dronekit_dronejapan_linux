#!usr/bin/env python
# -*- coding: utf-8 -*-
print( "SITLは前もって起動させておいてください" )    # 開始メッセージ

# 必要なライブラリをインポート
from dronekit import connect    # フライトコントローラやシミュレータへ接続するのがdronekit内にあるconnect
import time                     # ウェイト関数time.sleepを使うために必要

# 起動済みのSITLへの接続設定
connection_string = "tcp:localhost:5760"

# フライトコントローラ(FC)へ接続
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

print("終了．")    # 終了メッセージ

