import re, jieba, argparse
from collections import Counter
from re import compile as _Re
import core.shared as shared

parser = argparse.ArgumentParser(
    description="Calculates percentage comprehension of a text file based on known words."
)
parser.add_argument(
    "-t",
    "--target",
    required=True,
    help="Relative path to .txt target file in Chinese.",
)
parser.add_argument(
    "-o",
    "--output",
    required=False,
    help="Path to output file with all words & characters words from text. Skip to not create an output file.",
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


def text_analyzer(
    targetfile: str, outputfile: str
) -> str:
    # access text in .txt format
    try:
        target_text = open(targetfile, "r")  # filename of your target text here
    except KeyError as ke:
        raise ke

    target_text_content = shared.text_clean_up(target_text)

    target_word_content = list(jieba.cut(target_text_content))  # split using jieba
    counted_target_word = Counter(target_word_content)
    total_unique_words = len(counted_target_word)

    target_character_content = split_unicode_chrs(target_text_content)
    counted_target_character = Counter(target_character_content)
    total_unique_characters = len(counted_target_character)

    if outputfile is not None:
        try:
            with open(outputfile, "w+") as file:
                file.write("=== All Unique Words ===\n")
                for ele, count in counted_target_word.most_common():
                    file.write(ele + " : " + str(count) + "\n")

                file.write("\n\n\n")
                file.write("=== All Unique Characters ===\n")
                for ele, count in counted_target_character.most_common():
                    file.write(ele + " : " + str(count) + "\n")
        except KeyError as ke:
            return ke
            
    return (
        "\n\033[92mTotal Unique Words: \033[0m"
        + f"{total_unique_words}"
        "\n\033[92mTotal Unique Characters: \033[0m"
        + f"{total_unique_characters}"
    )

def sort_by_count(e):
  return e[1]

if __name__ == "__main__":
    print(text_analyzer(args.target, args.output))