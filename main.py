# by:wzy

from urllib import request
import cv2
import multiprocessing
import threading

listPossible = []


def getHead(number, id):
    url = 'http://q1.qlogo.cn/g?b=qq&nk=' + str(number) + '&s=100'
    response = request.urlopen(url)
    for header in response.getheaders():
        if header[0] == "X-Delay":
            request.urlretrieve(url, './getHead/getHead' + str(id) + '.jpg')
            return True
    return False
    # if len(response.getheaders()) == 17:
    #     request.urlretrieve(url, './getHead/getHead' + str(id) + '.jpg')
    #     return True
    # else:
    #     return False


def aHash(img):
    img = cv2.resize(img, (8, 8))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    s = 0
    hash_str = ''
    for i in range(8):
        for j in range(8):
            s = s + gray[i, j]
    avg = s / 64
    for i in range(8):
        for j in range(8):
            if gray[i, j] > avg:
                hash_str = hash_str + '1'
            else:
                hash_str = hash_str + '0'
    return hash_str


def cmpHash(hash1, hash2):
    n = 0
    if len(hash1) != len(hash2):
        return -1
    for i in range(len(hash1)):
        if hash1[i] != hash2[i]:
            n = n + 1
    return n


def work(id, begin, end):
    filename = 'possibleQQ.txt'
    QQnumberInit = begin
    while int(QQnumberInit) < end:
        try:
            assert getHead(QQnumberInit, id)
            img1 = cv2.imread('./getHead/getHead' + str(id) + '.jpg')
            img2 = cv2.imread('./target/target.jpg')
            if img1 is None:
                assert False
            hash1 = aHash(img1)
            hash2 = aHash(img2)
            n = cmpHash(hash1, hash2)
            print(str(id) + '号线程\t剩余：' + str(int(end - int(QQnumberInit))) + '次，正在比较账号：', int(QQnumberInit),
                  '均值哈希算法相似度为：',
                  100 - n, '%')
            if (100 - n) > 95:
                listPossible.append(QQnumberInit + '，相似度：' + str(100 - n) + '%')
                with open(filename, 'a') as file_object:
                    file_object.write('账号：' + QQnumberInit + '，相似度：' + str(100 - n) + '%\n')
            QQnumberInit = str(int(QQnumberInit) + 1)
        except AssertionError:
            print(str(id) + '号线程\t剩余：' + str(int(end - int(QQnumberInit))) + '次，账号：', int(QQnumberInit), '不存在')
            QQnumberInit = str(int(QQnumberInit) + 1)


def run(QQnumberBegin, QQnumberEnd):
    process = 0
    while process < (multiprocessing.cpu_count() * 4):
        threading.Thread(target=work, args=(process,
                                            QQnumberBegin + (
                                                    QQnumberEnd - QQnumberBegin) / multiprocessing.cpu_count() * process,
                                            QQnumberBegin + (
                                                    QQnumberEnd - QQnumberBegin) / multiprocessing.cpu_count() * (
                                                    process + 1) - 1)).start()
        process += 1


if __name__ == "__main__":
    run(1400000000, 1500000000)