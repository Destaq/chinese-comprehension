import re, os
import unicodedata
import pdfminer.high_level
from re import compile as _Re

def load_word_list_from_file(file: str):
    try:
        word_list = open(file, "r", encoding="utf8")  # filename of your known words here
    except KeyError as ke:
        raise ke

    words = set(
        re.sub(r"\s+", "\n", word_list.read()).split("\n")
    )  # splitting to remove accidental whitespace
    if "" in words:
        words.remove("")
    word_list.close()

    finalized_words = words.copy()

    # assume learner knows characters used in every word they know
    # this is to make parsing words such as 慢慢的 which are not
    # on the HSK be "recognized" by the program.
    for word in words:
        for single_hanzi in [char for char in word]:
            finalized_words.add(single_hanzi)

    return finalized_words

def text_clean_up(target_text):
    target_text_content = "".join(
        re.sub(r"\s+", "\n", target_text).split("\n")
    )  # remove whitespace

    # remove diacritics
    normalized = unicodedata.normalize("NFKD", target_text_content)
    result = "".join(c for c in normalized if unicodedata.category(c) != "Mn")
    return result

def remove_exclusions(word_list: list, additional_exclusions: list, do_punctuations=False):
    punctuations = (
        ",.:()!@[]+/\\！?？｡。＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃《》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏.?;﹔|.-·-*─\''\""
    )  # NOTE: need to include English punctuation due to PDF reader
    # NOTE: punctuations are now disabled by default as that is the industry standard

    if do_punctuations:
        exclusions = [char for char in punctuations]
        word_list = [word for word in word_list if word not in exclusions]

    word_list = list(filter(lambda x: x not in additional_exclusions and not re.match(r'[a-zA-Z0-9]+', x), word_list))

    return word_list

def round_to_nearest_50(x, base=50):
    return base * round(x/base)

def text_setup(file):
    _, file_extension = os.path.splitext(file)
    if file_extension == ".pdf":
        target_text = pdfminer.high_level.extract_text(file)
    else:  # already in txt format
        try:
            target_text = open(file, "r", encoding="utf8")  # filename of your target text here
            target_text = target_text.read()
        except KeyError as ke:
            raise ke

    return target_text


_unicode_chr_splitter = _Re("(?s)((?:[\ud800-\udbff][\udc00-\udfff])|.)").split

def split_unicode_chrs(text):
    """
    Split a Chinese text character by character.

    Courtesy of `flow` on StackOverflow: https://stackoverflow.com/a/3798790/12876940
    """
    return [chr for chr in _unicode_chr_splitter(text) if chr]
