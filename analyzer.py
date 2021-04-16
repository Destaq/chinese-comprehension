import argparse
from LAC import LAC
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

print("Initializing parser...", end="\r")
lac = LAC(mode='seg')
print("Initializing parser... \033[94mdone\033[0m\n")


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
    exclude_words = []
    if excludefile != None:
        exclude_words = shared.load_word_list_from_file(excludefile)

    # access text in .txt format
    target_text = shared.text_setup(targetfile)

    target_text_content = shared.text_clean_up(target_text)
    target_word_content = list(lac.run(target_text_content))
    counted_target_word = Counter(shared.remove_exclusions(target_word_content, exclude_words))
    total_unique_words = len(counted_target_word)

    target_character_content = split_unicode_chrs(target_text_content)
    counted_target_character = Counter(shared.remove_exclusions(target_character_content, exclude_words))
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
        "\n\033[92mTotal Words: \033[0m"
        + f"{shared.round_to_nearest_50(len(target_word_content))}"
        "\n\033[92mTotal Unique Words: \033[0m"
        + f"{shared.round_to_nearest_50(total_unique_words)}"
        "\n\033[92mTotal Characters: \033[0m"
        + f"{shared.round_to_nearest_50(len(target_text_content))}"
        "\n\033[92mTotal Unique Characters: \033[0m"
        + f"{shared.round_to_nearest_50(total_unique_characters)}"
    )

if __name__ == "__main__":
    print(text_analyzer(args.target, args.output, args.exclude))
