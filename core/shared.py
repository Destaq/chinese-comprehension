import re

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