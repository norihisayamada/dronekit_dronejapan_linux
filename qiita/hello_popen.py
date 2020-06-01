#!usr/bin/env python
# -*- coding: utf-8 -*-
print( "SITLをsubprocessで起動します" )    # 開始メッセージ

# 必要なライブラリをインポート
from subprocess import Popen      # subprocessの中から、Popenをインポート
from signal import signal, SIGINT # Ctrl+C(SIGINT)の送出のために必要 
from dronekit import connect    # フライトコントローラやシミュレータへ接続するのがdronekit内にあるconnect
import time                     # ウェイト関数time.sleepを使うために必要


# dronekit SITL の起動情報
# example: 'dronekit-sitl copter --home=35.079624,136.905453,50.0,3.0 --instance 0'
sitl_frame          = 'copter'          # rover, plane, copterなどのビークルタイプ
sitl_home_latitude  = '35.079624'       # 緯度(度)
sitl_home_longitude = '136.905453'      # 経度(度)
sitl_home_altitude  = '0.0'             # 高度(m)
sitl_home_direction = '0.0'              # 機首方位(度)
sitl_instance_num   = 0                 # 0〜


# コマンドライン入力したい文字列をリスト形式で作成
sitl_boot_list = ['dronekit-sitl',sitl_frame,
                    '--home=%s,%s,%s,%s' % (sitl_home_latitude,sitl_home_longitude,sitl_home_altitude,sitl_home_direction),
                    '--instance=%s'%(sitl_instance_num)]

print '# sitl command: ', sitl_boot_list        # 文字列を表示
p = Popen(sitl_boot_list)   # サブプロセスの起動
time.sleep(1)   # 起動完了のために1秒待つ


# フライトコントローラ(FC)へ接続
connection_string = 'tcp:localhost:' + str(5760 + int(sitl_instance_num) * 10 ) # インスタンスが増えるとポート番号が10増える
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


 # サブプロセスにもSIGINT送信
p.send_signal(SIGINT)
p.communicate()
time.sleep(1)   # 終了完了のために1秒待つ

print("終了．")    # 終了メッセージ
