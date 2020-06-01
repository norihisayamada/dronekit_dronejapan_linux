#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import Tkinter
import paho.mqtt.client as mqtt
import json

# MQTTブローカーの情報，パブリッシュするトピック
mqtt_server = 'localhost'
mqtt_port = 1883
mqtt_topic = 'ctrl/001' # このトピック名を受信するドローンが動く

# ドローンに投げるコマンドのベースになる辞書
drone_command = {
    "command":"None",
    "d_lat":"0",
    "d_lon":"0",
    "d_alt":"0"
}

# メイン関数
def main(args):

    # Tkinterのウィンドウを作る
    root = Tkinter.Tk()
    root.title(u'MQTT publisher for Drone Control') # ウィンドウタイトルバー
    root.geometry('400x520')        # ウィンドウサイズ

    # ボタンが押された時のコールバック関数
    def Button_pushed(event):
        # コマンド(実際はボタン上のテキスト)を取得
        drone_command["command"] = event.widget["text"]

        # GOTOボタンのときは，緯度/経度/高度の情報も取得する
        if drone_command["command"] == "GOTO":
            # mainの子なので，main内で定義されているEditBoxクラスにアクセスできる
            drone_command["d_lat"] = EditBox_lat.get()
            drone_command["d_lon"] = EditBox_lon.get()
            drone_command["d_alt"] = EditBox_alt.get()

        # MQTTのサーバー、ポート番号、トピック名を取る
        mqtt_server = EditBox_Host.get()
        mqtt_port = int(EditBox_Port.get() )
        mqtt_topic = EditBox_topic.get()

        # ブローカーへ接続
        client = mqtt.Client()
        client.connect( mqtt_server, mqtt_port, 60 )
        client.loop_start()

        # データをJSONで作ってPub
        json_command = json.dumps( drone_command )
        client.publish( mqtt_topic, json_command )

        client.loop_stop()

    #--------------------------------------------
    # 以降はウィンドウのデザインだけ

    # MQTTブローカーのアドレス、ポートを入力する部分
    frame_top = Tkinter.Frame(root,bd=2,relief='ridge')
    frame_top.pack(fill="x")
    Static_Host = Tkinter.Label(frame_top,font=("",11),text=u'Broker address: ')
    Static_Host.pack(anchor='n',side='left')
    EditBox_Host = Tkinter.Entry(frame_top,font=("",11),width=28)
    EditBox_Host.insert(Tkinter.END,'localhost')
    EditBox_Host.pack(anchor='n',side='left')
    EditBox_Port = Tkinter.Entry(frame_top,font=("",11),width=5)
    EditBox_Port.insert(Tkinter.END,'1883')
    EditBox_Port.pack(anchor='n',side='left')

    # トピック名の入力部分
    frame1 = Tkinter.Frame(root,pady=10)
    frame1.pack()
    Label_topic = Tkinter.Label(frame1,font=("",12),text="Topic name:")
    Label_topic.pack(side="left")
    EditBox_topic = Tkinter.Entry(frame1,font=("",12),justify="center",width=15)
    EditBox_topic.insert(Tkinter.END,'ctrl/001')
    EditBox_topic.pack(side="left")

    # フライトモード部分
    frame2 = Tkinter.Frame(root,pady=10)
    frame2.pack()
    Label_mode = Tkinter.Label(frame2,font=("",11),text="Flight mode:")
    Label_mode.pack(side="left")
    Button_mode_guided = Tkinter.Button(frame2,font=("",11),text=u'GUIDED')
    Button_mode_guided.bind("<Button-1>",Button_pushed )
    Button_mode_guided.pack(side="left")
    Button_mode_rtl = Tkinter.Button(frame2,font=("",11),text=u'RTL')
    Button_mode_rtl.bind("<Button-1>",Button_pushed )
    Button_mode_rtl.pack(side="left")

    # ARM/DISARM部分
    frame3 = Tkinter.Frame(root,pady=10)
    frame3.pack()
    Label_ada = Tkinter.Label(frame3,font=("",11),text="ARM/DISARM:")
    Label_ada.pack(side="left")
    Button_ada_arm = Tkinter.Button(frame3,font=("",11),text=u'ARM')
    Button_ada_arm.bind("<Button-1>",Button_pushed )
    Button_ada_arm.pack(side="left")
    Button_ada_disarm = Tkinter.Button(frame3,font=("",11),text=u'DISARM')
    Button_ada_disarm.bind("<Button-1>",Button_pushed )
    Button_ada_disarm.pack(side="left")

    # 離着陸部分
    frame4 = Tkinter.Frame(root,pady=10)
    frame4.pack()
    Label_ada = Tkinter.Label(frame4,font=("",11),text="Takeoff/Landing:")
    Label_ada.pack(side="left")
    Button_Takeoff = Tkinter.Button(frame4,font=("",11),text=u'TAKEOFF')
    Button_Takeoff.bind("<Button-1>",Button_pushed )
    Button_Takeoff.pack(side="left")
    Button_mode_land = Tkinter.Button(frame4,font=("",11),text=u'LAND')
    Button_mode_land.bind("<Button-1>",Button_pushed )
    Button_mode_land.pack(side="left")

    #空白
    Label_blank = Tkinter.Label(root,pady=10,font=("",12),text="  ")
    Label_blank.pack()

    # 緯度入力
    frame5 = Tkinter.Frame(root,pady=10)
    frame5.pack()
    Label_lat = Tkinter.Label(frame5,font=("",11),text="Latitude:")
    Label_lat.pack(side="left")
    EditBox_lat = Tkinter.Entry(frame5,font=("",11),justify="center",width=15)
    EditBox_lat.insert(Tkinter.END,'35.893246')
    EditBox_lat.pack(side="left")

    # 経度入力
    frame6 = Tkinter.Frame(root,pady=10)
    frame6.pack()
    Label_lon = Tkinter.Label(frame6,font=("",11),text="Longitude:")
    Label_lon.pack(side="left")
    EditBox_lon = Tkinter.Entry(frame6,font=("",11),justify="center",width=15)
    EditBox_lon.insert(Tkinter.END,'139.954909')
    EditBox_lon.pack(side="left")

    # 高度入力
    frame7 = Tkinter.Frame(root,pady=10)
    frame7.pack()
    Label_alt = Tkinter.Label(frame7,font=("",11),text="Altitude:")
    Label_alt.pack(side="left")
    EditBox_alt = Tkinter.Entry(frame7,font=("",11),justify="center",width=15)
    EditBox_alt.insert(Tkinter.END,'30')
    EditBox_alt.pack(side="left")

    # GOTOボタン
    frame8 = Tkinter.Frame(root,pady=10)
    frame8.pack()
    Button_goto = Tkinter.Button(frame8,font=("",11),text=u'GOTO', width=20)
    Button_goto.bind("<Button-1>",Button_pushed )
    Button_goto.pack(side="left")

    # メインループ
    root.mainloop()

    return 0

# このpyファイルがscriptとして呼ばれた時はmainを実行．importされたときは何もしない
if __name__ == '__main__':
    sys.exit(main(sys.argv)) # ここでmain関数を呼ぶ．argvとはＣ言語と同じコマンドライン引数のこと

