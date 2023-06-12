TEXT TO SPEECH

파일 변경해서 저장하면
utils파일에도 변경해서 저장하기


1. upload wav, duration, metadata<br/>
mfa_to_npy에서 실행하고 생성된 ./dataset/kss/wavs_cut , ./dataset/kss/result/duration 파일들을 naturalspeech에 넣는다.<br/>
./data/kss/metadata.csv 의 확장자명을 txt로 변경한 뒤 naturalspeech에 넣는다.

2. cd workspace<br/>
%cd ./drive/MyDrive/naturalspeech

3. prepare tensorrt<br/>
https://developer.nvidia.com/nvidia-tensorrt-8x-download 에서 해당 환경과 맞는 tensorrt 로컬로 다운 후 naturalspeech폴더에 업로드

4. prerpare<br/>
pip install -r requirements.txt<br/>
python3 -m pip install --upgrade tensorrt<br/>
sudo dpkg -i nv-tensorrt-local-repo-ubuntu2004-8.6.0-cuda-11.8_1.0-1_amd64.deb<br/>
sudo cp /var/nv-tensorrt-local-repo-ubuntu2004-8.6.0-cuda-11.8/*-keyring.gpg /usr/share/keyrings/<br/>
sudo apt-get update<br/>
sudo apt-get install tensorrt

5. 업로드한 duration을 백업본으로, 모델 구동할 땐 durations폴더 사용<br/>
rm -rf durations<br/>
cp -r ./duration ./durations

6. 업로드한 wavs_cut을 백업본으로, 모델 구동할 땐 wavs폴더 사용<br/>
rm -rf ./wavs<br/>
cp -r ./wavs_cut ./wavs

7. wavs폴더을 심볼릭 링크<br/>
rm -rf DUMMY1<br/>
ln -s ./wavs DUMMY1

8. data split and make transcript<br/>
python make_transcript.py<br/>
(train, valid, test 비율 8:1:1)

9. make transcript.cleaned<br/>
python preprocess_texts.py

10. copy transcript utils folder<br/>
rm -rf ./utils/filelists<br/>
cp -r ./filelists ./utils/filelists/

11. torch 오류로 인해 functional.py 복사<br/>
(stft 오류로 인해 해결방법: https://github.com/coqui-ai/TTS/issues/2449)<br/>
!cp ./copy_error/functional.py /usr/local/lib/python3.9/dist-packages/torch/functional.py

12. warmup<br/>
python3 train.py -c configs/kss.json -m kss_warmup --warmup

13. attach_memory_bank<br/>
python3 attach_memory_bank.py -c configs/kss.json --weights_path logs/kss_warmup/G_200.pth

14. train<br/>
python3 train.py -c configs/kss.json -m kss_warmup

15. inference<br/>
text.txt에 한줄로 text입력한뒤 저장.<br/>
python inference.py
