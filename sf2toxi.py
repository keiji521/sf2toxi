#!/usr/bin/python
#coding:utf-8

'''
This program is not completion.
The program purpose is soundfont2 export to xi(Fasttracker2)
'''
import os
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
minor_version=1 #:x41
samples_note_map=[0 for i in range(96)]#'0'*96 :x42
volume_envelope=[0 for i in range(24)]#[2]*24 :xA2
pannning_envelope=[0 for i in range(24)]#[2]*24:xD2
ppvolume_points_number=0#[1]:x102
pannning_points_number=0#   :x103
volume_sustain_point=0#   :x104
volume_loop_start_point=0# :x105
volume_loop_end_point=0#    :x106
panning_sustain_point=0#    :x107
panning_loop_start_point=0# :x108
panning_loop_end_point=0#:x109
volume_type=0#           :x10A
panning_type=0#          :x10B
vibrato_type=0#          :x10C
vibrato_sweep =0#        :x10D
vibrato_depth=0#         :x10E
vibrato_rate=0#          :x10F
volume_fadeout=0# :x110
extended_info=0#  :x112
samples_number=0#:x128
sample_length=0#:x12A
sample_loop_start=0#:x12E
sample_loop_length=0#:x132
sample_volume=100#:x136
sample_finetune=0#:x137
sample_type=0#:x138
sample_panning=0#:x139
sample_transpose=0#:x13A
sample_sample_name_length=0#:x13B
sample_name='sample001'#:x13C

'''xi file structure
CHAR extxi[21];   //"Extended Instrument :x00
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
dir_name = argvs[1].split('.')[0]
if len(argvs)<1:
	print('too less arguments')

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
    '''
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
    '''

'''
    TODO 
    spliting sample data by dwatart and dwend.
    
'''
matchOB = re.search(r'smpl',data)
if matchOB:
    print(matchOB)
    print(matchOB.start())
    print(matchOB.end())
    print(matchOB.span())

smpldata_size = unpack('<L',data[matchOB.end():matchOB.end()+4])[0]
smpl_start = matchOB.end()+4
smpldata = data[smpl_start:smpl_start+smpldata_size]
for i in range(repeat):
    shdr_list[i].append(smpldata[shdr_list[i][1]:shdr_list[i][2]])
'''
for i in shdr_list:
    print(i[0])
'''
try:
	os.mkdir(dir_name)
except(OSError):
	print('error has occured')
