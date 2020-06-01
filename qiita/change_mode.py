#!usr/bin/env python
# -*- coding: utf-8 -*-
print( "dronekitスタート" )    # 開始メッセージ

# 必要なライブラリをインポート
from kbhit import *                 # kbhitを使うために必要(同じフォルダにkbhit.pyを置くこと)
from dronekit import connect        # connectを使いたいのでインポート
from dronekit import VehicleMode    # VehicleModeも使いたいのでインポート
import time                         # ウェイト関数time.sleepを使うために必要

# kbhit()を使うための「おまじない」を最初に２つ書く
atexit.register(set_normal_term)
set_curses_term()

# 接続文字列の作成
connection_string = "/dev/ttyUSB0,57600"       # テレメトリ接続だとttyUSB、ボーレートは57.6k

# フライトコントローラ(FC)へ接続
print( "FCへ接続: %s" % (connection_string) )    # 接続設定文字列を表示
vehicle = connect(connection_string, wait_ready=True)    # 接続

#Ctrl+cが押されるまでループ
try:
    while True:
        if kbhit():     # 何かキーが押されるのを待つ
            key = getch()   # 1文字取得

            # keyの中身に応じて分岐
            if  key=='s':				# stabilize
                mode = 'STABILIZE'
            elif key=='a':				# Alt Hold
                mode = 'ALT_HOLD'
            elif key=='p':				# PosHold
                mode = 'POSHOLD'
            elif key=='l':				# loiter
                mode = 'LOITER'
            elif key=='g':				# guided
                mode = 'GUIDED'
            elif key=='t':				# auto
                mode = 'AUTO'
            elif key=='r':				# RTL
                mode = 'RTL'
            elif key=='d':				# land
                mode = 'LAND'

            vehicle.mode = VehicleMode( mode )  # フライトモードの変更を指示
        
        # 現在のフライトモードを表示
        print("--------------------------" )
        print(" Mode: %s" % vehicle.mode.name )

        time.sleep(1)

except( KeyboardInterrupt, SystemExit):    # Ctrl+cが押されたら離脱
    print( "SIGINTを検知" )

# フライトコントローラとの接続を閉じる
vehicle.close()

print("終了．")    # 終了メッセージ
