# inference code
from models.models import (
    SynthesizerTrn,
)

from text.symbols import symbols

from utils import utils
from text import text_to_sequence, cleaned_text_to_sequence

from utils import commons
import torch
import scipy
import os

def get_text(text, hps):
    text_norm = text_to_sequence(text, hps.data.text_cleaners)
    if hps.data.add_blank:
        text_norm = commons.intersperse(text_norm, 0)
    text_norm = torch.LongTensor(text_norm)
    return text_norm

hps = utils.get_hparams_from_file('configs/kss.json')
model_name = 'G_500'
model_path = './logs/kss_warmup/' + model_name + '.pth' # you should change model_path
with open('./text.txt', 'r') as f:
    text = f.readline()
result_path = './result'

net_g = SynthesizerTrn(
    len(symbols),
    hps.data.filter_length // 2 + 1,
    hps.train.segment_size // hps.data.hop_length,
    hps.models,
).cuda(0)

net_g.attach_memory_bank(hps.models)

_, _, _, epoch_str = utils.load_checkpoint(
    model_path, net_g, None
)

net_g.eval()

x = get_text(text, hps).cuda().unsqueeze(0)
x_lengths = torch.LongTensor([x.size(1)]).cuda()

with torch.no_grad():
    y_hat, mask, *_ = net_g.infer(x, x_lengths, noise_scale=0.667, length_scale=1.1, max_len=1200)
    audio = y_hat[0, 0, :].cpu().numpy()

if not os.path.exists(result_path):
    os.makedirs(result_path)

scipy.io.wavfile.write(
    filename=os.path.join(result_path, model_name+'.wav'),
    rate=hps.data.sampling_rate,
    data=audio,
)