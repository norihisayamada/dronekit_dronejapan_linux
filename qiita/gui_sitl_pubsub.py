#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time                         # ウェイト関数time.sleepを使うために必要
from subprocess import Popen        # subprocessの中から、Popenをインポート
from signal import signal, SIGINT   # Ctrl+C(SIGINT)の送出のために必要 

from dronekit import connect        # connectを使いたいのでインポート
from dronekit import VehicleMode    # VehicleModeも使いたいのでインポート
from dronekit import LocationGlobal, LocationGlobalRelative   # ウェイポイント移動に使いたいのでインポート

import Tkinter                      # GUIを作るライブラリ
import paho.mqtt.client as mqtt     # MQTT送受信
import json                         # JSON<-->辞書型の変換用


#==dronekit-sitl の起動情報================================
# example: 'dronekit-sitl copter --home=35.079624,136.905453,50.0,3.0 --instance 0'
sitl_frame          = 'copter'          # rover, plane, copterなどのビークルタイプ
sitl_home_latitude  = '35.894087'       # 緯度(度)  柏の葉キャンパス駅前ロータリー
sitl_home_longitude = '139.952447'      # 経度(度)
sitl_home_altitude  = '17.0'            # 高度(m)
sitl_home_direction = '0.0'             # 機首方位(度)
sitl_instance_num   = 0                 # 0〜

# コマンドライン入力したい文字列をリスト形式で作成
sitl_boot_list = ['dronekit-sitl',sitl_frame,
                  '--home=%s,%s,%s,%s' % (sitl_home_latitude,sitl_home_longitude,sitl_home_altitude,sitl_home_direction),
                  '--instance=%s'%(sitl_instance_num)]

#connection_stringの生成
connection_string = 'tcp:localhost:' + str(5760 + int(sitl_instance_num) * 10 ) # インスタンスが増えるとポート番号が10増える


#== MQTTの情報，Pub/Subするトピック =======================
mqtt_server = 'localhost'
mqtt_port = 1883

mqtt_pub_topic = 'drone/001'  # Publish用のトピック名を作成
mqtt_sub_topic = 'ctrl/001'   # Subscribe用のトピック名を作成

#== MQTTに送信するJSONのベースになる辞書 ===================
drone_info = {
            "status":{
                "isArmable":"false",
                "Arm":"false",
                "FlightMode":"false"
            },
            "position":{
                "latitude":"35.0000", 
                "longitude":"135.0000",
                "altitude":"20",
                "heading":"0"
            }
}

#== MQTTで受信するコマンドのベースになる辞書 ================
drone_command = {
    "IsChanged":"false",
    "command":"None",
    "d_lat":"0",
    "d_lon":"0",
    "d_alt":"0"
}

#== メイン関数 ============================================
def main(args):
    #==Tkinterのウィンドウを作る===============================
    root = Tkinter.Tk() # ウィンドウ本体の作成
    root.title(u'Dronekit-SITL Monitor')    # ウィンドウタイトルバー
    root.geometry('400x550')        # ウィンドウサイズ

    # Status
    frame0 = Tkinter.Frame(root,pady=10)
    frame0.pack()
    Label_status = Tkinter.Label(frame0,font=("",11),text="Status:")
    Label_status.pack(side="left")
    EditBox_status = Tkinter.Entry(frame0,font=("",11),justify="center",width=15)
    EditBox_status.pack(side="left")

    # IsArmable
    frame1 = Tkinter.Frame(root,pady=10)
    frame1.pack()
    Label_armable = Tkinter.Label(frame1,font=("",11),text="IsArmable:")
    Label_armable.pack(side="left")
    EditBox_armable = Tkinter.Entry(frame1,font=("",11),justify="center",width=15)
    EditBox_armable.pack(side="left")

    # ARM/DISARM
    frame2 = Tkinter.Frame(root,pady=10)
    frame2.pack()
    Label_arm = Tkinter.Label(frame2,font=("",11),text="Armed:")
    Label_arm.pack(side="left")
    EditBox_arm = Tkinter.Entry(frame2,font=("",11),justify="center",width=15)
    EditBox_arm.pack(side="left")

    # フライトモード
    frame3 = Tkinter.Frame(root,pady=10)
    frame3.pack()
    Label_flightmode = Tkinter.Label(frame3,font=("",11),text="Flight mode:")
    Label_flightmode.pack(side="left")
    EditBox_flightmode = Tkinter.Entry(frame3,font=("",11),justify="center",width=15)
    EditBox_flightmode.pack(side="left")

    # 緯度
    frame5 = Tkinter.Frame(root,pady=10)
    frame5.pack()
    Label_lat = Tkinter.Label(frame5,font=("",11),text="Latitude:")
    Label_lat.pack(side="left")
    EditBox_lat = Tkinter.Entry(frame5,font=("",11),justify="center",width=15)
    EditBox_lat.pack(side="left")

    # 経度
    frame6 = Tkinter.Frame(root,pady=10)
    frame6.pack()
    Label_lon = Tkinter.Label(frame6,font=("",11),text="Longitude:")
    Label_lon.pack(side="left")
    EditBox_lon = Tkinter.Entry(frame6,font=("",11),justify="center",width=15)
    EditBox_lon.pack(side="left")

    # 高度
    frame7 = Tkinter.Frame(root,pady=10)
    frame7.pack()
    Label_alt = Tkinter.Label(frame7,font=("",11),text="Altitude:")
    Label_alt.pack(side="left")
    EditBox_alt = Tkinter.Entry(frame7,font=("",11),justify="center",width=15)
    EditBox_alt.pack(side="left")

    # 方位
    frame8 = Tkinter.Frame(root,pady=10)
    frame8.pack()
    Label_dir = Tkinter.Label(frame8,font=("",11),text="Bearing:")
    Label_dir.pack(side="left")
    EditBox_dir = Tkinter.Entry(frame8,font=("",11),justify="center",width=15)
    EditBox_dir.pack(side="left")

    # InstanceNumber
    frame4 = Tkinter.Frame(root,pady=10)
    frame4.pack()
    Label_num = Tkinter.Label(frame4,font=("",11),text="Instance Number:")
    Label_num.pack(side="left")
    EditBox_number = Tkinter.Entry(frame4,font=("",11),justify="center",width=15)
    EditBox_number.pack(side="left")

    # Pubトピック名
    frame9 = Tkinter.Frame(root,pady=10)
    frame9.pack()
    Label_pubtopic = Tkinter.Label(frame9,font=("",11),text="Publish Topic:")
    Label_pubtopic.pack(side="left")
    EditBox_pubtopic = Tkinter.Entry(frame9,font=("",11),justify="center",width=30)
    EditBox_pubtopic.pack(side="left")

    # Subトピック名
    frame10 = Tkinter.Frame(root,pady=10)
    frame10.pack()
    Label_subtopic = Tkinter.Label(frame10,font=("",11),text="Subscribe Topic:")
    Label_subtopic.pack(side="left")
    EditBox_subtopic = Tkinter.Entry(frame10,font=("",11),justify="center",width=30)
    EditBox_subtopic.pack(side="left")

    #==dronekit-sitlの起動====================================
    p = Popen(sitl_boot_list)   # サブプロセスの起動
    time.sleep(1)   # 起動完了のために1秒待つ

    #==フライトコントローラ(FC)へ接続==========================
    vehicle = connect( connection_string, wait_ready=True )    # 接続

    #==MQTTのSubscribe関数====================================
    def on_message(client, userdata, msg):
        recv_command = json.loads(msg.payload)

        # 受信メッセージをコマンド辞書にコピー、その際に変更フラグを付加
        drone_command["IsChanged"] = "true"     # 届いた際にtrueにし，コマンドを処理したらfalseにする
        drone_command["command"] = recv_command["command"]

        if drone_command["command"] == "GOTO":
            drone_command["d_lat"] = recv_command["d_lat"]
            drone_command["d_lon"] = recv_command["d_lon"]
            drone_command["d_alt"] = recv_command["d_alt"]

    #==MQTTの初期化===========================================
    client = mqtt.Client()                  # クラスのインスタンス(実体)の作成
    client.connect( mqtt_server, mqtt_port, 60 )   # 接続先は自分自身
    client.subscribe( mqtt_sub_topic )
    client.on_message = on_message
    client.loop_start()                     # 通信処理スタート

    #==1秒おきに画面表示を更新する関数=========================
    def redraw():
        # ステータス、Arming関連、フライトモード情報の更新
        EditBox_status.delete(0,Tkinter.END)     # 前の文字列を削除
        EditBox_status.insert(Tkinter.END, str(vehicle.system_status.state) )  # 新しい文字列を書き込む
        EditBox_armable.delete(0,Tkinter.END)
        EditBox_armable.insert(Tkinter.END, str(vehicle.is_armable) )
        EditBox_arm.delete(0,Tkinter.END)
        EditBox_arm.insert(Tkinter.END, str(vehicle.armed) )
        EditBox_flightmode.delete(0,Tkinter.END)
        EditBox_flightmode.insert(Tkinter.END, str(vehicle.mode.name) )

        # 緯度/経度/高度/方位の更新
        EditBox_lat.delete(0,Tkinter.END)
        EditBox_lat.insert(Tkinter.END, str(vehicle.location.global_frame.lat) )
        EditBox_lon.delete(0,Tkinter.END)
        EditBox_lon.insert(Tkinter.END, str(vehicle.location.global_frame.lon) )
        EditBox_alt.delete(0,Tkinter.END)
        EditBox_alt.insert(Tkinter.END, str(vehicle.location.global_frame.alt) )
        EditBox_dir.delete(0,Tkinter.END)
        EditBox_dir.insert(Tkinter.END, str(vehicle.heading) )

        # 起動インスタンス番号、MQTTのトピック名の更新
        EditBox_number.delete(0,Tkinter.END)
        EditBox_number.insert(Tkinter.END, str(sitl_instance_num) )
        EditBox_pubtopic.delete(0,Tkinter.END)
        EditBox_pubtopic.insert(Tkinter.END, mqtt_pub_topic )
        EditBox_subtopic.delete(0,Tkinter.END)
        EditBox_subtopic.insert(Tkinter.END, mqtt_sub_topic )

        #==Publishするデータを作る===============================
        drone_info["status"]["isArmable"] = str(vehicle.is_armable)                 # ARM可能か？
        drone_info["status"]["Arm"] = str(vehicle.armed)                            # ARM状態
        drone_info["status"]["FlightMode"] = str(vehicle.mode.name)                 # フライトモード
        drone_info["position"]["latitude"] = str(vehicle.location.global_frame.lat) # 緯度
        drone_info["position"]["longitude"] = str(vehicle.location.global_frame.lon)# 経度
        drone_info["position"]["altitude"] = str(vehicle.location.global_frame.alt) # 高度
        drone_info["position"]["heading"] = str(vehicle.heading)                    # 方位

        #==MQTTの送信===========================================
        json_message = json.dumps( drone_info )     # 辞書型をJSON型に変換
        client.publish("drone/001", json_message )   # トピック名は以前と同じ"drone/001"

        # コマンドに対する処理
        if drone_command["IsChanged"] == "true":
            # GUIDEDコマンド
            if drone_command["command"] == "GUIDED":
                print("# Set GUIDED mode")
                vehicle.mode = VehicleMode("GUIDED")

            # RTLコマンド
            if drone_command["command"] == "RTL":
                print("# Set RTL mode")
                vehicle.mode = VehicleMode("RTL")

            # ARMコマンド
            if drone_command["command"] == "ARM":
                print("# Arming motors")
                vehicle.armed = True

            # DISARMコマンド
            if drone_command["command"] == "DISARM":
                print("# Disarming motors")
                vehicle.armed = False

            # TAKEOFFコマンド
            if drone_command["command"] == "TAKEOFF":
                print("# Take off!")
                aTargetAltitude = 20.0
                vehicle.simple_takeoff(aTargetAltitude)  # Take off to target altitude

            # LANDコマンド
            if drone_command["command"] == "LAND":
                print("# Set LAND mode...")
                vehicle.mode = VehicleMode("LAND")

            # GOTOコマンド
            if drone_command["command"] == "GOTO":
                print("# Set target position.")
                if drone_command["d_lat"] == "0":
                    drone_command["d_lat"] = str( vehicle.location.global_frame.lat )   # 緯度
                if drone_command["d_lon"] == "0":
                    drone_command["d_lon"] = str( vehicle.location.global_frame.lon )   # 経度
                if drone_command["d_alt"] == "0":
                    drone_command["d_alt"] = str( vehicle.location.global_frame.alt )   # 高度
                point = LocationGlobalRelative(float(drone_command["d_lat"]), float(drone_command["d_lon"]), float(drone_command["d_alt"]) )
                vehicle.simple_goto(point, groundspeed=5)

            # コマンドは読み終えたので、フラグを倒す
            drone_command["IsChanged"] = "false"
            drone_command["command"] = "None"

        root.after(1000, redraw )    # 1秒後に自分自身を呼び出す

    #==Tkinterの時間実行の機能after関数を使う===================
    root.after(1000, redraw )  # 最初に1回だけは本文で呼び出す必要がある．

    #==Tkinterメインループ====================================
    # Xボタンを押すまでこの関数がブロックする
    root.mainloop()

    #==ここから終了処理========================================
    # MQTT終了
    client.loop_stop()

    # フライトコントローラとの接続を閉じる
    vehicle.close()

     # サブプロセスにもSIGINT送信
    p.send_signal(SIGINT)
    p.communicate()
    time.sleep(1)   # 終了完了のために1秒待つ

    return 0

# このpyファイルがimportされたのではなく，scriptとして実行された時
if __name__ == '__main__':
    sys.exit(main(sys.argv))    # ここでmain関数を呼ぶ．argvはC言語と同様にコマンドライン引数

