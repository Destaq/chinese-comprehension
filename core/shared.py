import re

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
        re.sub("\s+", "\n", target_text.read()).split("\n")
    )  # remove whitespace
    target_text_content = "".join(
        re.sub("[a-zA-Z0-9]", "\n", target_text_content).split("\n")
    )  # remove english characters and numbers
    punctuations = (
        "！？｡。＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃《》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏.?;﹔|.-·-*─"
    )
    target_text_content = "".join(
        re.sub(r"[%s]+" % punctuations, "", target_text_content).split("\n")
    )  # remove punctuations

    return target_text_content

def remove_words(word_list: list, exclude_words: list):
    if len(exclude_words):
        for exclude in exclude_words:
            if exclude in word_list:
                print(exclude)
                del word_list[exclude]

    return word_list

def round_to_nearest_50(x, base=50):
    return base * round(x/base)