def max_word_count(filename: str) -> tuple[str, int]:
    freq = {}
    for piece in open(filename).read().lower().split():
        # 只考虑小写字母的单词
        word = ''.join(c for c in piece if c.isalpha())
        if word:  # 单词存在
            freq[word] = 1 + freq.get(word, 0)  # 有则 +1 无则初始化为 0

    max_word = ''
    max_count = 0
    for (w, c) in freq.items():  # (key, value) tuples represent (word, count)
        if c > max_count:
            max_word = w
            max_count = c

    return max_word, max_count


if __name__ == '__main__':
    file_path = "example.txt"
    max_word, max_count = max_word_count(filename=file_path)
    print('The most frequent word is: \'{}\''.format(max_word))
    print('Its number of occurrences is: {}'.format(max_count))
