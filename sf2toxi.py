#!/usr/bin/python
#coding:utf-8

'''
This program is not completion.
The program purpose is soundfont2 export to xi(Fasttracker2)
'''

import sys
import re
from struct import * 
#------------sf2 variables------------------------------------------------------
shdr_size = 0
shdr_list = []
sample_name = ''
dwstart = 0
dwend = 0
dwstart_loop = 0
dwend_loop = 0
dwsample_rate = 0
byte_orig_pitch = 0
char_chPitch_correction = 0
w_sample_link = 0
sf_sample_link = 0
smpldata = ''
part_smpldata = ''
smpldata_size = 0
bit_per_second = 0
#--------------------------------------------------------------------------------
#---------------------xi variables-----------------------------------------------
extxi="Extended Instrument: " #x00
name=""   # Name,0x1A :x15
trkname="FastTracker v2.00"# Tracker name,f.e. "FastTracker v2.00" in FT2's case :x2c
major_version=2             # :x40
minor_version=1 :x41
samples_note_map='0'*96 :x42
volume_envelope[2]*24 :xA2
pannning_envelope[2]*24:xD2
volume_points_number[1]:x102
pannning_points_number   :x103
volume_sustain_point     :x104
volume_loop_start_point  :x105
volume_loop_end_point    :x106
panning_sustain_point    :x107
panning_loop_start_point :x108
panning_loop_end_point:x109
volume_type           :x10A
panning_type          :x10B
vibrato_type          :x10C
vibrato_sweep         :x10D
vibrato_depth         :x10E
vibrato_rate          :x10F
volume_fadeout :x110
extended_info  :x112
samples_number:x128
sample_length:x12A
sample_loop_start:x12E
sample_loop_length:x132
sample_volume:x136
sample_finetune:x137
sample_type:x138
sample_panning:x139
sample_transpose:x13A
sample_sample_name_length:x13B
sample_name:x13C

'''xi file structure
CHAR extxi[21];   //"Extended Instrument: " :x00
CHAR name[23];    //Name,0x1A :x15
CHAR trkname[20]; //Tracker name,f.e. "FastTracker v2.00" in FT2's case :x2c
BYTE major_version[1] :x40
BYTE minor_version[1] :x41
BYTE samples_note_map[1]*96 :x42
SHORT volume_envelope[2]*24 :xA2
SHORT pannning_envelope[2]*24:xD2
BYTE volume_points_number[1]:x102
BYTE pannning_points_number   [1]:x103
BYTE volume_sustain_point     [1]:x104
BYTE volume_loop_start_point  [1]:x105
BYTE volume_loop_end_point    [1]:x106
BYTE panning_sustain_point    [1]:x107
BYTE panning_loop_start_point [1]:x108
BYTE panning_loop_end_point[1]   :x109
BYTE volume_type           [1]   :x10A
BYTE panning_type          [1]   :x10B
BYTE vibrato_type          [1]   :x10C
BYTE vibrato_sweep         [1]   :x10D
BYTE vibrato_depth         [1]   :x10E
BYTE vibrato_rate          [1]   :x10F
UNSIGNED SHORT volume_fadeout[2] :x110
BYTE extended info [1]*22 :x112
BYTE samples_number[2]:x128
------looping samples number----------
INT sample_length[4]:x12A
INT sample_loop_start[4]:x12E
INT sample_loop_length[4]:x132
BYTE sample_volume[1]:x136
BYTE sample_finetune[1]:x137
BYTE sample_type[1]:x138
BYTE sample_panning[1]:x139
BYTE sample_transpose[1]:x13A
BYTE sample_sample_name_length[1]:x13B
CHAR sample_name[22]:x13C
--------------------------------------
DATA sample_datqa:x152
'''

#search pattern from sf2
argvs = sys.argv
print("searching "+argvs[1])

#open sf2. argv[1] is name of sf2
sf2 = open(argvs[1],'rb')
data=sf2.read()
sf2.close()

#search shdr chunk
matchOB = re.search(r'shdr',data)
shdr_size = unpack('<L',data[matchOB.end():matchOB.end()+4])
shdr_start = matchOB.end()+4
repeat = shdr_size[0]/46 # one sample data have 46 byte

for i in range(repeat):
    sample_name = data[shdr_start:shdr_start+20]
    dwstart = unpack('<L',data[shdr_start+20:shdr_start+24])
    dwend = unpack('<L',data[shdr_start+24:shdr_start+28])
    dwstart_loop = unpack('<L',data[shdr_start+28:shdr_start+32])
    dwend_loop = unpack('<L',data[shdr_start+32:shdr_start+36])
    dwsample_rate = unpack('<L',data[shdr_start+36:shdr_start+40])
    byte_orig_pitch = data[shdr_start+40]
    char_chPitch_correction = data[shdr_start+41]
    w_sample_link = unpack('<H',data[shdr_start+41:shdr_start+43])
    sf_sample_link = unpack('<H',data[shdr_start+43:shdr_start+45])
    shdr_start += 46
    shdr_list.append([sample_name,dwstart[0],dwend[0],dwstart_loop[0],dwend_loop[0],dwsample_rate[0],byte_orig_pitch[0],char_chPitch_correction[0],w_sample_link[0],sf_sample_link[0]])
    print(sample_name)
    print(dwstart)
    print(dwend)
    print(dwstart_loop)
    print(dwend_loop)
    print(dwsample_rate)
    print(byte_orig_pitch)
    print(char_chPitch_correction)
    print(w_sample_link)
    print(sf_sample_link)
for i in shdr_list:
    print(i)


matchOB = re.search(r'smpl',data)
if matchOB:
    print matchOB
    print matchOB.start()
    print matchOB.end()
    print matchOB.span()

smpldata_size = unpack('<L',data[matchOB.end():matchOB.end()+4])[0]
smpl_start = matchOB.end()+4
smpldata = data[smpl_start:smpl_start+smpldata_size]

for i in range(repeat):
    pass
