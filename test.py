from flask import Flask, request, json, send_file
import zipfile
from datetime import datetime
import tempfile
from PIL import Image, ImageDraw, ImageFont
import re
from functools import reduce

app = Flask(__name__)

imageFiles = [
    {'file_name': '1-1.jpg', 'file_path': 'sample/sample3.jpg'},
    {'file_name': '1-2.jpg', 'file_path': 'sample/sample.jpg'},
    {'file_name': '1-3.jpg', 'file_path': 'sample/sample3.jpg'},
    {'file_name': '2-1.jpg', 'file_path': 'sample/sample2.jpg'},
    {'file_name': '2-2.jpg', 'file_path': 'sample/sample3.jpg'},
    {'file_name': '2-3.jpg', 'file_path': 'sample/sample3.jpg'},
    {'file_name': '3-1.jpg', 'file_path': 'sample/sample2.jpg'},
    {'file_name': '3-2.jpg', 'file_path': 'sample/sample3.jpg'},
    {'file_name': '4-1.jpg', 'file_path': 'sample/sample.jpg'},
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
headerHeight = 70  # タイトルの高さ
paperWidth = cellMergin + ( cellSize + cellMergin ) * daiMax 
paperHeight = headerHeight + ( cellSize + cellFooterHeight) * danMax + cellMergin * (danMax + 1) 


img = Image.new('RGB', (paperWidth, paperHeight),'white')
draw = ImageDraw.Draw(img)  # im上のImageDrawインスタンスを作る
titleFont = ImageFont.truetype('./Kosugi-Regular.ttf',30)
cellFont = ImageFont.truetype('./Kosugi-Regular.ttf',20)
draw.text((cellMergin,cellMergin),"棚画像一覧", font=titleFont, fill=(0,0,0,255))
thumbnail = Image.open('sample/sample2.jpg')
w, h = thumbnail.size
thumbnail = thumbnail.resize((int(w/20), int(h/20)))
# img.paste(thumbnail, (cellMergin, cellMergin + headerHeight))

def findObjectByFileName(fileName, items):
    return reduce(lambda s,i: i if i['file_name']==fileName else s, items, None )

def stretchSize(parentWidth, parentHeight, childWidth, childHeight):
    # width基準にストレッチ
    height = int(parentWidth / childWidth * childHeight)
    if (parentHeight > height):
        return { "width": parentWidth, "height": height, "base": 'width' }
    # height基準にストレッチ
    width = int(parentHeight / childHeight * childWidth)
    return { "width": width, "height": parentHeight, "base": 'height' }



print(findObjectByFileName('2-5.jpg',imageFiles))

for dai in range(daiMax):
    for dan in range(danMax):
        fileObject = findObjectByFileName('{0}-{1}.jpg'.format(dai+1, dan+1), imageFiles)
        x1 = cellMergin + (cellSize + cellMergin ) * dai
        y1 = headerHeight + (cellSize + cellFooterHeight +  cellMergin ) * dan
        x2 = cellMergin + (cellSize + cellMergin ) * dai + cellSize
        y2 = headerHeight + (cellSize + cellFooterHeight +  cellMergin ) * dan + cellSize
        lineColor = (200,200,200,255)
        if fileObject:
            thumbnail = Image.open(fileObject['file_path'])
            w, h = thumbnail.size
            size = stretchSize(cellSize, cellSize, w, h)
            thumbnail = thumbnail.resize((size['width'], size['height']))
            draw.rectangle(( x1, y1, x2, y2 ), outline=lineColor,width=2)
            img.paste(thumbnail, (x1+ int((cellSize - size['width'])/2), y1 + int((cellSize - size['height'])/2)))
            # draw.rectangle(( x1, y1, x2, y2 ), outline=(0,255,0,255),width=10)
            draw.text((x1,y1+cellSize+cellFooterHeight/4),fileObject['file_name'], font=cellFont, fill=(0,0,0,255))
        else:
            draw.rectangle(( x1, y1, x2, y2 ), outline=lineColor,width=2)
            draw.line(( x1, y1, x2, y2 ), fill=lineColor)
            draw.line(( x2, y1, x1, y2 ), fill=lineColor)
            draw.text((x1,y1+cellSize+cellFooterHeight/4),'(no picture)', font=cellFont, fill=(0,0,0,255))

img.save('index.jpg','JPEG')
 