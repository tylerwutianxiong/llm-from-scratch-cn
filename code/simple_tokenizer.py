import re
from typing import List

class SimpleTokenizerV1:
    def __init__(self, str_to_int: dict):
        # 预编译正则，用于后续分词
        self._token_pattern = re.compile(r'([,.:;?_!"()\']|--|\s)')
        self.str_to_int = str_to_int
        # 反向映射：ID -> token
        self.int_to_str = {i: s for s, i in str_to_int.items()}

    def split_and_clean(self, text: str) -> List[str]:
        """
        步骤1：按照标点 & 空白拆分  
        步骤2：去除空字符串  
        例子： "你好，world!" → ['你好', '，', 'world', '!']
        """
        raw_tokens = self._token_pattern.split(text)
        # 只保留非空 token
        return [tok for tok in raw_tokens if tok.strip()]

    def encode(self, text: str) -> List[int]:
        """
        将文本转换为 ID 列表，遇到 OOV（未登录词）打印 warning 并使用 <unk>
        """
        tokens = self.split_and_clean(text)
        ids: List[int] = []
        for tok in tokens:
            if tok in self.str_to_int:
                ids.append(self.str_to_int[tok])
            else:
                print(f"Warning: 未知 token ‘{tok}’，使用 <unk>")
                ids.append(self.str_to_int.get("<unk>"))
        return ids

    def decode(self, ids: List[int]) -> str:
        """
        将 ID 列表还原为字符串，并在标点前去掉多余空格
        """
        words = [self.int_to_str.get(i, "<unk>") for i in ids]
        text = " ".join(words)
        # 去掉标点前多余空格
        text = re.sub(r'\s+([,.:;?_!"()\'])', r'\1', text)
        return text
