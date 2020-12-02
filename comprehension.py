import re, jieba, argparse
from collections import Counter
from re import compile as _Re
import core.shared as shared

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

    target_text_content = shared.text_clean_up(target_text)

    character_word_text = ""
    if mode == "smart":
        character_word_text = "Words"
        target_text_content = list(jieba.cut(target_text_content))  # split using jieba
    elif mode == "simple":
        character_word_text = "Characters"
        target_text_content = split_unicode_chrs(target_text_content)
        known_words = set(
            "".join([e for e in known_words])
        )  # convert known_words to chr_by_chr too
    else:
        raise KeyError("mode provided invalid")

    counted_target = Counter(target_text_content)
    target_length = len(target_text_content)

    total_unique_words = len(counted_target)
    counter = 0
    crosstext_count = 0
    unknown_words = []
    unknown_word_counter = 0

    for hanzi, count in counted_target.items():
        counter += 1
        print(f"-- {counter/total_unique_words * 100:.2f}% complete --", end="\r")
        if hanzi in known_words:
            crosstext_count += count
        elif outputfile is not None:
            unknown_word_counter += 1
            unknown_words.append((hanzi, count))

    unknown_words.sort(key=sort_by_count, reverse=True)
    if outputfile is not None:
        try:
            with open(outputfile, "w+") as file:
                for ele, count in unknown_words:
                    file.write(ele + " : " + str(count) + "\n")
        except KeyError as ke:
            return ke
            
        return (
            "\n\033[92mTotal Unique " + f"{character_word_text}" + ": \033[0m"
            + f"{total_unique_words}"
            +"\n\033[92mComprehension: \033[0m"
            + f"{crosstext_count/target_length * 100:.3f}%"
            + "\n\033[92mUnique Unknown " + f"{character_word_text}" + ": \033[0m"
            + f"{unknown_word_counter}"
        )
    else:
        return (
            "\n\033[92mTotal Unique " + f"{character_word_text}" + ": \033[0m"
            + f"{total_unique_words}"
            "\n\033[92mComprehension: \033[0m"
            + f"{crosstext_count/target_length * 100:.3f}%"
        )

def sort_by_count(e):
  return e[1]

if __name__ == "__main__":
    print(comprehension_checker(args.known, args.target, args.mode, args.unknown))
