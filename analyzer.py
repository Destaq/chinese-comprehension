import argparse
import csv
from LAC import LAC
from tabulate import tabulate
from collections import Counter
from re import compile as _Re
import core.shared as shared

parser = argparse.ArgumentParser(
    description="Calculate unique words and character count of a text file - result is rounded to nearest 50"
)
parser.add_argument(
    "-k",
    "--known",
    required=False,
    help="Relative path to .txt file with newline-separated known words for *ing in output.",
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
    knownfile: str, targetfile: str, outputfile: str, excludefile: str
) -> str:
    known_words = shared.load_word_list_from_file(knownfile)

    exclude_words = []
    if excludefile != None:
        exclude_words = shared.load_word_list_from_file(excludefile)

    # access text in .txt format
    target_text = shared.text_setup(targetfile)

    target_text_content = shared.text_clean_up(target_text)
    target_text_content = ''.join(shared.remove_exclusions(target_text_content, exclude_words))
    target_word_content = list(lac.run(target_text_content))
    counted_target_word = Counter(shared.remove_exclusions(target_word_content, exclude_words))
    total_unique_words = len(counted_target_word)

    target_character_content = split_unicode_chrs(target_text_content)
    counted_target_character = Counter(shared.remove_exclusions(target_character_content, exclude_words))
    total_unique_characters = len(counted_target_character)

    # calculate hsk distribution
    hsk_distribution = {}
    with open('data/hsk_list.csv', mode='r') as csv_file:
        rows = csv.reader(csv_file, delimiter=",")
        for row in rows:
            if row[0] != "hanzi":  # first row
                hsk_distribution[row[0]] = {
                    "level": row[1],
                    "pinyin": row[2],
                    "meaning": row[3]
                }

    hsk_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, "-": 0}
    for word in target_word_content:
        try:
            hsk_counts[int(hsk_distribution[word]["level"])] += 1
        except:
            hsk_counts["-"] += 1

    total_value = 0
    all_values = sum(hsk_counts.values())
    for (key, value) in hsk_counts.items():
        total_value += value
        percentage = round((total_value / all_values) * 100, 3)
        value = [str(value), f" ({percentage}%)"]
        hsk_counts[key] = value

    if outputfile is not None:
        try:
            with open(outputfile, "w+") as file:
                file.write("=== All Unique Words ===\n")
                total_count = sum(counted_target_word.values())
                current_cumulative_count = 0
                for ele, count in counted_target_word.most_common():
                    current_cumulative_count += count
                    spaceup = 0
                    if ele not in known_words:
                        ele = "*" + str(ele)
                        spaceup = 1
                    file.write(ele + (8 - len(ele)) * " " + ": " + str(count) + (7 - len(str(count))) * " " + ": " + 8 * " " + str(round((current_cumulative_count * 100) / total_count, 3)) + "%\n")

                file.write("\n\n\n")
                file.write("=== All Unique Characters ===\n")
                total_count = sum(counted_target_character.values())
                current_cumulative_count = 0
                for ele, count in counted_target_character.most_common():
                    current_cumulative_count += count
                    spaceup = 0
                    if ele not in known_words:
                        ele = "*" + str(ele)
                        spaceup = 1
                    file.write(ele + (8 - len(ele)) * " " + ": " + str(count) + (7 - len(str(count))) * " " + ": " + 8 * " " + str(round((current_cumulative_count * 100) / total_count, 3)) + "%\n")
        except KeyError as ke:
            return ke

    hsk_output = []
    for (key, value) in hsk_counts.items():
        hsk_output.append([key, value[0], value[1]])
            
    return (
        "\n\033[92mTotal Words: \033[0m"
        + f"{shared.round_to_nearest_50(len(target_word_content))}"
        "\n\033[92mTotal Unique Words: \033[0m"
        + f"{shared.round_to_nearest_50(total_unique_words)}"
        "\n\033[92mTotal Characters: \033[0m"
        + f"{shared.round_to_nearest_50(len(target_text_content))}"
        "\n\033[92mTotal Unique Characters: \033[0m"
        + f"{shared.round_to_nearest_50(total_unique_characters)}"
        + "\n\n\033[90m=== HSK Breakdown ===\n\033[0m"
        + tabulate(hsk_output, headers=["Level", "Count", "Cumulative Frequency"])
    )

if __name__ == "__main__":
    print(text_analyzer(args.known, args.target, args.output, args.exclude))
