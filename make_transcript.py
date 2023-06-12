import tqdm
import os
from sklearn.model_selection import train_test_split

check_wav = os.listdir('./wavs')
check_npy = os.listdir('./durations')
            
test_text = open('./filelists/transcript_refine_test.txt', 'w', encoding='UTF-8')
val_text = open('./filelists/transcript_refine_val.txt', 'w', encoding='UTF-8')
train_text = open('./filelists/transcript_refine_train.txt', 'w', encoding='UTF-8')

check_npy = [file.replace('.wav.npy', '.wav') for file in check_npy]

train_wav, test_wav = train_test_split(check_wav, test_size=0.2, shuffle=True)
test_wav, valid_wav = train_test_split(test_wav, test_size=0.5, shuffle=True)

with open('./metadata.txt', 'r', encoding='UTF-8') as f:
    for line in tqdm.tqdm(f):
        wav_file_path = line.split('|')[0] + '.wav'
        text = line.split('|')[2]

        if wav_file_path not in check_wav:
            continue
        if wav_file_path not in check_npy:
            continue

        if wav_file_path in test_wav:
            test_text.write(f'DUMMY1/{wav_file_path}|{text}\n')
        elif wav_file_path in valid_wav:
            val_text.write(f'DUMMY1/{wav_file_path}|{text}\n')
        else:
            train_text.write(f'DUMMY1/{wav_file_path}|{text}\n')

train_text.close()
val_text.close()
test_text.close()