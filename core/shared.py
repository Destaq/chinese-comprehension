import re, os
import pdfminer.high_level

def load_word_list_from_file(file: str):
    try:
        word_list = open(file, "r")  # filename of your known words here
    except KeyError as ke:
        raise ke

    words = set(
        re.sub("\s+", "\n", word_list.read()).split("\n")
    )  # splitting to remove accidental whitespace
    if "" in words:
        words.remove("")
    word_list.close()

    return words

def text_clean_up(target_text):
    target_text_content = "".join(
        re.sub("\s+", "\n", target_text).split("\n")
    )  # remove whitespace
    return target_text_content

def remove_punctuations(word_list: list):
    punctuations = ["！", "？", "。", "，"]
    for punctuation in punctuations:
        if punctuation in word_list:
            word_list = [v for v in word_list if v != punctuation]

    return word_list

def remove_exclusions(word_list: list, additional_exclusions: list):
    punctuations = (
        "！？｡。＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃《》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏.?;﹔|.-·-*─"
    )
    exclusions = [char for char in punctuations]
    exclusions.extend(additional_exclusions)
    word_list = list(filter(lambda x: x not in exclusions and not re.match(r'[a-zA-Z0-9]+', x), word_list))

    return word_list

def round_to_nearest_50(x, base=50):
    return base * round(x/base)

def text_setup(file):
    _, file_extension = os.path.splitext(file)
    if file_extension == ".pdf":
        target_text = pdfminer.high_level.extract_text(file)
    else:  # already in txt format
        try:
            target_text = open(file, "r")  # filename of your target text here
            target_text = target_text.read()
        except KeyError as ke:
            raise ke

    return target_text
