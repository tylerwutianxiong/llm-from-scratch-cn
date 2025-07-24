# 第一章：Tokenizer 原理

本章示例采用「代码块 → 解释段落」的紧凑格式，便于初学者逐行理解核心逻辑。所有解释与示例紧跟在对应代码之后，并附加练习与扩展提示。

---

```python
# Step 1: 正则分词并清洗空白／空字符串
def split_and_clean(text: str) -> List[str]:
    # 预编译正则匹配：标点、双连字符、任意空白
    _token_pattern = re.compile(r'([,.:;?_!"()\']|--|\s)')
    raw_tokens = _token_pattern.split(text)
    # 只保留非空白、非空字符串的 token
    return [tok for tok in raw_tokens if tok.strip()]
```

> **解释 Step 1：**
>
> * `re.compile` 预编译正则，避免每次分词时重复编译，提高性能；
> * 模式 `([,.:;?_!"()' ]|--|\s)` 捕获逗号、句号、分号、问号、感叹号、双/单引号、圆括号、双连字符，以及所有空白；
> * `re.split` 在匹配到分隔符时进行切分，且保留分隔符自身作为 token；
> * `tok.strip()` 去除纯空白与空字符串，确保最终 token 列表只包含有意义的单元；
> * 当输入包含连续多个分隔符或多余空白时，`raw_tokens` 可能包含空项或重复分隔符，通过过滤一次性处理；
> * 示例对比：
>
>   ```python
>   raw_tokens = _token_pattern.split("Hello,  world!")  
>   # ['Hello', ',', ' ', '', 'world', '!']  
>   tokens = [tok for tok in raw_tokens if tok.strip()]  
>   # ['Hello', ',', 'world', '!']
>   ```
> * 优点：方法简单直观，易于扩展正则以支持更多符号；
> * 缺点：纯正则对复杂 Unicode 标点、emoji、合字支持有限；
> * **练习**：尝试加入中文书名号（《》）、破折号（—）或 emoji 类别，观察分词结果；

```python
# Step 2: 文本编码为 ID 列表，OOV 映射到 <unk>
def encode(text: str, vocab: Dict[str,int]) -> List[int]:
    tokens = split_and_clean(text)
    ids = []
    for tok in tokens:
        if tok in vocab:
            ids.append(vocab[tok])
        else:
            print(f"Warning: 未知 token ‘{tok}’，使用 <unk>")
            ids.append(vocab.get("<unk>", 0))
    return ids
```

> **解释 Step 2：**
>
> * 首先调用 `split_and_clean` 获取 token 列表；
> * 假设每个词就是一个 token，词典就像一本书，书中列出了所有已知的 token；
> * 当处理新文本时，如果遇到词典里没有的 token（例如 “ahahhaha”），就会出现 OOV（Out-Of-Vocabulary），如果直接查表，会抛出 `KeyError` 错误；
> * 本章中，我们在词典里额外添加一个特殊标记 `<unk>`（unknown）用来处理 OOV：遇到未知 token 时打印警告并统一映射为 `<unk>`，避免程序中断；
> * 缺点：不同的未知 token 都被映射为相同的 `<unk>`，无法区分；当未知词过多时，模型学习到的表示也不够细粒度；
> * 后续可使用 BPE（Byte-Pair Encoding）等子词编码方法，将未知的长 token 拆分为更小的 subword，并加入词典，以减少 `<unk>` 的使用；
> * 返回完整的 ID 列表，后续可直接输入到模型中训练或推理。

```python
# Step 3: 将 ID 列表还原为字符串，并去掉标点前多余空格
def decode(ids: List[int], inv_vocab: Dict[int,str]) -> str:
    words = [inv_vocab.get(i, "<unk>") for i in ids]
    text = " ".join(words)
    # 去掉空格 + 标点 的冗余
    text = re.sub(r'\s+([,.:;?_!"()\'])', r'\1', text)
    return text
```

> **解释 Step 3：**
>
> * 通过 `inv_vocab` 将每个整数 ID 恢复为对应 token；
> * 用空格拼接所有 token，得到中间字符串；
> * 正则 `\s+([,.:;?_!"()'])` 删除「空格+标点」的多余空格，使输出更符合自然语言规范；
> * 对于 BPE 等子词模式，可能需要根据子词前后缀自定义拼接策略；
> * 此阶段还可添加 Unicode 归一化（NFC/NFD）、大小写还原、合并多余空格等处理，提升可读性；
> * 若需要保留换行、空行或原始缩进，可先记录它们的位置，并在 decode 后重新插入，保证格式一致；
> * **练习**：为 `decode` 编写单元测试，验证 encode→decode 的可逆性，并尝试输出包含 emoji、中文符号的复杂文本；

---

以上三个步骤对应了 `SimpleTokenizerV1` 的核心功能：分词、编码、解码。文中示例与练习可帮助初学者在实践中深入理解分词器设计。
