from PIL import Image

def max_message_length(image_path):
    img = Image.open(image_path)
    width, height = img.size
    max_length_bits = 3 * width * height
    max_length_bytes = max_length_bits // 8
    return max_length_bytes

def encode_lsb(image_path, message, output_path):
    img = Image.open(image_path)
    width, height = img.size
    pixels = img.load()

    binary_message = ''.join(format(byte, '08b') for byte in message.encode('utf-8'))
    binary_message += '00000000'

    if len(binary_message) > width * height * 3:
        raise ValueError("Сообщение слишком большое для этого изображения")

    index = 0
    for y in range(height):
        for x in range(width):
            if img.mode == 'RGBA':
                r, g, b, a = pixels[x, y]
            else:
                r, g, b = pixels[x, y]
                a = 255

            if index < len(binary_message):
                r = (r & 0xFE) | int(binary_message[index])
                index += 1
            if index < len(binary_message):
                g = (g & 0xFE) | int(binary_message[index])
                index += 1
            if index < len(binary_message):
                b = (b & 0xFE) | int(binary_message[index])
                index += 1

            if img.mode == 'RGBA':
                pixels[x, y] = (r, g, b, a)
            else:
                pixels[x, y] = (r, g, b)

    img.save(output_path)

def decode_lsb(image_path):
    img = Image.open(image_path)
    width, height = img.size
    pixels = img.load()

    binary_message = ''

    for y in range(height):
        for x in range(width):
            if img.mode == 'RGBA':
                r, g, b, a = pixels[x, y]
            else:
                r, g, b = pixels[x, y]

            binary_message += str(r & 1)
            binary_message += str(g & 1)
            binary_message += str(b & 1)

    message_bytes = bytearray()
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i+8]
        if byte == '00000000':
            break
        message_bytes.append(int(byte, 2))

    message = message_bytes.decode('utf-8')
    return message


if __name__ == "__main__":
    image_path = 'images/original.png'
    output_path = 'images/secret1.png'

    message1 = 'Привет!'
    print(f'Максимальная длина сообщения: {max_message_length(image_path)} байт')
    encode_lsb(image_path, message1, output_path)
    decoded_message1 = decode_lsb(output_path)
    print('Декодированное сообщение 1:', decoded_message1)

    image_path = 'images/original.png'
    output_path = 'images/secret2.png'

    message2 = 'Это секретное сообщение для лабораторной работы по информационной безопасности.'
    print(f'Максимальная длина сообщения: {max_message_length(image_path)} байт')
    encode_lsb(image_path, message2, output_path)
    decoded_message2 = decode_lsb(output_path)
    print('Декодированное сообщение 2:', decoded_message2)

    image_path = 'images/original.png'
    output_path = 'images/secret3.png'

    message3 = ('Метод LSB (англ. least significant bit - наименьший значащий бит, НЗБ) '
                'заключается в замене последних значащих битов в контейнере (изображения, аудио или видеозаписи) '
                'на биты скрываемого сообщения. Разница между пустым и заполненным контейнерами '
                'должна быть не ощутима для органов восприятия человека.')
    print(f'Максимальная длина сообщения: {max_message_length(image_path)} байт')
    encode_lsb(image_path, message3, output_path)
    decoded_message3 = decode_lsb(output_path)
    print('Декодированное сообщение 3:', decoded_message3)
