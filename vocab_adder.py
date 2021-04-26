import argparse
import core.shared as shared
from collections import Counter
from LAC import LAC

parser = argparse.ArgumentParser(
    description="Add words from a file to your known vocab."
)
parser.add_argument("-t", "--target", required=True, help="Path to .txt or .pdf file of target text to add")
parser.add_argument("-k", "--known", required=True, help="Path to .txt file where vocabulary from the text will be dumped.")
parser.add_argument("-m", "--mode", default="smart", help="smart/simple (smart default) - whether to split text char-by-char (simple) or word-by-word (smart)")
args = parser.parse_args()

print("Initializing parser...", end="\r")
lac = LAC(mode='seg')
print("Initializing parser... \033[94mdone\033[0m\n")

def add_vocab(targetfile: str, knownfile: str, mode: str):
    target_text = shared.text_setup(targetfile)
    target_text_content = shared.text_clean_up(target_text)

    if mode == "smart":
        target_text_content = list(lac.run(target_text_content))
    else:
        target_text_content = shared.split_unicode_chrs(target_text_content)

    target_text_content = shared.remove_exclusions(target_text_content, [])

    # add to known wordlist if not in wordlist
    known_words_list = []
    with open(knownfile, "r+") as file:
        known_words_list = file.read().splitlines()
    
    with open(knownfile, "w+") as file:
        for word in known_words_list:
            file.write(word + "\n")

        for word in list(dict.fromkeys(target_text_content)):
            if word not in known_words_list:
                known_words_list.append(word)
                file.write(word + "\n")



if __name__ == "__main__":
    add_vocab(args.target, args.known, args.mode)
    print("Task completed.")
