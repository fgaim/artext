[![LICENSE](https://img.shields.io/github/license/fgaim/artext.svg)](https://github.com/fgaim/artext/blob/master/LICENSE)
![GitHub issues](https://img.shields.io/github/issues/fgaim/artext.svg)
[![PyPI](https://img.shields.io/pypi/v/artext.svg)](https://pypi.org/project/artext/)
[![CircleCI](https://circleci.com/gh/fgaim/artext.svg?style=shield)](https://circleci.com/gh/fgaim/artext)

# Artext: Artificial Text Generation
## Probabilistic Noising of Natural Language

Artext is a work on injecting noise into text without affecting the core meaning for a human reader.
This kind of data can be useful for many NLP tasks, particulary in making models robust to noisy/erroneous input.


Note: Noising will generally increase the vocabulary size of the data sets, as it introduces word inflections and orthographic variations that may not have existed before. Therefore, it should be used with caution, especially for closed-vocabulary neural network models such as machine translation. In such scenarios, consider using subword based vocabulary (`BPE` for instance).

This is a work in progress, and the result of our experiments we will published soon.
Meanwhile, if you use `artext` in your research please cite this repository.


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

Generate sentence (`sent`) or document (`doc`) level noise samples for a text file as follows:
```
python -m artext -src source.txt -out output.txt -l sent -er 0.5 -n 10
```

[or] From source code using `inject.py` as follows:
```
python inject.py -src source.txt -out output.txt -l sent -er 0.5 -n 10
```

Use `-h` to see all options.


### Use as a library
```python
from artext import Artext

artxt = Artext()
artxt.samples = 5
artxt.error_rate = 0.25
sent = 'This is a sample sentence to be noised.'
noises = artxt.noise_sentence(sent)
print(noises)
```

## Examples


```
python example.py -er 0.5 -n 10
```

### Sentence Level Examples

**Input (clean sentence from Lang-8):**
```
So , I think if we have to go somewhere on foot , we must put on our hat .
```

**Human (error example from Lang-8):**

So , I think if we have to go somewhere on foot , we must put <del>on</del>  our hat .


**Output (artext):**
- So , I think if we have to <del>go</del> <ins>going</ins> somewhere on <del>foot</del> <ins>feet</ins> , we must put on our hat <del>.</del> <ins>?</ins>
- So <del>,</del> I <del>think</del> <ins>thinking</ins> if we have to go somewhere on foot , we must put on <ins>!</ins> our <del>hat</del> <ins>hats</ins> .
- So , I think if <del>we</del> have <ins>we</ins> to go somewhere on <del>foot</del> <ins>feet</ins> , we must put on our hat <del>.</del> <ins>;</ins>
- So <del>,</del> I think if we have to go somewhere on foot , we <del>must</del> put <ins>must</ins> on our <del>hat</del> <ins>hats</ins> .
- So , I think if we have to go somewhere on <del>foot</del> <ins>feet</ins> , we must <del>put</del> on <ins>put</ins> our hat .
- So <del>,</del> <ins>;</ins> I think if we <del>have</del> <ins>take</ins> to go somewhere on foot <del>,</del> we must put on our <del>hat</del> <ins>hats</ins> .
- So , I think if we have to go <del>somewhere</del> <ins>someplace</ins>  on foot , we must <del>put</del> <ins>putting</ins> on our <del>hat</del> <ins>hats</ins> .
- So , I think if we have to go somewhere on foot , we must put on our <del>hat .</del> <ins>chapeau ;</ins>
- So <del>,</del> I think if <del>we</del> have <ins>we</ins> to <del>go</del> somewhere <ins>go</ins> on foot , we must put on our hat .
- So , I <del>think</del> <ins>retrieve</ins> if we <del>have</del> <ins>having</ins> to <del>go</del> <ins>going</ins> somewhere on <del>foot ,</del> <ins>substructure</ins> we must <del>put</del> <ins>putting</ins> on our hat .


### Document Level Examples

**Input (clean sentence from Lang-8):**
```
This morning I found out that one of my favourite bands released a new album .
I already forgot about Rise Against and it is a great surprise for me, because I haven't listened to them for 2 years .
I hope this band did n't become worse, like many others big ones did , and I 'll enjoy listening to it .
Well , I just have to get it and check it out .
```

**Human (error example from Lang-8):** 

This morning I found out that one of my favourite <del>bands</del> <ins>band</ins> released <del>a</del> <ins>his</ins> new album . I already forgot about Rise Against <del>and</del> <ins>an</ins> it is a great surprise for me , because I <del>have</del> <ins>did</ins> n't <del>listened</del> <ins>return</ins> to them for 2 years . I hope this band did n't become worse <del>,</del> <ins>yet</ins> like many others big ones <del>did ,</del> and I 'll enjoy listening <del>to</del> it . Well , <del>I just have</del> <ins>there remains</ins> to get it and check it out .


**Output (artext):**
- This morning I found out that one of my <del>favourite</del> <ins>favored</ins> bands released a new album . I already forgot about <del>Rise Against</del> <ins>grow Agianst</ins> and it <del>is</del> <ins>are</ins> a great surprise for me , because I have n't <del>listened</del> <ins>listen</ins> to them for 2 years <del>.</del> I <del>hope</del> <ins>hoping</ins> this <del>band did</del> <ins>bands serve</ins> n't become worse , like many others big ones did , and I 'll enjoy <del>listening</del> to <ins>listening</ins> it . Well , I just <del>have</del> <ins>deliver</ins> to get it and check it out .
- This morning I found out that one of my favourite <del>bands released</del> <ins>band</ins> a <ins>released</ins> new album . I already <del>forgot</del> <ins>forget</ins> about Rise <del>Against</del> <ins>Aigniast</ins> and it is a great surprise for me , <del>because</del> I <ins>beceause</ins> have n't listened to them for 2 <del>years</del> <ins>geezerhood</ins> . I <del>hope</del> <ins>hoping</ins> this <del>band did</del> <ins>bands</ins> n't <del>become worse ,</del> <ins>did becoming wore</ins> like many <del>others</del> <ins>other</ins> big ones <del>did ,</del> <ins>didding ;</ins> and I 'll enjoy listening to it <del>. Well</del> <ins>eWll</ins> , I just have to get it and check it out .
- This morning I found out <del>that</del> one <ins>that</ins> of my favourite bands released a new <del>album</del> <ins>albums</ins> . I already <del>forgot</del> <ins>forgotting</ins> about Rise <del>Against</del> <ins>Aainst</ins> and it <del>is</del> <ins>be</ins> a great <del>surprise</del> <ins>surprisal</ins> for me , because I <del>have</del> <ins>having</ins> n't <del>listened</del> <ins>listneed</ins> to <del>them</del> <ins>tem</ins> for 2 years . I hope this band <del>did</del> <ins>do</ins> n't become <del>worse ,</del> like many others big ones <del>did</del> <ins>didding</ins> , and I 'll enjoy listening to it . Well , I just have to get it and <del>check</del> <ins>checking</ins> it out .
- This morning I found out that one of my favourite bands released a new album . I already forgot <del>about</del> <ins>abuot</ins> Rise <del>Against</del> <ins>Agaiinst</ins> and it is a great <del>surprise</del> <ins>srrpuise</ins> for me , because I have n't <del>listened</del> <ins>listening</ins> to them for 2 <del>years</del> <ins>year</ins> . I hope this band did n't become worse , like many <del>others</del> big <ins>other</ins> ones did , and I 'll <del>enjoy listening</del> <ins>enjoying litening</ins> to it . Well , I <del>just</del> <ins>scarce</ins> have to <del>get</del> <ins>getting</ins> it and <del>check it</del> <ins>checking</ins> out <ins>it</ins> .
- This <del>morning</del> <ins>mornings</ins> I <del>found</del> <ins>ground</ins> out <del>that</del> <ins>hTat</ins> one of my <del>favourite bands</del> <ins>favorite band</ins> released a new album . I already <del>forgot</del> <ins>forget</ins> about <del>Rise Against</del> <ins>arise Agsinat</ins> and it is a great <del>surprise</del> <ins>surprisal</ins> for me , <del>because</del> I <del>have</del> <ins>because</ins> n't <del>listened</del> <ins>have listen</ins> to them for 2 <del>years</del> <ins>year</ins> . I hope this band did n't become <del>worse</del> <ins>tough</ins> , like many <del>others</del> <ins>other</ins> big ones did , and I 'll <del>enjoy</del> listening <ins>enjoy</ins> to it <del>.</del> <ins>?</ins> Well , I <del>just</del> <ins>hardly</ins> have to get it and check it out .
- This morning I <del>found</del> <ins>fnuod</ins> out <del>that</del> <ins>htat</ins> one of my favourite bands <del>released</del> <ins>releasing</ins> a newalbum . I already forgot <del>about</del> <ins>abut</ins> Rise <del>Against</del> <ins>Aigainst</ins> and it is a great <del>surprise</del> <ins>surprises</ins> for me , <del>because</del> <ins>becuasae</ins> I have n't listened to them for 2 <del>years</del> <ins>year</ins> . I hope this band did n't <del>become</del> <ins>becoming</ins> worse , like many <del>others</del> <ins>other</ins> big <del>ones</del> <ins>one</ins> did <del>,</del> and I 'll <del>enjoy</del> listening <ins>enjoying</ins> to it . Well , I just <del>have to</del> <ins>having</ins> get <ins>to</ins> it and check it out <del>.</del> <ins>!</ins>
- This morning I found out that one of <del>my</del> favourite <ins>my</ins> bands <del>released</del> <ins>release</ins> a new album . I <del>already forgot</del> <ins>alraedyy forgotting</ins> about Rise <del>Against</del> <ins>Aagaianst</ins> and it <del>is</del> <ins>are</ins> a great <del>surprise</del> <ins>surprises</ins> for me <del>,</del> <ins>.</ins> because I have n't <del>listened</del> <ins>listen</ins> to them for 2 years . I hope this <del>band</del> did <ins>band</ins> n't become worse , like <del>many</del> others big ones did , and I 'll enjoy listening to it . Well , I just have to get it and check it out .
- This morning I <del>found</del> <ins>incur</ins> out that one of my <del>favourite</del> <ins>favored</ins> bands <del>released</del> <ins>releaseed</ins> a new <del>album</del> <ins>albums</ins> . I already forgot about Rise <del>Against</del> <ins>igAanst</ins> and it is a <del>great</del> <ins>grat</ins> surprisefor me , because I <del>have</del> <ins>having</ins> n't <del>listened</del> <ins>listen</ins> to them for 2 years <del>.</del> I hope this band did n't becomeworse , like many others big <del>ones did</del> <ins>one do</ins> , and I 'll <del>enjoy</del> <ins>enjoying</ins> listening to it . Well <del>,</del> <ins>:</ins> I just <del>have</del> <ins>having</ins> to <del>get</del> <ins>getting</ins> it and check it out .
- This morning I <del>found</del> <ins>founding</ins> out <del>that</del> <ins>hTat</ins> one of my favourite bands <del>released</del> <ins>releasing</ins> a <del>new</del> <ins>newfangled</ins> album . I already <del>forgot</del> <ins>block</ins> about Rise <del>Against</del> <ins>Aganst</ins> and it is a great surprise for me , <del>because</del> <ins>becuasee</ins> I have n't listened to them for 2 years . I hope <del>this</del> <ins>tthis</ins> band did n't <del>become</del> <ins>becoming</ins> worse <del>,</del> <ins>:</ins> like many others big ones did , and I 'll enjoy listening to it . Well , I just <del>have</del> <ins>having</ins> to get it and check it out . <ins>.</ins>
- This morning <del>I</del> found <ins>I</ins> out that one of my favourite <del>bands released</del> <ins>band releasing</ins> a new album . I already forgot about <del>Rise</del> <ins>Rising</ins> Against and it <del>is</del> a <del>great</del> <ins>is Greeat</ins> surprise for me , because I have n't listened to them for 2 years . I <del>hope</del> <ins>desire</ins> this band did n't become worse , like many others big ones <del>did</del> <ins>didding</ins> , and I 'll <del>enjoy</del> <ins>enjoying</ins> listening to it . Well <del>,</del> <ins>?</ins> I just have to get it and check it out .
