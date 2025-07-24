## 示例：功能完整的小脚本

下面是一份完整的、用于演示 Tokenizer 原理的 Python 脚本，包含 `split_and_clean`、`encode`、`decode` 三个核心函数，放在一起更直观：

```python
import re
from typing import List

# 预编译正则，用于后续分词
_token_pattern = re.compile(r'([,.:;?_!"()\']|--|\s)')

def split_and_clean(text: str) -> List[str]:
    """
    步骤1：按照标点 & 空白拆分  
    步骤2：去除空字符串  
    """
    raw = _token_pattern.split(text)
    return [tok for tok in raw if tok.strip()]

def encode(text: str, vocab: dict) -> List[int]:
    """
    把文本转换为 ID 列表，遇到 OOV 用 <unk> 并打印警告
    """
    tokens = split_and_clean(text)
    ids: List[int] = []
    for tok in tokens:
        if tok in vocab:
            ids.append(vocab[tok])
        else:
            print(f"Warning: 未知 token ‘{tok}’，使用 <unk>")  
            ids.append(vocab.get("<unk>", 0))
    return ids

def decode(ids: List[int], inv_vocab: dict) -> str:
    """
    把 ID 列表还原为字符串，并去掉标点前多余空格
    """
    words = [inv_vocab.get(i, "<unk>") for i in ids]
    text = " ".join(words)
    text = re.sub(r'\s+([,.:;?_!"()\'])', r'\1', text)
    return text

# 演示
vocab = {"你好":1, "，":2, "world":3, "!":4, "<unk>":0}
inv_vocab = {i:s for s,i in vocab.items()}
text = "你好，LLM!"
print(split_and_clean(text))
print(encode(text, vocab))
print(decode([1,2,0,4], inv_vocab))
