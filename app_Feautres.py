from PIL import Image
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# Convert encoding data into 8-bit binary
# form using ASCII value of characters
def genData(data):
    # list of binary codes
    # of given data
    newd = []

    if isinstance(data, str):
        # For string input
        for i in data:
            newd.append(format(ord(i), '08b'))
    elif isinstance(data, bytes):
        # For bytes input
        for byte in data:
            newd.append(format(byte, '08b'))
    else:
        raise TypeError("Invalid data type. Expected string or bytes.")

    return newd


# Pixels are modified according to the
# 8-bit binary data and finally returned
def modPix(pix, data):
    datalist = genData(data)
    lendata = len(datalist)
    imdata = iter(pix)

    for i in range(lendata):

        # Extracting 3 pixels at a time
        pix = [value for value in imdata.__next__()[:3] +
               imdata.__next__()[:3] +
               imdata.__next__()[:3]]

        # Pixel value should be made
        # odd for 1 and even for 0
        for j in range(0, 8):
            if (datalist[i][j] == '0' and pix[j] % 2 != 0):
                pix[j] -= 1

            elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
                if (pix[j] != 0):
                    pix[j] -= 1
                else:
                    pix[j] += 1

        # Eighth pixel of every set tells
        # whether to stop or read further.
        # 0 means keep reading; 1 means the message is over.
        if (i == lendata - 1):
            if (pix[-1] % 2 == 0):
                if (pix[-1] != 0):
                    pix[-1] -= 1
                else:
                    pix[-1] += 1

        else:
            if (pix[-1] % 2 != 0):
                pix[-1] -= 1

        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]


def encrypt_data(key, data):
    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv
    encrypted_data = cipher.encrypt(pad(data.encode(), AES.block_size))
    return iv + encrypted_data


def decrypt_data(key, encrypted_data):
    iv = encrypted_data[:AES.block_size]
    encrypted_data = encrypted_data[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
    return decrypted_data.decode()


def encode_enc(newimg, data, key):
    w = newimg.size[0]
    (x, y) = (0, 0)

    encrypted_data = encrypt_data(key, data)

    for pixel in modPix(newimg.getdata(), encrypted_data):

        # Putting modified pixels in the new image
        newimg.putpixel((x, y), pixel)
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1


# Decode the data in the image
def unhide(key,img):
    encrypted_data = b''
    imgdata = iter(img.getdata())

    while (True):
        pixels = [value for value in imgdata.__next__()[:3] +
                  imgdata.__next__()[:3] +
                  imgdata.__next__()[:3]]

        # string of binary data
        binstr = ''

        for i in pixels[:8]:
            if (i % 2 == 0):
                binstr += '0'
            else:
                binstr += '1'

        encrypted_data += bytes([int(binstr, 2)])
        if (pixels[-1] % 2 != 0):
            break

    decrypted_data = decrypt_data(key, encrypted_data)
    return decrypted_data



