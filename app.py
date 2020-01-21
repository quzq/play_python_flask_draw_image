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

dai_max = max(
    map(lambda i: getNumberFromStr(i['file_name'],0), imageFiles )
)
dan_max = max(
    map(lambda i: getNumberFromStr(i['file_name'],1), imageFiles )
)
print(dai_max, dan_max)

cellSize=200    # 各サムネイルの一辺のサイズ（正方形）
cellFooterHeight = 30
cellMergin = 15
headerHeight = 100  # タイトルの高さ
paperWidth = cellSize * dai_max + cellMergin * (dai_max -1) 
paperHeight = headerHeight + ( cellSize + cellFooterHeight) * dan_max + cellMergin * (dan_max + 1) 


img = Image.new('RGB', (paperWidth, paperHeight),'white')
draw = ImageDraw.Draw(img)  # im上のImageDrawインスタンスを作る
font = ImageFont.truetype('./Kosugi-Regular.ttf',10)
draw.text((cellMergin,cellMergin),"棚画像一覧", font=font, fill=(0,0,0,255))
thumbnail = Image.open('sample/sample2.jpg')
w, h = thumbnail.size
thumbnail = thumbnail.resize((int(w/20), int(h/20)))
img.paste(thumbnail, (cellMergin, cellMergin + headerHeight))

img.save('index.jpg','JPEG')
 
@app.route('/', methods=["GET"])
def hello():
    # 画像なので圧縮する必要なし
    with tempfile.NamedTemporaryFile(delete=True) as tf:
        with zipfile.ZipFile(tf, "w", compression=zipfile.ZIP_STORED) as new_zip:
            new_zip.write(
                'sample/index.jpg',
                arcname='images/index.jpg'
            )

            # for image_file in request.json["files"]:
            for image_file in imageFiles:
                new_zip.write(
                    image_file["file_path"],
                    # cp932にencodeする場合はarcnameにエンコード済み文字列を渡せばいける？
                    arcname='images/' + image_file["file_name"]
                )

        return send_file(tf.name)    # 画像なので圧縮する必要なし
    # with tempfile.NamedTemporaryFile(delete=True) as tf:
    #     with zipfile.ZipFile(tf, "w", compression=zipfile.ZIP_STORED) as new_zip:
    #         new_zip.write(
    #             'sample/sample.jpg',
    #             # cp932にencodeする場合はarcnameにエンコード済み文字列を渡せばいける？
    #             arcname='sample.jpg'
    #         )
        
    #     return send_file(
    #         tf.name,
    #         attachment_filename='images.zip',
    #         mimetype='application/zip'
    #     )
    # with tempfile.NamedTemporaryFile(mode="wb") as jpg:
    #     hello = "Hello world"
    #     jpg.write(b"Hello World!")
    #     return send_file(tf.name)
 
if __name__ == "__main__":
    app.run(debug=True)