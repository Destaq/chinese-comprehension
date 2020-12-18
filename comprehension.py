import re, argparse
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
parser.add_argument(
    "-e",
    "--exclude",
    required=False,
    help="Path to .txt file with newline-separated words to exclude (e.g. proper nouns)",
)

args = parser.parse_args()

_unicode_chr_splitter = _Re("(?s)((?:[\ud800-\udbff][\udc00-\udfff])|.)").split


def split_unicode_chrs(text):
    """
    Split a Chinese text character by character.

    Curtesy of `flow` on StackOverflow: https://stackoverflow.com/a/3798790/12876940
    """
    return [chr for chr in _unicode_chr_splitter(text) if chr]


def comprehension_checker(
    knownfile: str, targetfile: str, mode: str, outputfile: str, excludefile: str,
) -> str:
    known_words = shared.load_word_list_from_file(knownfile)

    exclude_words = []
    if excludefile != None:
        exclude_words = shared.load_word_list_from_file(excludefile)

    # access text in .txt format
    try:
        target_text = open(targetfile, "r")  # filename of your target text here
    except KeyError as ke:
        raise ke

    result_text = ""
    if mode == "smart":
        result_text = "Words"
        comprehension_result = smart_analysis(target_text.read(), known_words, exclude_words)
    elif mode == "simple":
        result_text = "Characters"
        comprehension_result = simple_analysis(target_text.read(), known_words, exclude_words)
    else:
        raise KeyError("mode provided invalid")

    if outputfile is not None:
        try:
            with open(outputfile, "w+") as file:
                for ele, count in comprehension_result["unknowns"]:
                    file.write(ele + " : " + str(count) + "\n")
        except KeyError as ke:
            return ke

    target_length = comprehension_result["target_length"]
    total_unique = comprehension_result["total_unique"]
    compredension_count = comprehension_result["compredension_count"]
    unknown_count = len(comprehension_result["unknowns"])
    return (
        "\n\033[92mTotal Unique " + f"{result_text}" + ": \033[0m"
        + f"{total_unique}"
        +"\n\033[92mComprehension: \033[0m"
        + f"{compredension_count/target_length * 100:.3f}%"
        + "\n\033[92mUnique Unknown " + f"{result_text}" + ": \033[0m"
        + f"{unknown_count}"
    )

def simple_analysis(target_text, known_words, excluded_characters):
    known_characters = set(
        "".join([e for e in known_words])
    )  # convert known_words to chr_by_chr too

    target_text_content = split_unicode_chrs(target_text)
    counted_target = Counter(target_text_content)
    crosstext_count = 0
    unknown = []
    for character, count in counted_target.items():
        if shared.is_excluded(character, excluded_characters) == True:
            continue

        if character in known_characters:
            crosstext_count += count
        else:
            unknown.append((character, count))

    unknown.sort(key=sort_by_count, reverse=True)
    return {
        "target_length": len(target_text_content),
        "total_unique": len(counted_target.items()),
        "compredension_count": crosstext_count, 
        "unknowns": unknown
    }


def smart_analysis(target_text, known_words, excluded_words):
    known_characters = set(
        "".join([e for e in known_words])
    )  # convert known_words to chr_by_chr too

    target_word_and_type = shared.text_segmentation(target_text)    
    counted_target = Counter(target_word_and_type)
    target_length = 0
    total_unique_words = 0
    crosstext_count = 0
    unknown_words = []
    print("Analyzing target text against known words...", end="\r")
    for word_and_type, count in counted_target.items():
        word = word_and_type[0]
        word_type = word_and_type[1]

        if word_type == "u": # exclude all particles (的,了) 
            continue

        if word_type == "w": # exclude all punctuation 
            continue

        if word_type == "xc": # exclude other function words, usually used for sounds
            continue 

        if shared.is_excluded(word, excluded_words) == True:
            continue

        target_length += count
        total_unique_words += 1
        if (word_type == "m" or word_type == "r") and shared.know_all_characters(word, known_characters) == True:
            crosstext_count += count
        elif word in known_words:
            crosstext_count += count
        else:
            unknown_words.append((word, count))
    print("Analyzing target text against known words... \033[94mdone\033[0m\n")

    unknown_words.sort(key=sort_by_count, reverse=True)
    return {
        "target_length": target_length,
        "total_unique": total_unique_words,
        "compredension_count": crosstext_count, 
        "unknowns": unknown_words
    }

def sort_by_count(e):
  return e[1]

if __name__ == "__main__":
    print(comprehension_checker(args.known, args.target, args.mode, args.unknown, args.exclude))

