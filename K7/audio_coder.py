import wave

def encode_lsb_audio(audio_path, message, output_path):
    with wave.open(audio_path, 'rb') as audio:
        params = audio.getparams()
        frames = audio.readframes(params.nframes)

    binary_message = ''.join(format(byte, '08b') for byte in message.encode('utf-8'))
    binary_message += '00000000'
    if len(binary_message) > len(frames) * 8:
        raise ValueError("Сообщение слишком большое для этого аудиофайла")

    frames = bytearray(frames)
    index = 0
    for i in range(len(frames)):
        if index < len(binary_message):
            frames[i] = (frames[i] & 0xFE) | int(binary_message[index])
            index += 1

    with wave.open(output_path, 'wb') as audio_out:
        audio_out.setparams(params)
        audio_out.writeframes(frames)

def decode_lsb_audio(audio_path):
    with wave.open(audio_path, 'rb') as audio:
        frames = audio.readframes(audio.getnframes())

    binary_message = ''

    for byte in frames:
        binary_message += str(byte & 1)

    message_bytes = bytearray()
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i+8]
        if byte == '00000000':
            break
        message_bytes.append(int(byte, 2))

    message = message_bytes.decode('utf-8')
    return message


if __name__ == "__main__":
    audio_path = 'audio/original.wav'
    output_path = 'audio/secret1.wav'

    message1 = 'Привет!'
    encode_lsb_audio(audio_path, message1, output_path)
    decoded_message1 = decode_lsb_audio(output_path)
    print('Декодированное сообщение 1:', decoded_message1)

    audio_path = 'audio/original.wav'
    output_path = 'audio/secret2.wav'

    message2 = 'Это секретное сообщение для лабораторной работы по информационной безопасности.'
    encode_lsb_audio(audio_path, message2, output_path)
    decoded_message2 = decode_lsb_audio(output_path)
    print('Декодированное сообщение 2:', decoded_message2)

    audio_path = 'audio/original.wav'
    output_path = 'audio/secret3.wav'

    message3 = ('Метод LSB (англ. least significant bit - наименьший значащий бит, НЗБ) '
                'заключается в замене последних значащих битов в контейнере (изображения, аудио или видеозаписи) '
                'на биты скрываемого сообщения. Разница между пустым и заполненным контейнерами '
                'должна быть не ощутима для органов восприятия человека.')
    encode_lsb_audio(audio_path, message3, output_path)
    decoded_message3 = decode_lsb_audio(output_path)
    print('Декодированное сообщение 3:', decoded_message3)
