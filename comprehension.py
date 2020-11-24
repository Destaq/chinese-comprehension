import re, jieba, argparse
from collections import Counter
from re import compile as _Re

parser = argparse.ArgumentParser(
    description="Calculates percentage comprehension of a text file based on known words."
)
parser.add_argument(
    "-k",
    "--known",
    required=True,
    help="Relative path to .txt file with newline-separated known words.",
)
parser.add_argument(
    "-t",
    "--target",
    required=True,
    help="Relative path to .txt target file in Chinese.",
)
parser.add_argument(
    "-m",
    "--mode",
    default="smart",
    help="Mode for separating text and known vocab: 'smart' (default, word-by-word using jieba) 'simple' (character-by-character)",
)
parser.add_argument(
    "-u",
    "--unknown",
    required=False,
    help="Path to output file with unknown words from text. Skip to not create an output file.",
)

args = parser.parse_args()

# disable jieba messages
jieba.setLogLevel(20)
print("Initializing dictionary...", end="\r")
jieba.initialize()
print("Initializing dictionary... \033[94mdone\033[0m\n")


_unicode_chr_splitter = _Re("(?s)((?:[\ud800-\udbff][\udc00-\udfff])|.)").split


def split_unicode_chrs(text):
    """
    Split a Chinese text character by character.

    Curtesy of `flow` on StackOverflow: https://stackoverflow.com/a/3798790/12876940
    """
    return [chr for chr in _unicode_chr_splitter(text) if chr]


def comprehension_checker(
    knownfile: str, targetfile: str, mode: str, outputfile: str
) -> str:
    try:
        wordlist = open(knownfile, "r")  # filename of your known words here
    except KeyError as ke:
        raise ke

    known_words = set(
        re.sub("\s+", "\n", wordlist.read()).split("\n")
    )  # splitting to remove accidental whitespace
    if "" in known_words:
        known_words.remove("")
    wordlist.close()

    # access text in .txt format
    try:
        target_text = open(targetfile, "r")  # filename of your target text here
    except KeyError as ke:
        raise ke

    target_text_content = "".join(
        re.sub("\s+", "\n", target_text.read()).split("\n")
    )  # remove whitespace
    target_text_content = "".join(
        re.sub("[a-zA-Z0-9]", "\n", target_text_content).split("\n")
    )  # remove english characters and numbers
    punctuations = (
        "！？｡。＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃《》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏.?;﹔"
    )
    target_text_content = "".join(
        re.sub(r"[%s]+" % punctuations, "", target_text_content).split("\n")
    )  # remove punctuations

    if mode == "smart":
        target_text_content = list(jieba.cut(target_text_content))  # split using jieba
    elif mode == "simple":
        target_text_content = split_unicode_chrs(target_text_content)
        known_words = set(
            "".join([e for e in known_words])
        )  # convert known_words to chr_by_chr too
    else:
        raise KeyError("mode provided invalid")

    counted_target = Counter(target_text_content)
    target_length = len(target_text_content)

    counter = 0
    crosstext_count = 0
    unknown_words = []
    unknown_word_counter = 0

    for hanzi, count in counted_target.items():
        counter += 1
        print(f"-- {counter/len(counted_target) * 100:.2f}% complete --", end="\r")
        if hanzi in known_words:
            crosstext_count += count
        elif outputfile is not None:
            unknown_word_counter += 1
            unknown_words.append(hanzi)

    if outputfile is not None:
        try:
            with open(outputfile, "w+") as file:
                for ele in unknown_words:
                    file.write(ele + "\n")
        except KeyError as ke:
            return ke
            
        return (
            "\n\033[92mComprehension: \033[0m"
            + f"{crosstext_count/target_length * 100:.3f}%"
            + "\n\033[92mUnique Unknown Words: \033[0m"
            + f"{unknown_word_counter}"
        )
    else:
        return (
            "\n\033[92mComprehension: \033[0m"
            + f"{crosstext_count/target_length * 100:.3f}%"
        )


if __name__ == "__main__":
    print(comprehension_checker(args.known, args.target, args.mode, args.unknown))
