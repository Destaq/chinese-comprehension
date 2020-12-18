import re, argparse
from collections import Counter
from re import compile as _Re
import core.shared as shared

parser = argparse.ArgumentParser(
    description="Calculate unique words and character count of a text file - result is rounded to nearest 50"
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


def text_analyzer(
    targetfile: str, outputfile: str, excludefile: str,
) -> str:
    excluded_words = []
    if excludefile != None:
        excluded_words = shared.load_word_list_from_file(excludefile)

    # access text in .txt format
    try:
        target_text = open(targetfile, "r")  # filename of your target text here
        target_text_content = target_text.read()
    except KeyError as ke:
        raise ke

    target_word_and_type = shared.text_segmentation(target_text_content)    
    counted_target_word = Counter(target_word_and_type)

    total_unique_words = 0
    target_character_content = []
    for word_and_type, _ in counted_target_word.items():
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

        total_unique_words += 1

        characters = split_unicode_chrs(word)
        for character in characters:
            target_character_content.append(character)

    counted_target_character = Counter(target_character_content)
    total_unique_characters = len(counted_target_character)

    # if outputfile is not None:
    #     try:
    #         with open(outputfile, "w+") as file:
    #             file.write("=== All Unique Words ===\n")
    #             for ele, count in counted_target_word.most_common():
    #                 file.write(ele + " : " + str(count) + "\n")

    #             file.write("\n\n\n")
    #             file.write("=== All Unique Characters ===\n")
    #             for ele, count in counted_target_character.most_common():
    #                 file.write(ele + " : " + str(count) + "\n")
    #     except KeyError as ke:
    #         return ke
            
    return (
        "\n\033[92mTotal Unique Words: \033[0m"
        # + f"{shared.round_to_nearest_50(total_unique_words)}"
        + f"{total_unique_words}"
        "\n\033[92mTotal Unique Characters: \033[0m"
        # + f"{shared.round_to_nearest_50(total_unique_characters)}"
        + f"{total_unique_characters}"
    )

if __name__ == "__main__":
    print(text_analyzer(args.target, args.output, args.exclude))
