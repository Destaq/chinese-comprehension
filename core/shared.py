import re
from LAC import LAC

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

def is_excluded(word, additional_exclusions: list):
    punctuations = (
        "！？｡。＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃《》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏.?;﹔|.-·-*─"
    )
    exclusions = [char for char in punctuations]
    exclusions.extend(additional_exclusions)
    if word not in exclusions and not re.match(r'[a-zA-Z0-9]+', word):
        return False
    return True

def round_to_nearest_50(x, base=50):
    return base * round(x/base)

def know_all_characters(word: str, known_characters: list):
    by_character = set(
        "".join([e for e in word])
    )  # spilt word by character
    for character in by_character:
        if character not in known_characters:
            return False
    return True

def text_segmentation(target_text: str):
    print("Initializing parser...", end="\r")
    lac = LAC(mode='LAC')
    print("Initializing parser... \033[94mdone\033[0m\n")

    print("Segmenting target text...", end="\r")
    splits = list(re.sub("\s+", "\n", target_text).split("\n"))
    result = lac.run(splits)

    target_word_and_type = []
    for line in result:
        combined = list(zip(line[0], line[1]))
        target_word_and_type = target_word_and_type + combined
    print("Segmenting target text... \033[94mdone\033[0m\n")

    return target_word_and_type