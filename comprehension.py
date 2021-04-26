import argparse
from LAC import LAC
from collections import Counter
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
    "-c",
    "--characters",
    required=False,
    default=False,
    action="store_true",
    help="SUGGESTED: Add this flag (just -c, no extra info) if you know all the characters in your wordlist. This is due to segmentation limitation. For ex. 慢慢的 is seen as one word, if this word is not in your wordlist, it will be unknown. By setting this flag (and having the characters 慢 and 的 in your wordlist (can be part of other words), 慢慢的 will be an 'understood' word."
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

print("Initializing parser...", end="\r")
lac = LAC(mode='seg')
print("Initializing parser... \033[94mdone\033[0m\n")


def comprehension_checker(
    knownfile: str, targetfile: str, mode: str, outputfile: str, excludefile: str,
) -> str:
    known_words = shared.load_word_list_from_file(knownfile)

    exclude_words = []
    if excludefile != None:
        exclude_words = shared.load_word_list_from_file(excludefile)


    # get text in correct format if in PDF format; TODO: more formats
    target_text = shared.text_setup(targetfile)

    target_text_content = shared.text_clean_up(target_text)

    character_word_text = ""
    if mode == "smart":
        character_word_text = "Words"
        target_text_content = list(lac.run(target_text_content))
    elif mode == "simple":
        character_word_text = "Characters"
        target_text_content = shared.split_unicode_chrs(target_text_content)
        known_words = set(
            "".join([e for e in known_words])
        )  # convert known_words to chr_by_chr too
    else:
        raise KeyError("mode provided invalid")

    target_text_content = shared.remove_exclusions(target_text_content, exclude_words)
    counted_target = Counter(target_text_content)
    target_length = len(target_text_content)

    total_unique_words = len(counted_target)
    counter = 0
    crosstext_count = 0  # counter of words that are understood
    unknown_words = []
    unknown_word_counter = 0

    for hanzi, count in counted_target.items():  # hanzzi represents a full word (unless simple mode)
        counter += 1
        print(f"-- {counter/total_unique_words * 100:.2f}% complete --", end="\r")
        if hanzi in known_words:
            crosstext_count += count
        elif set([char for char in hanzi]).issubset(set(known_words)) and args.characters:
            # ex. user knows 慢 的，慢慢的=对
            crosstext_count += count
        else:
            unknown_word_counter += 1
            if outputfile is not None:
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
        f"\n\033[92mWord Count: \033[0m{len(target_text_content)} (excluding 'exclusions')"
        + "\n\033[92mTotal Unique " + f"{character_word_text}" + ": \033[0m"
        + f"{total_unique_words}"
        +"\n\033[92mComprehension: \033[0m"
        + f"{crosstext_count/target_length * 100:.3f}%"
        + "\n\033[92mUnique Unknown " + f"{character_word_text}" + ": \033[0m"
        + f"{unknown_word_counter}"
    )

def sort_by_count(e):
  return e[1]

if __name__ == "__main__":
    print(comprehension_checker(args.known, args.target, args.mode, args.unknown, args.exclude))
