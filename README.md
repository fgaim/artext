# Artext: Artificial Text Generation
### Probabilistic Noisig of Natural Languages

Artext is a work on intentionally injecting noise into text without affecting the text's core meaning to human reader.
This kind of data can be useful for many NLP tasks, particulary to make models robust to erroneous text. 
This is a work in progress, we will publish the results of our experiments soon.
Meanwhile, if you use `artext` in your research please cite this repository.

```
Note: Noising will generally increase the vocabulary size, as it introduces word inflections and spelling variations.
Therefore use with caution specially when the target models are neural networks.
```


## Setup

Developed and tested with `Python 3.6`.  

Using `pip`:
```
pip install artext
```

From source:
```
git clone https://github.com/fgaim/artext
cd artext
pip install -r requirements.txt
python setup.py install
```

Install required resources:
```
python -m spacy.load('en_core_web_sm')
python -m nltk.download('punckt')
```


## Usage

#### Use from commandline
Generate sentence or document level noisy samples for a text file follows.
Use `-h` to show all options.
```
python -m artext -src source.txt -out output.txt -l sent -er 0.5 -n 10
```

[or] From source code using `inject.py` as follows.
```
python inject.py -src source.txt -out output.txt -l sent -er 0.5 -n 10
```

#### Use programmatically
```
from artext import Artext

artxt = Artext()
artxt.samples = 5
sent = 'This is a sample sentence, to be noised.'
noises = artxt.noise_sentence(sent)
print(noises)
```

## Examples


```
python test.py -er 0.5 -n 20
```

#### Sentence Level Examples
```
Input:
This person tried to keep an eye on the president while doing his work.

Noises:
- This person tried to keep eye on the president while doing his work :
- This person tried to keep an eye on the president while doing his works.
- This people tried to keep an eye in the president while doing his works.
- This people tried to keep an eye with the president while doing his work.
- This person tried to keep an eye on president while doing his work.
- This person tried to keep an eye on a president while doing his work.
- This people tried to keep an eye on the president while doing his work.
- This person tried to keep an eyes on the president while doing his work.
- This person tried to keep an eye the on peeridsnt while doing his works.
- This person tried to keep the eye on an president while doing his work.
- This person tried to keep an eye on the president while doing his work!
- This person tried to keep an eye on the president while do his work.
- This person tried to keep an eye to the president while doing work his.
- This person tried to keeping an eye on the president while doing his work.
- These people tried to keep an eye in the president while doing his work :
- These person tried to keep an eye on presidents while doing his work.
- This person tried to keep an eye for the president while doing his work :
- This person tried to keep an eye on the president while doing his work.
- This people tried to keep eye on the president while doing his works.
- This person tried to keep an eye on the president while dioingg his work ,
- This person tried to keep an on eye the president while doing his works ,
- This person tried to keep an eye on the presidents while doing his work.
- This person tried to keep an eye on an president while doing his works.
- This person tried to keep an eye the on president while doing his work.
- This person tried to keep an eyes on the president while do his works.
```


#### Document Level Examples
```
Input:
I went to Iceland for vacation. The top of the mountain was very cold. Fortunately, I was wearing snowboard gear.

Noises:
- I went to Iceland by vacation. The top of the mountain were very cold! Fortunately, I was wearing snowboard gear.
- I went to Iceland for vaactaon. The tops of the mountain was very cold. Fortunately, I was wearing snowboard gear!
- I went to Iceland to vacation ; The top of the mountain was very cold Fortunately, I was wearing snobwoard gear.
- I wenting to Iceland on vacation. The tops of the mountain was very cold : Fortunately, I was wearing snwboad gear.
- I go to Iceland for vacation. The top of the mountain was very cold. Fortunately, I was wearing snowboards gear.
- I went to Iceland on vacation. The top of the mountain very was cold. Fortunately I was wearing snowboard gear.
- I went to Iceland at vacation? a top of the mountain was very cold. Fortunately: I be wearing snowboard gear.
- I went to Iceland for vacation , an top of the mountain was very cold. Fortunately, I was wearing snowboard gear ;
- I went to Iceland to vacation. The top of mountain was very cold Fortunately, I was wearing snowboard gear
- I went to Iceland for vacations ; The top of the mountain were very cold. Fortunately I was wearing snowboard gear
- I went with Iceland vacation. The top the moiunain was very cold : Fortunately; I was wearing snowboard gear.
- I wenting to Iceland to vacation. The top the of mountain was very cold. Fortunately, I was wearing snowboards gears.
- I went to Iceland for vacations : The top to the mountain very was cold Fortunately . I was wearing snowboard gear ;
- I went with Iceland for vacation. The tops from the mountain was very cold. Fortunately, I was wearing snowboards gear ;
- I went on Iceland for vacation. The tops of the mountain was very cold Fortunately? I was wearing snowboard gear.
- I went to Iceland vacation. the top of the mountain be very cold. Fortunately, I be wearing snowboard gear.
- I went to Iceland for vacation. The top the of mountain was very cold? Fortunately, I was wearing snowboard gears.
- I went to Iceland for vacation? The top to the mountain was very cold. Fortunately, I was wearing snowboard gears ;
- I went on Iceland for vacations , The top of the mountain being very cold. Fortunately I were wearing gear snowboard.
- I went to Iceland for vacation The top of the mountains was very cold. Fortunately, I was wearing snowboards gear :
- I go to Iceland for vacation The tops of the mountain was very cold! Fortunately I being wearing snowboard gear.
- I went Iceland for vacation. The top on the mountain was very cold. Fortunately . I was wearing snowboard gear!
- I went to Iceland with vacation The top from the mountain was very cold. Fortunately: I was wearing snowboard gear.
- I went to Iceland for vacations? The top of the mountains be very cold. Fortunately, I being wearing snowboard gear.
- I went to Iceland with vacation. The top with the mountain was very cold. Fortunately? I was wearing snowboard gear
```
