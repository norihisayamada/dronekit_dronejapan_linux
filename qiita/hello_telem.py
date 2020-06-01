#!usr/bin/env python
# -*- coding: utf-8 -*-
print( "dronekitスタート" )    # 開始メッセージ

# 必要なライブラリをインポート
from dronekit import connect    # フライトコントローラやシミュレータへ接続するのがdronekit内にあるconnect
import time                     # ウェイト関数time.sleepを使うために必要

# 接続文字列の作成
connection_string = "/dev/ttyUSB0,57600"       # テレメトリ接続だとttyUSB、ボーレートは57.6k

# フライトコントローラ(FC)へ接続
print( "FCへ接続: %s" % (connection_string) )    # 接続設定文字列を表示
vehicle = connect(connection_string, wait_ready=True)    # 接続

#Ctrl+cが押されるまでループ
try:
    while True:
        # vehicleオブジェクト内のステータスを表示
        print("--------------------------" )
        print(" GPS: %s" % vehicle.gps_0 )          # GPSがないとゼロのまま
        print(" Battery: %s" % vehicle.battery )    # パワーモジュールがないとゼロのまま
        print(" Last Heartbeat: %s" % vehicle.last_heartbeat )
        print(" Is Armable?: %s" % vehicle.is_armable )     # ARM可能か？
        print(" System status: %s" % vehicle.system_status.state )
        print(" Mode: %s" % vehicle.mode.name )

        time.sleep(1)

except( KeyboardInterrupt, SystemExit):    # Ctrl+cが押されたら離脱
    print( "SIGINTを検知" )

# フライトコントローラとの接続を閉じる
vehicle.close()


print("終了．")    # 終了メッセージ
