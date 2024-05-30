import os
from flask import Flask, render_template

app = Flask(__name__)
@app.route('/')
def index():
# 获取文件夹下所有文件名
    image_names = os.listdir('static')  # ['my_k.png', 'my_bar.png', 'my_line.png', 'my_pie.png', 'my_scatter.png']
    image_names = [url for url in image_names if url.split('.')[1] == 'png']
    # image_name = 'my_line.png'
    return render_template('index.html', image_names=image_names)

if __name__ == '__main__':

    app.run(host='0.0.0.0',port=9000)