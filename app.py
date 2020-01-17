from flask import Flask, request, json, send_file
import zipfile
from datetime import datetime
import tempfile
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)

widthMergin = 20
heightMergin = 20
headerHeight = 100  # タイトルの高さ
imgWidth = 500
imgHeight = 500
img = Image.new('RGB', (imgWidth, imgHeight),'white')
draw = ImageDraw.Draw(img)  # im上のImageDrawインスタンスを作る
fnt = ImageFont.truetype('./Kosugi-Regular.ttf',30)
draw.text((widthMergin,heightMergin),"棚画像一覧", font=fnt, fill=(0,0,0,255))
thumbnail = Image.open('sample/sample2.jpg')
w, h = thumbnail.size
thumbnail = thumbnail.resize((int(w/20), int(h/20)))
img.paste(thumbnail, (widthMergin, heightMergin + headerHeight))

img.save('index.jpg','JPEG')
 
@app.route('/', methods=["GET"])
def hello():
    imageFiles = [
        {'file_name': 'sample2.jpg', 'file_path': 'sample/sample2.jpg'},
        {'file_name': 'sample.jpg', 'file_path': 'sample/sample.jpg'},
        ]
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