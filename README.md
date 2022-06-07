# chinese-comprehension
Analyze a Chinese text using your known words to gauge comprehension.

# Requirements
* Python 3.9 or below
* [LAC](https://github.com/baidu/lac/) - Chinese character segmentation library

![image](https://user-images.githubusercontent.com/61620873/118395391-88917000-b64a-11eb-8341-3fe3a12aec27.png)
![image](https://user-images.githubusercontent.com/61620873/118395410-a65ed500-b64a-11eb-8d3c-5546e65b9d5a.png)
![image](https://user-images.githubusercontent.com/61620873/118395468-db6b2780-b64a-11eb-8d29-cc745228ea18.png)


## Features
- Count unique words in text
  - Count unique unknown words in text
- Calculate comprehension of text based on your known words
  - Calculate the above splitting text and known vocab word-by-word or character-by-character
- Exclude words such as proper nouns to improve comprehension accuracy 
- Output unknown words into a file, sorted by frequency
- Add all words from book to known wordlist

## Installation
*Non-technical explanation for those not familiar with programming.*

Step 1: Download Python 3.9 or below. [Link](https://www.python.org/downloads/release/python-3912/)

**Note program will not run on Python 3.10 or above**

Step 2: Install Python 3.9. When installing you need to make sure you click the box on the bottom that says "install path variable".

Step 3: After Python is installed click on the search bar and type cmd to start command prompt. This will pull up a window that is "Command Prompt" (Windows).

If you are using Mac, simply open a terminal window by pressing cmd-space and then typing terminal and opening said app.

Step 4: Verify you have python installed by typing `python --version`, it should tell you that you have python 3.X.X installed. If the version says 2.X.X, try typing `python3 --version` instead, and use `python3 -m pip` instead of `pip` in future steps.

Step 5: Download the comprehension zip file [here](https://github.com/Destaq/chinese-comprehension) by clicking the green button and clicking download zip.

Step 6: Once the comprehension zip file is installed you can extract it to where you want it to be.

Step 7: Open the command prompt/terminal window and navigate to the folder you extracted the comprehension zip file to. [How to navigate in the terminal tutorial](https://tutorials.codebar.io/command-line/introduction/tutorial.html). You can also navigate by dragging the folder to the command prompt.

Step 8: Type in `pip install -r requirements.txt` in the commmand line once you navigate to the comprehension folder.

Step 9: You can now refer to the documentation on this page to use the tool!

Finally (technical), note that if you are using an **M1 Mac**, you will need to run everything via a virtual environment as this chip is not supported yet by LAC. This can be easily done with conda by following the following [steps](https://github.com/conda-forge/miniforge/issues/165#issuecomment-860233092).

## Usage
```
usage: comprehension.py [-h] -k KNOWN -t TARGET [-m MODE] [-u UNKNOWN]
                        [-e EXCLUDE]

Calculates percentage comprehension of a text file based on known words.

optional arguments:
  -h, --help            show this help message and exit
  -k KNOWN, --known KNOWN
                        Relative path to .txt file with newline-separated known words.
  -t TARGET, --target TARGET
                        Relative path to .txt target file in Chinese.
  -m MODE, --mode MODE  Mode for separating text and known vocab: 'smart' (default, word-by-word using jieba) 'simple' (character-by-character)
  -c, --characters      Add this flag (just -c, no extra info) if you know all the characters in your wordlist. This is due to segmentation limitation. For ex. 慢慢的 is seen as one word, if this word is not in your wordlist,
                        it will be unknown. By setting this flag (and having the characters 慢 and 的 in your wordlist (can be part of other words), 慢慢的 will be an 'understood' word.
  -u UNKNOWN, --unknown UNKNOWN
                        Path to output file with unknown words from text. Skip to not create an output file.
  -e EXCLUDE, --exclude EXCLUDE
                        Path to .txt file with newline-separated words to exclude (e.g. proper nouns)
```

The `--known` parameter takes the filename containing known words. These words represent all words the user knows for best accuracy. Methods for fetching these words:
- export from Anki
- export from Pleco
- take HSK test
- consult [HelloChinese word list](https://docs.google.com/spreadsheets/d/1PppWybtv_ch5QMqtWlU4kAm08uFuhYK-6HGVnGeT63Y/edit#gid=121546596)

The file should have words separated line-by-line:
```
是
你好
再见
有
五
...
```

The `--target` parameter takes the filename containing the target text. This should be normally formatted:
```
美猴王一見，倒身下拜，磕頭不計其數，口中只道：「師父，師父，我弟子志心
朝禮，志心朝禮。」祖師道：「你是那方人氏？且說個鄉貫、姓名明白，再拜。」
猴王道：「弟子乃東勝神洲傲來國花果山水簾洞人氏。」祖師喝令：「趕出去！
他本是個撒詐搗虛之徒，那裏
...
```

The `-c` or `--comprehension` flag allows you to mark words which would otherwise be unknown as known, as long as you know all of the characters that make it up. Due to the way the word segmenter words, many words that learners are likely to know are graded separately, and thus would not be present on the `known.txt` file.

For example, say a learner knows the word `开心` and the particle `地`. Logically, they would be expected to understand the word `开心地`, or happily. However, because this word is parsed *standalone*, unless it is explicitly on the wordlist, it would be viewed as unknown. This behavior can be bypassed by setting the `-c` flag, ex. `python3 comprehension.py -k "known.txt" -t "myfile.pdf" -c`. Keep in mind that this method is also not perfect, because independent words made up of known characters may have differing meanings (e.g. 头发 - learners may know 头 and 发 but not them in conjunction).

Quick side note: the `"` here are not required, but it's best to put them here anywhere. If your filename has a space in it (for example `my known.txt`), then that will obviously mess with the command line, so this would be reason to put speech marks around it. If you're not sure, just always put speech marks around the arguments.

It is advised to take comprehension using the `-c` flag with a grain of salt, based on the difficulty of the text the level is likely to be some percentage points lower. But it is still far more accurate then without the flag.

`--mode` allows you to switch between 'simple' and 'smart' mode, where the default is 'smart' - segmenting text word-by-word (ex. 你/有/什么/名字/？ for smart vs 你/有/什/么…… for simple.

`--unknown` allows you to create a file with all the unknown words in the text, in the format:
```
Hanzi : Count
Hanzi : Count
...
```

which is sorted by frequency. Ideal when preparing for a more difficult text or wanting to recap words. __This file has to be .txt. format__. Ex. `python3 comprehension.py -k "data/known.txt" -t "books/Earth_Vernes.pdf" -u "data/unknown_words.txt"`.

The `--exclude` parameter takes the filename containing words to exclude words. Exclude any proper nouns such as character names & company names to improve accuracy.

The file should have words separated line-by-line:
```
安琪
赵宁一
爱丽丝
麦当劳
...
```

### Example

*Code*: `python3 comprehension.py --known "known.txt" -t "samples/books/Great_Expectations.pdf" -u "output.txt"`
*Description*: Gathers known words from `known.txt`, and analyzes `samples/books/Great_Expectations.pdf` using the default word-by-word splitting. Unknown words are outputted to `output.txt`.

*Content of `output.txt`*
```
道 : 4621
行者 : 2575
來 : 1665
裏 : 1591
與 : 1498
又 : 1485
卻 : 1264
...
```

# Analyzer

## Usage
```
usage: analyzer.py [-h] -t TARGET [-o OUTPUT] [-e EXCLUDE] [-n NOWORDS]

Calculate unique words and character count of a text file - result is rounded
to nearest 50. Note that character counts may not line up with character counts
seen in official webnovel figures, as this tool does not count punctuation.

optional arguments:
  -h, --help            show this help message and exit
  -t TARGET, --target TARGET
                        Relative path to .txt or .pdf target file in Chinese.
  -o OUTPUT, --output OUTPUT
                        Path to output file with all words & characters words
                        from text. Skip to not create an output file.
  -e EXCLUDE, --exclude EXCLUDE
                        Path to .txt file with newline-separated words to
                        exclude (e.g. proper nouns)
  -n NOWORDS, --no-words NOWORDS
                        Setting this flag will mean that the tool does not segment words, so you will not have a calculating of # of words, # of unique words, and HSK breakdown. Can lead to a significant speedup, as segmentation takes approx. 1 minute per 1 million characters. Off by default. To set, simply add -n.
```

Finally, you can use the `--known` or `-k` argument linking to a file in your system that has newline-separated words that you know. By doing so, and also outputting a file, any words/characters that you don't know will have a star symbol (*) by them.

### Example

*Code*: `python3 analyzer.py -t "samples/books/journey_to_the_west.txt" -o "output.txt"`
*Description*: Analyzes `samples/books/journey_to_the_west.txt` using the word-by-word and character-by-character splitting. Outputs all characters and words to `output.txt`.

*Output*
```
Total Unique Words: 32226
Total Unique Characters: 3572
```

*Content of `output.txt`*
```
=== All Unique Words ===
的 : 18840
了 : 15791
昇 : 10683
周 : 9155
余皓 : 8995
我 : 7512
...

=== All Unique Characters ===
的 : 19664 (4.2%)
了 : 17135 (5.6%)
余 : 14223 ...
*皓 : 14103
一 : 12667
周 : 11641
昇 : 10756
不 : 10217
我 : 8723
```

Note the *. This will be put next to words that are not known if a knownfile is provided. Likewise, note the percentages. This is the cumulative frequency percentages of these texts.
Currently only possible if smart mode is selected.

# Vocab Adder
The `vocab_adder` file is extremely simple. It allows you to input a file and your known vocab list, and will append all unknown words in the file to your vocab list.

Example:
`python3 vocab_adder.py -t books/Earth_Vernes.pdf -k data/known.txt`

You can specify the mode (default is smart, which is segmentation) with the `-m` flag by typing `--mode simple`.

# FAQ

Q: How is punctuation counted?
A: As is the industry standard, punctuation (periods, commas, etc.) *are* included in total character count. However, they are not included in unique character count nor in any output files.
