from flask import Flask, request, json, send_file
import zipfile
from datetime import datetime
import tempfile
from PIL import Image, ImageDraw, ImageFont
import re

app = Flask(__name__)

imageFiles = [
    {'file_name': '1-1.jpg', 'file_path': 'sample/sample2.jpg'},
    {'file_name': '1-2.jpg', 'file_path': 'sample/sample.jpg'},
    {'file_name': '1-3.jpg', 'file_path': 'sample/sample2.jpg'},
    {'file_name': '2-1.jpg', 'file_path': 'sample/sample2.jpg'},
    {'file_name': '2-2.jpg', 'file_path': 'sample/sample.jpg'},
    {'file_name': '2-3.jpg', 'file_path': 'sample/sample2.jpg'},
    {'file_name': '3-1.jpg', 'file_path': 'sample/sample2.jpg'},
    {'file_name': '3-2.jpg', 'file_path': 'sample/sample.jpg'},
]
def getNumberFromStr(str, pos):
    return int(re.findall(r"[0-9]+", str)[pos]) 

daiMax = max(
    map(lambda i: getNumberFromStr(i['file_name'],0), imageFiles )
)
danMax = max(
    map(lambda i: getNumberFromStr(i['file_name'],1), imageFiles )
)
print(daiMax, danMax)

cellSize=200    # 各サムネイルの一辺のサイズ（正方形）
cellFooterHeight = 30
cellMergin = 15
headerHeight = 100  # タイトルの高さ
paperWidth = cellSize * daiMax + cellMergin * (daiMax -1) 
paperHeight = headerHeight + ( cellSize + cellFooterHeight) * danMax + cellMergin * (danMax + 1) 


img = Image.new('RGB', (paperWidth, paperHeight),'white')
draw = ImageDraw.Draw(img)  # im上のImageDrawインスタンスを作る
fnt = ImageFont.truetype('./Kosugi-Regular.ttf',30)
draw.text((cellMergin,cellMergin),"棚画像一覧", font=fnt, fill=(0,0,0,255))
thumbnail = Image.open('sample/sample2.jpg')
w, h = thumbnail.size
thumbnail = thumbnail.resize((int(w/20), int(h/20)))
# img.paste(thumbnail, (cellMergin, cellMergin + headerHeight))


# for(int i = 0; i < 10; i++):
draw.rectangle((
    cellMergin + (cellSize + cellMergin ) * 0 ,    headerHeight + (cellSize + cellFooterHeight +  cellMergin ) * 0,
    cellMergin + (cellSize + cellMergin ) * 0 + cellSize,    headerHeight + (cellSize + cellFooterHeight +  cellMergin ) * 0 + cellSize
    ), fill=128)

img.save('index.jpg','JPEG')
 