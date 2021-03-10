import math
import wave
import struct

FREQUENCY = {"A": 440, "B": 494, "C": 523, "D": 587, "E": 659, "F": 698, "G": 784, "Q": 0}
SAMPLE_RATE = 2000
MAX_VOLUME = 32767
MIN_VOLUME = -32768

def main():
    main_menu()


def main_menu():
    """
    shows a main menu with all options available
    """

    while True:
        print("Welcome to wave editor!\n1. Change .wav file\n2. Create sample\n3. Exit")
        main_menu_choice = input("Choose option from list above: ")
        if main_menu_choice == "1":
            filename = input("Enter the file name you want to work with: ")
            rate, data = load_wave(filename)
            data = change_menu(data)
            new_filename = input("Enter the name for your file: ")
            save_wave(rate, data, new_filename)
            del data, rate
        elif main_menu_choice == "2":
            data = sound_creating()
            data = change_menu(data)
            new_filename = input("Enter the name for your file: ")
            save_wave(SAMPLE_RATE, data, new_filename)
            del data
        elif main_menu_choice == "3":
            break
        else:
            print("Wrong input. Try again.")
            continue


def change_menu(data):
    """
    shows the editing menu to user with all available options
    :param data: list of lists contains audio data
    :return: list of lists contains audio data
    """

    while True:
        print("1. Inversion\n"
              "2. Negative sound\n"
              "3. Increase speed\n"
              "4. Decrease speed\n"
              "5. Increase volume\n"
              "6. Decrease volume\n"
              "7. Low pass filter\n"
              "8. Exit to main menu")
        changing_choice = input("Choose one of options below: ")
        if changing_choice == "1":
            data = inversion(data)
        elif changing_choice == "2":
            data = negative_sound(data)
        elif changing_choice == "3":
            data = speed_increase(data)
        elif changing_choice == "4":
            data = speed_decrease(data)
        elif changing_choice == "5":
            data = volume_up(data)
        elif changing_choice == "6":
            data = volume_down(data)
        elif changing_choice == "7":
            data = low_pass_filter(data)
        elif changing_choice == "8":
            return data
        else:
            print("No option available. Please try again.")
            continue


def inversion(data):
    """
    function does inversion to list of list using slice method
    :param data: list of lists contains audio data
    :return: list of lists contains audio data
    """
    data = data[::-1]
    data = limit_checker(data)
    return data

def negative_sound(data):
    """
    function multiplies all elements in list of lists by (-1)
    :param data: list of lists contains audio data
    :return: list of lists contains audio data
    """
    data = [[-j for j in i] for i in data]
    data = limit_checker(data)
    return data

def speed_increase(data):
    """
    function deletes all elements with even index from list of lists
    :param data: list of lists contains audio data
    :return: list of lists contains audio data
    """
    data = [o for i, o in enumerate(data) if i % 2 == 0]
    data = limit_checker(data)
    return data

def speed_decrease(data):
    """
    function counts arithmetic mean between adjacent elements with similar indexes and adds them between the elements
    :param data: list of lists contains audio data
    :return: list of lists contains audio data
    """
    new_data = []
    for i in range(len(data) - 1):
        new_data.append(data[i])
        temp = [(data[i][0] + data[i + 1][0]) // 2, (data[i][1] + data[i + 1][1]) // 2]
        new_data.append(temp)
    new_data.append(data[-1])
    data = new_data
    data = limit_checker(data)
    return data

def volume_up(data):
    """
    function multiplies every element in list of lists by 1.2 using list comprehension but with limit of values.
    :param data: list of lists contains audio data
    :return: list of lists contains audio data
    """
    data = [[max(MIN_VOLUME, int(j * 1.2)) if j < 0 else min(MAX_VOLUME, int(j * 1.2)) for j in i] for i in data]
    data = limit_checker(data)
    return data

def volume_down(data):
    """
    function divides every element in list of list by 1.2 using list comprehension with same limits
    :param data: list of lists contains audio data
    :return: list of lists contains audio data
    """
    data = [[int(j / 1.2) for j in i] for i in data]
    data = limit_checker(data)
    return data

def low_pass_filter(data):
    """
    function counts and adds arithmetic mean from adjacent elements
    :param data: list of lists contains audio data
    :return: list of lists contains audio data
    """
    n = len(data)
    new_data = [[(data[0][0] + data[1][0]) // 2, (data[0][1] + data[1][1]) // 2]]
    for i in range(1, len(data) - 1):
        temp = [(data[i - 1][0] + data[i][0] + data[i + 1][0]) // 3,
                (data[i - 1][1] + data[i][1] + data[i + 1][1]) // 3]
        new_data.append(temp)
    last_list = [int((data[n - 1][0] + data[n - 2][0]) / 2), int((data[n - 1][1] + data[n - 2][1]) / 2)]
    new_data.append(last_list)
    data = new_data
    data = limit_checker(data)
    return data

def get_data():
    """
    function sorts all data from input file into one list in format [NOTE, NUMBER, NOTE, NUMBER, ...]
    :return: list of lists contains audio data
    """
    name = input("Enter the name of file you want to use: ")
    file = open(name, "r")
    data = file.read().replace("\n", " ").split()
    return data

def get_list_length(cur_duration):
    """
    function calculates and returns us length of note list
    :param cur_duration: duration of playing
    :return: length of list
    """
    duration = int(cur_duration)
    if duration == 16:
        length_note_list = SAMPLE_RATE
    else:
        length_note_list = int(SAMPLE_RATE*(duration/16))
    return length_note_list

def sound_creating():
    """
    function creates file with audio data
    :return: list of lists contains audio data
    """
    input_list = get_data()
    note = input_list[::2]
    duration = input_list[1::2]
    data = []
    for i_note, i_dur in zip(note, duration):
        for i in range(get_list_length(i_dur)):
            if i_note != "Q":
                samples_per_cycle = SAMPLE_RATE / FREQUENCY[i_note]
                val = int(MAX_VOLUME * math.sin((math.pi * 2 * i) / samples_per_cycle))
            else:
                val = 0
            data.append([val, val])
    return data

def limit_checker(data):
    """
    functions checks the audio data list for breaking minimal and maximal limits of volume.
    :param data: list of lists contains audio data
    :return: list of lists contains audio data
    """
    for i in range(len(data)):
        if int((data[i][0] + data[i][1]) // 2) > MAX_VOLUME:
            data[i][0] = MAX_VOLUME
            data[i][1] = MAX_VOLUME
        elif int((data[i][0] + data[i][1]) // 2) < MIN_VOLUME:
            data[i][0] = MIN_VOLUME
            data[i][1] = MIN_VOLUME
    return data

def load_wave(wave_filename):
    try :
        fin = wave.open(wave_filename,'r')
        num_frames = fin.getnframes()
        data = []
        while (fin.tell() < num_frames):
            frame = fin.readframes(1)
            data_p = []
            if fin.getsampwidth() == 1:
                data_p.append(struct.unpack('%dB'%(fin.getnchannels()), frame))
            elif fin.getsampwidth() == 2:
                data_p.append(struct.unpack('%dh'%(fin.getnchannels()), frame))
            else :
                fin.close()
                raise Exception('Unhandeled sample width')
            if fin.getnchannels() == 1 :
                data_p[0] = (data_p[0][0],data_p[0][0])
            elif fin.getnchannels() > 2 :
                data_p[0] = (data_p[0][0],data_p[0][1])
            if fin.getsampwidth() == 1 :
                data_p[0] = (256*(data_p[0][0]-128), 256*(data_p[0][1]-128))
            data.append(list(data_p[0]))
        fin.close()
        return fin.getframerate(), \
               data
    except KeyboardInterrupt:
        raise
    except :
        return -1

def save_wave(frame_rate, audio_data, wave_filename):
    try :
        fout = wave.open(wave_filename,'w')
        fout.setparams((2,
                        2,
                        frame_rate,
                        0,
                        'NONE',
                        'not compressed'))
        values = []
        for frame in audio_data:
            for data in frame:
                values.append(struct.pack('h', data))
        value_str = b"".join(values)
        fout.writeframes(value_str)
        fout.close()
        return 0
    except KeyboardInterrupt:
        raise
    except :
        return -1

if __name__ == "__main__":
    main()
