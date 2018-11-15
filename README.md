# Artext: Artificial Text Generation

[![LICENSE](https://img.shields.io/github/license/fgaim/artext.svg)](https://github.com/fgaim/artext/blob/master/LICENSE)
![GitHub issues](https://img.shields.io/github/issues/fgaim/artext.svg)
[![PyPI](https://img.shields.io/pypi/v/artext.svg)](https://pypi.org/project/artext/)
[![CircleCI](https://circleci.com/gh/fgaim/artext.svg?style=shield)](https://circleci.com/gh/fgaim/artext)


## Probabilistic Noising of Natural Language

Artext is a work on injecting noise into text without affecting the core meaning for a human reader.
This kind of data can be useful for many NLP tasks, particulary in making models robust to noisy/erroneous input.


This is a work in progress, and the result of our experiments we will published soon.
Meanwhile, if you use `artext` in your research please cite this repository.

> Note: Noising will generally increase the vocabulary size of the data sets, as it introduces word inflections and orthographic variations that may not have existed before. Therefore, use it with caution, especially for closed-vocabulary neural network models such as machine translation. Consider using subword based vocabulary (`BPE` for instance) in such scenarios.



## Setup

`artext`'s developed and tested with `Python 3.6` and can be installed in two ways:

1. Using `pip`:

```
 pip install artext
 ```

2. From source code:
```
git clone https://github.com/fgaim/artext
cd artext
pip install -r requirements.txt
python setup.py install
```

Get required resources:
```bash
python -m spacy download 'en_core_web_sm'
python -m nltk.downloader 'punkt'
python -m nltk.downloader 'wordnet'
```


## Usage

### Use from command-line

Generate sentence or document level noise samples for a text file as follows:
```
python -m artext -src source.txt -out output.txt -l sent -er 0.5 -n 10
```

[or] From source code using `inject.py` as follows.
```
python inject.py -src source.txt -out output.txt -l sent -er 0.5 -n 10
```

Use `-h` to see all options.


### Use as a library
```python
from artext import Artext

artxt = Artext()
artxt.samples = 5
artxt.error_overall = 0.25
sent = 'This is a sample sentence to be noised.'
noises = artxt.noise_sentence(sent)
print(noises)
```

## Examples


```
python example.py -er 0.5 -n 20
```

### Sentence Level Examples
```
Input:
This person tried to keep an eye on the president while doing his work.

Noises:
- This people hear to keep an eye on the presidents while coiffe his work :
- This pperson tried to keep an eye the on president wahiile doing his work.
- This person tried to keep an oculus on the presidents while doing his work :
- This person trying to keeping an eyes on the president while uedoig his works.
- This person tried to keep an eye on the presidents while doing his work
- This person to tried keeping an eye on the president while doing his employment.
- This rperson tried to keep an eye the on presidents while arrange his employment ,
- This person trying to keep an eyes on the presidents while doing his works
- This people trying to keep an eye on the president while doing his works?
- This person trying to keeping an eye on the presidnt while dooign his work.
- This people tried to keeping an eyes on the president while doing work his!
- This pperson try to keep an eye on the president while doing his works ;
- This person try to keep an eye on the president while do his works :
- This person tried to keeping an eye on the president while doing his works.
- This person tried to keep an eye on the presidents hwle doing his works.
- This people try to keeping an eye on the preident while set his work.
- This person tried to keep an eye on the president while doing his work
- This people to tried keep an eye on the president while dooing his works.
- This person rtied to keep an eye on the prexy while doing his work.
- This people trying to sustain an eyes on the chairperson while doing his work ;
```


### Document Level Examples
```
Input:
I went to Iceland for vacation. The top of the mountain was very cold. Fortunately, I was wearing snowboard gear.

Noises:
- I wenting to Iceland for vacation. The top of the mountains being very cold. Fortunately: I being wearing snowboards gear.
- I went to ncelaIud for vacations The tops of the mntain personify very cold Fortunately, I be outwear snnowboard gear?
- I went to Iceland for vacation! The top of the mountains constitute really cold : Fortunately! I were wear nsowbarod gears
- I get to Iceland for vacations. The top of the mountain being very cold? Fortunately, I being wearing snowboard gear
- I die to Iceeland for vacations. The top the of mauntoin was cold very Fortunately, I was wearing snowboard gears.
- I went to for Iceland vacation , The tops the of mouintain be cold very. Fortunately, I were wearing snowboard gear.
- I wenting to Iceland for vacation , The teetotum of the muuntain be very cold , fortunately; I being wearing gear snowboard!
- I expire to Icealnd for vacation. The tops of the slew was very cold Forunateyl, I were wearing snowboaar gear.
- I wenting to Ieland for vacations : The meridian the of mountains very were cold luckily I were wearing snowboards gears.
- I went to Iceland for vacations? The cover of the mountains were very inhuman. Fortunately, I being wear snowboard gears
- I went to Iceland for vacation The top of the mountain was really cold. Fortunately; I being wearing snowboards gear
- I went to Iceland for vacations. The top of the omunan were very. Fortunately, I being wearing snowboard gear ;
- I went to Iceland for vacations ; The top of the slew was very cold. Fortunately: I were weareing snowbboard gear?
- I went to Iceland for vacation. The elevation of the mouantain were very cold Forrtunately . I was wearing snowboard gear.
- I went to Iceland for vacation? The top of the mountains be very cold. fortunately I, was tire snowboard gears.
- I went to Iceland for vacation , The tops of the mountains was really cold. Fortunately, I being wearinaig snowboard gears!
- I go to Iceland for vacations : The top of the was flock very cold luckily, was I wearing snowboard gears.
- I become to Iceland for vacation! The tops of the mountains was very cold. Fortunately, I represent wearing snowboard gear
- I to depart Ieland for vacations ; The crest of the mountain were very frigid. luckily, I were iwwearig snowboard gear.
- I wenting to Icleand for holiday. The top the of mountains be rattling insensate. Fortunately; I being wearing snowboard gear.
```
