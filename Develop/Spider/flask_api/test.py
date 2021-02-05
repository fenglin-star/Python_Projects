import hashlib


if __name__ == '__main__':
    file_name = r"D:\PycharmProjects\Develop\flask_img\img\demo\2020\12\20\51447b3267534e6b83689afae2b1fdb2.png"
    with open(file_name, 'rb') as fp:
        data = fp.read()
    file_md5= hashlib.md5(data).hexdigest()
    print(file_md5)     # ac3ee699961c58ef80a78c2434efe0d0