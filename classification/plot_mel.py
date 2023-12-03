import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

#############################################################################################
#############################################################################################
#Creating the subplots

fig = plt.figure(constrained_layout=True)
gs = GridSpec(2, 3, figure=fig)

py_ax = fig.add_subplot(gs[0, :])
py_ax.set_title("Melspectrogram of the original dataset (python)")

sample_axes = []
for i in range(3):
    sample_axes.append(fig.add_subplot(gs[1, i]))
    sample_axes[i].set_title(f"Sample {i}")

#############################################################################################
#############################################################################################
#Python melspec

from classification.utils.audio_student import AudioUtil, Feature_vector_DS
from classification.datasets import Dataset

def display(myds, cls_index, ax=plt):
    """
    Play sound and display i'th item in dataset.

    :param cls_index: Class name and index.
    """
    audio = myds.get_audiosignal(cls_index)
    AudioUtil.play(audio)
    ax.imshow(
        AudioUtil.melspectrogram(audio, Nmel=myds.nmel, Nft=myds.Nft),
        cmap="jet",
        origin="lower",
        aspect="auto",
    )

def getTrueIndex(idx):
    idxs = np.asarray(range(40), dtype=str)
    idxs.sort()

    for true_i,i in enumerate(idxs):
        if idx == int(i):
            return true_i
    

dataset = Dataset()
myds = Feature_vector_DS(dataset, Nft=512, nmel=20, duration=5000, shift_pct=0.0)

cl = "birds"
idx = 25
display(myds,[cl, getTrueIndex(idx)], py_ax)

#############################################################################################
#############################################################################################
#Sample melspec

for i in range(3):
    sample = np.load(f"/home/hugo/Documents/Etude/LELEC2101/LELEC210X-Groupe-G/classification/data/sample/{cl}{idx}_{i+1}_mic.npy")

    sample_axes[i].imshow(
        sample,
        cmap="jet",
        origin="lower",
        aspect="auto",
    )


#############################################################################################
#############################################################################################

plt.show()
