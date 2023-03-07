#
# 色抽出のサンプルコード
#
import numpy as np
import cv2
from time import sleep
import pprint
#四隅検出
#ライブラリのインポート
import pandas as pd

#画像用変数
imgred_name = r'..\python\images\red.jpg'
imgblue_name = r'..\python\images\blue.jpg'
# メイン関数
def mainred():
    imgred = cv2.imread('..\\python\\test.jpg') # ファイル読み込み(x軸 赤)

    # BGRでの色抽出
    #記述はBGRの順
    redLower = np.array([0, 0, 200])    # 抽出する色の下限
    redUpper = np.array([50, 50, 255])    # 抽出する色の上限
    redResult = redExtraction(imgred, redLower, redUpper)
    #cv2.imshow('BGR_test1', redResult)
    #生成画像の保存
    cv2.imwrite(imgred_name,redResult)
    sleep(1)
    
# メイン関数　青
def mainblue():
    imgblue = cv2.imread('..\\python\\test.jpg') # ファイル読み込み(x軸 赤)


    blueLower = np.array([190, 0, 0])    # 抽出する色の下限
    blueUpper = np.array([255, 40, 40])    # 抽出する色の上限
    blueResult = blueExtraction(imgblue, blueLower, blueUpper)
    #cv2.imshow('BGR_test1', blueResult)
    cv2.imwrite(imgblue_name,blueResult)
    sleep(1)



# BGRで特定の色を抽出する関数
def redExtraction(imgred, redLower, redUpper):
    red_mask = cv2.inRange(imgred, redLower, redUpper) # BGRからマスクを作成
    redresult = cv2.bitwise_and(imgred, imgred, mask=red_mask) # 元画像とマスクを合成
    return redresult

def blueExtraction(imgblue, blueLower, blueUpper):
    blue_mask = cv2.inRange(imgblue, blueLower, blueUpper) # BGRからマスクを作成
    blueresult = cv2.bitwise_and(imgblue, imgblue, mask=blue_mask) # 元画像とマスクを合成
    return blueresult




if __name__ == '__main__':
    mainred()
    mainblue()

#四隅の角の検出
#画像読み込み
imgred = cv2.imread(imgred_name)
imgblue = cv2.imread(imgblue_name)

#グレースケールに変換
grayred = cv2.cvtColor(imgred,cv2.COLOR_BGR2GRAY)
grayblue = cv2.cvtColor(imgblue,cv2.COLOR_BGR2GRAY)

#空のリスト作成
xvaluered = []
yvaluered = []
xvalueblue = []
yvalueblue = []

#コーナー検出
cornersred = cv2.goodFeaturesToTrack(grayred,100,0.5,10)
cornersred = np.int0(cornersred)
cornersblue = cv2.goodFeaturesToTrack(grayblue,100,0.5,10)
cornersblue = np.int0(cornersblue)



#画像の読み取り部可視化
#print("--赤（ｘ軸）--")
for i in cornersred:
    x,y = i.ravel()
    cv2.circle(imgred,
           center=(x,y),
           radius=3,
           color=(0, 255, 0),
           thickness=3,
           lineType=cv2.LINE_4,
           shift=0)
    #print(x,y)
    xvaluered.append(x)
    yvaluered.append(y)
    
#print("--青（ｙ軸）--")
for i in cornersblue:
    x,y = i.ravel()
    cv2.circle(imgblue,
           center=(x,y),
           radius=3,
           color=(0, 255, 0),
           thickness=3,
           lineType=cv2.LINE_4,
           shift=0)
    #print(x,y)
    xvalueblue.append(x)
    yvalueblue.append(y)

"""
print("--------------------------------------------bluex")
print(xvalueblue)
print("--------------------------------------------bluey")
print(yvalueblue)
"""

#画像書き出し
#下記テスト表示用
cv2.namedWindow('imgred', cv2.WINDOW_NORMAL)
cv2.imshow("imgred", imgred)

cv2.namedWindow('imgblue', cv2.WINDOW_NORMAL)
cv2.imshow("imgblue", imgblue)

cv2.waitKey(0)
cv2.destroyAllWindows()

"""
下記計算処理------------------------------------------------------
赤（x軸）
"""

#（ｘ、ｙ）になるようにリストに格納
val_red = ([])
while 0 <= len(yvaluered)-1:
    y = yvaluered.pop(0)
    x = xvaluered.pop(0)
    val_red.insert(0,[x, y])
    
# print(val)
#ｙ軸を基準として小さい順に並び替え
#2つ単位で長さを求めていく
val_red.sort(reverse=False, key=lambda x:x[1])

#print(val_red)


red =np.array([[[0,0]],])
distance = []
error = np.array([[[0,0]],])
#print(red)
#print(val_red[0])

x = val_red[0]
x =np.array([[x]])

while len(val_red) >= 0:
    #0.1の比較、誤差１以内
    if (val_red[0][1]+1 == val_red[1][1] or val_red[0][1] == val_red[1][1]) and (x[0,0][1] - val_red[0][1] == 0 or x[0,0][1] - val_red[0][1] == -1):
        
        #０番目を格納
        x = []
        x = val_red.pop(0)
        x =np.array([[x]])
        red = np.append(red,x,axis=0)
        

        x = []
        x = val_red.pop(0)
        x =np.array([[x]])
        red = np.append(red,x,axis=0)
        
        """
        print(len(red)-1)
        print("------------------------l")
        print(red)
        """
        #break
        
        
    else:
        
        if len(red)-1 == 2:
            red = np.delete(red, 0, 0)
            #2の場合の処理
            #print("2-----")
            distance.append(np.linalg.norm(red[0]-red[1]))
            red =np.array([[[0,0]],])
            x = val_red[0]
            x =np.array([[x]])
            
        elif len(red)-1 == 4:
            red = np.delete(red, 0, 0)
            #4の場合の処理
            #print("4-----")
            red = np.sort(red, axis=0)
            #2辺の長さを求める
            distance.append(np.linalg.norm(red[0]-red[1]))
            distance.append(np.linalg.norm(red[2]-red[3]))
            #動作用の変数の初期化
            red =np.array([[[0,0]],])
            x = val_red[0]
            x =np.array([[x]])
            
        elif len(red)-1 == 6:
            red = np.delete(red, 0, 0)
            #6の場合の処理
            #print("6-----")
            red = np.sort(red, axis=0)
            distance.append(np.linalg.norm(red[0]-red[1]))
            distance.append(np.linalg.norm(red[2]-red[3]))
            distance.append(np.linalg.norm(red[4]-red[5]))
            red =np.array([[[0,0]],])
            x = val_red[0]
            x =np.array([[x]])
            
        elif len(red)-1 == 8:
            red = np.delete(red, 0, 0)
            #8の場合の処理
            #print("8-----")
            red = np.sort(red, axis=0)
            distance.append(np.linalg.norm(red[0]-red[1]))
            distance.append(np.linalg.norm(red[2]-red[3]))
            distance.append(np.linalg.norm(red[4]-red[5]))
            distance.append(np.linalg.norm(red[6]-red[7]))
            red =np.array([[[0,0]],])
            x = val_red[0]
            x =np.array([[x]])
            
        elif len(red)-1 == 1:
            print("error")
        else:
            
            """
            print("error")
            
            print("残り　",len(val_red))
            print("最後",x[0,0][1])
            print("次",val_red[1])
            print(x[0,0][1] - val_red[0][1])
            print(distance)
            """
            break

"""
下記計算処理------------------------------------------------------
青（ｙ軸）
"""


#（ｘ、ｙ）になるようにリストに格納
val_blue = ([])
while 0 <= len(yvalueblue)-1:
    y = yvalueblue.pop(0)
    x = xvalueblue.pop(0)
    val_blue.insert(0,[x, y])
    
# print(val)
#ｙ軸を基準として小さい順に並び替え
#2つ単位で長さを求めていく
val_blue.sort(reverse=False, key=lambda x:x[0])

#print(val_blue)


blue =np.array([[[0,0]],])

error = np.array([[[0,0]],])
#print(blue)
#print(val_blue[0])

x = val_blue[0]
x =np.array([[x]])

while len(val_blue) > 0:
    #0.1の比較、誤差１以内
    if (val_blue[0][0]+1 == val_blue[1][0] or val_blue[0][0] == val_blue[1][0]) and (x[0,0][0] - val_blue[0][0] == 0 or x[0,0][0] - val_blue[0][0] == -1):
        
        #０番目を格納
        x = []
        x = val_blue.pop(0)
        x =np.array([[x]])
        blue = np.append(blue,x,axis=0)
        

        x = []
        x = val_blue.pop(0)
        x =np.array([[x]])
        blue = np.append(blue,x,axis=0)
        
        
        #print(len(val_blue))
        #print("------------------------l")
        #print(blue)
        
        
        
        
        
        #break
        
        
    else:

        if len(blue)-1 == 2:
            blue = np.delete(blue, 0, 0)
            #2の場合の処理
            #print("2-----")
            distance.append(np.linalg.norm(blue[0]-blue[1]))
            blue =np.array([[[0,0]],])
            x = val_blue[0]
            x =np.array([[x]])
            
            
        elif len(blue)-1 == 4:
            blue = np.delete(blue, 0, 0)
            #4の場合の処理
            #print("4-----")
            blue = np.sort(blue, axis=0)
            #2辺の長さを求める
            distance.append(np.linalg.norm(blue[0]-blue[1]))
            distance.append(np.linalg.norm(blue[2]-blue[3]))
            #動作用の変数の初期化
            blue =np.array([[[0,0]],])
            x = val_blue[0]
            x =np.array([[x]])
            
        elif len(blue)-1 == 6:
            blue = np.delete(blue, 0, 0)
            #6の場合の処理
            #print("6-----")
            blue = np.sort(blue, axis=0)
            distance.append(np.linalg.norm(blue[0]-blue[1]))
            distance.append(np.linalg.norm(blue[2]-blue[3]))
            distance.append(np.linalg.norm(blue[4]-blue[5]))
            blue =np.array([[[0,0]],])
            x = val_blue[0]
            x =np.array([[x]])
            
        elif len(blue)-1 == 8:
            blue = np.delete(blue, 0, 0)
            #8の場合の処理
            #print("8-----")
            blue = np.sort(blue, axis=0)
            distance.append(np.linalg.norm(blue[0]-blue[1]))
            distance.append(np.linalg.norm(blue[2]-blue[3]))
            distance.append(np.linalg.norm(blue[4]-blue[5]))
            distance.append(np.linalg.norm(blue[6]-blue[7]))
            blue =np.array([[[0,0]],])
            x = val_blue[0]
            x =np.array([[x]])
            
        elif len(blue)-1 == 1:
            print("error")
        else:
            
            """
            print("error")
            
            print("残り　",len(val_blue))
            print("最後",x[0,0][1])
            print("次",val_blue[1])
            print(x[0,0][1] - val_blue[0][1])
            print(distance)
            """
            break
        
        
"""
尺寸に変換処理-----------------
"""
#syaku[6][4.5][3][1.5][1][0.5][0.25][0.15]とする
deffalt = [6,4.5,3,2.5,1.5,1,0.5,0.25,0.15]
syaku = [0,0,0,0,0,0,0,0,0]
#distance[4]を3尺の基準とする。
#1尺
syaku1 = 66.66749999479173


#6尺から順に計算していく
def calculation(num):
    for i in range(len(deffalt)):  #7種分繰り返す
        if num >= deffalt[i]:
            sum = num // deffalt[i]
            syaku[i] = syaku[i] + np.round(sum) #元ある数値に追加,端数切捨て
            
            #syaku.insert(i , syaku[i] + (num // deffalt[i]))
            num = num % deffalt[i]
            
            #下記3行実行確認用
            #print(deffalt[i],"尺",sum,i)    
        #else:
            #print(deffalt[i] ,"-----")


#繰り返し処理
for i in range(len(distance)):
    num = distance[i]/syaku1
    calculation(num)
    #print(syaku)

#必要枚数表示

for i in range(len(syaku)):
    print(deffalt[i],"尺",syaku[i],"枚")