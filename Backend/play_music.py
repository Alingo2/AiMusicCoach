from mingus.midi import fluidsynth
import json
from mingus.containers import Bar
from mingus.containers import Track
from mingus.containers import Note
from mingus.midi.midi_track import MidiTrack
from mingus.midi.midi_file_out import MidiFile
import os

def tran(x):
    if x >= 'a':
        return ord(x) - 87
    elif x == '0':
        return 0.5
    else:
        return float(x)

def play_Music(filename):
    f = open(filename, 'rb')
    data = json.loads(f.read(), encoding='utf8')
    f.close()

    n = data['音符']
    h = data['音高']
    r = data['节拍']
    l = data['组成']
    k = data['调性']
    t = Track()
    b = Bar('C', (4, 4))
    b.place_rest(1)
    t.add_bar(b)
    name = 'CDEFGAB'
    symbol = '!@#$%^&'

    def tran(x):
        if x >= 'a':
            return ord(x) - 87
        elif x == '0':
            return 0.5
        else:
            return float(x)

    f = open(filename, 'rb')
    data = json.loads(f.read(), encoding='utf8')
    f.close()

    n = data['音符']
    h = data['音高']
    r = data['节拍']
    l = data['组成']
    k = data['调性']
    t = Track()
    b = Bar('C', (4, 4))
    b.place_rest(1)
    t.add_bar(b)
    name = 'CDEFGAB'
    symbol = '!@#$%^&'
    for i in range(len(l)):
        rn = list(map(tran, r[l[i]]))
        b = Bar('C', (4 * sum(rn)/8, 4))
        for j in range(len(n[l[i]])):
            if n[l[i]][j] == '0':
                b.place_rest(8 / rn[j])
            else:
                x = symbol.find(n[l[i]][j])
                if x == -1:
                    x = int(n[l[i]][j]) - 1
                    y = name[x]
                else:
                    y = name[x] + '#'
                    print(y)
                note = Note(y, int(h[l[i]][j]))
                note.transpose(k[i])
                b.place_notes(note, 8 / rn[j])
        t.add_bar(b)

    t2 = Track()
    b = Bar('C', (4, 4))
    b.place_rest(1)
    t2.add_bar(b)
    for i in range(int(sum(map(sum, map(lambda x: map(tran, r[x]), l)))) // 8):
        b = Bar('C', (4, 4))
        b.place_notes('C-3', 4)
        b.place_notes('C-7', 4)
        b.place_notes('C-5', 4)
        b.place_notes('C-7', 4)
        t2.add_bar(b)

    m = MidiFile()
    mt = MidiTrack(150)
    mt2 = MidiTrack(150)
    mt3 = MidiTrack(150)
    m.tracks = [mt,mt2,mt3]
    mt.set_instrument(1, 25)
    mt.play_Track(t)
    # for _, _, i in t2.get_notes():
    #     if i is not None:
    #         i[0].set_channel(2)
    # mt2.set_instrument(2, 115)
    # mt2.play_Track(t2)
    # for _, _, i in t.get_notes():
    #     if i is not None:
    #         i[0].set_channel(3)
    # mt3.set_instrument(3, 100)
    # mt3.track_data += mt3.controller_event(3, 7, 30)
    # mt3.play_Track(t)
    # m.write_file('D:/test.midi', False)
    # for i in range(len(l)):
    #     rn = list(map(tran, r[l[i]]))
    #     b = Bar('C', (4 * sum(rn) / 8, 4))
    #     for j in range(len(n[l[i]])):
    #         # if i==0 and j==0:
    #         #     b.place_notes('D-4', 3)
    #         # el
    #         if n[l[i]][j] == '0':
    #             b.place_rest(1 / rn[j])
    #         else:
    #             x = symbol.find(n[l[i]][j])
    #             if x == -1:
    #                 x = int(n[l[i]][j]) - 1
    #                 y = name[x]
    #             else:
    #                 y = name[x] + '#'
    #                 print(y)
    #
    #             note = Note(y, int(h[l[i]][j]))
    #             note.transpose(k[i])
    #             #print(note)
    #             print(rn[j])
    #             #print(b)
    #             b.place_notes(note, 1 / rn[j])
    #     t.add_bar(b)
    #     print(b)

    fluidsynth.init("D:\MyCode\MyPython\AiMusicCoach\GeneralUserSoftSynth\GeneralUserSoftSynth.sf2")
    fluidsynth.set_instrument(1, 1)            #24=Nylon Guitar
                                                # 25=Steel Guitar
                                                # 26=Jazz Guitar
                                                # 27=Clean Guitar
                                                # 28=Muted Guitar
                                                # 29=Overdrive Guitar
                                                # 30=Distortion Guitar
    m.write_file('D:\MyCode\MyPython\AiMusicCoach\Backend\music_file\mysong.midi', False)
    os.system("d: && cd D:\\MyCode\\MyPython\\AiMusicCoach\\fluidsynth-x64\\bin && fluidsynth -F mysong.wav D:/MyCode/MyPython/AiMusicCoach/GeneralUserSoftSynth/GeneralUserSoftSynth.sf2 D:\MyCode\MyPython\AiMusicCoach\Backend\music_file\mysong.midi")
    fluidsynth.play_Track(t, channel=1, bpm=150)

    # m = MidiFile()
    # MidiTrack(150).play_Track(t)
    # # m.tracks=[mt]
    # mt.set_instrument(1, 11)
    # mt.play_Track(t)
    # mt2 = MidiTrack(150)
    # mt3 = MidiTrack(150)
    # m.tracks = [mt, mt2, mt3]
    # mt.set_instrument(1, 11)

