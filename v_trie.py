from typing import List, Iterable, Generator
import itertools
import os.path
import re


class VietTrie:
  def __init__(self) -> None:
    self.next = {}
    self.is_word = False


  # this function is created for efficiency purposes
  # Used for efficient sliding window approach to extract all words in a sentence

  def trail_depth(self, word_gen: Generator[str, None, None]) -> int:
    depth = 0
    max_depth = depth
    tmp = self
    for token in word_gen:
      if token not in tmp.next:
        return max_depth
      tmp = tmp.next[token]
      depth += 1
      max_depth = depth if tmp.is_word else max_depth

    return max_depth

  def extract_words(self, original: str) -> List[str]:
    sentences = [sentence for sentence in re.split('[!.?,]+', original)]
    words = []
    for sentence in sentences:
      tokens = [token for token in sentence.split(" ") if token != ""]
      if not tokens:
        continue
        
      i = 0
      # construct a sliding window iterator every iteration
      while i < len(tokens):
        # skip names and title
        tmp = i
        while tmp < len(tokens) and tokens[tmp][0].isupper():
          tmp += 1
        if tmp != i:
          words.append(" ".join(tokens[i:tmp]))
        i = tmp
        if i == len(tokens):
          break

        # extract words from dictionary
        word_gen = itertools.islice(tokens , i, len(tokens)) # sliding window iterator
        depth = max(1, self.trail_depth(word_gen))
        words.append(" ".join(tokens[i:i+depth]))
        i += depth

    return words


  def has_word(self, word: str) -> bool:
    tokens = word.split(" ")
    tmp = self
    for token in tokens:
      if token not in tmp.next:
        return False
      tmp = tmp.next[token]

    return tmp.is_word


  def add_word(self, word: str) -> None:
    tokens = word.lower().split(" ")
    tmp = self
    for token in tokens:
      if token not in tmp.next:
        tmp.next[token] = self.__class__() # a hack to make VietTrie singleton :)
      tmp = tmp.next[token]
    tmp.is_word = True

# Load words from words.txt
words = []
file_path = os.path.join(os.path.dirname(__file__) if "__file__" in globals() else os.getcwd(), "words.txt")

try:
    with open(file_path, "r", encoding="utf-8") as f:
        words = f.read().strip().split("\n")
except FileNotFoundError:
    print(f"Warning: {file_path} not found. Trie will be empty.")

# innitiate trie
v_trie = VietTrie()

for word in words:
  v_trie.add_word(word)



if __name__ == "__main__":
  print(f"VietTrie.has_word(đàn bà) --> {v_trie.has_word('đàn bà')}")
  print(f"VietTrie.has_word(đàn ông) --> {v_trie.has_word('đàn ông')}")
  print(f"VietTrie.has_word(english) --> {v_trie.has_word('english')}")
  print(f"VietTrie.has_word(việt nam) --> {v_trie.has_word('việt nam')}")
  print(f"Extract words from this sentence: thiên nhiên Việt Nam rất hùng vĩ -> {v_trie.extract_words('thiên nhiên Việt Nam rất hùng vĩ')}")
  print(f"Extract words from this sentence: tiếng đàn piano thăng trầm du dương -> {v_trie.extract_words('tiếng đàn piano thăng trầm du dương')}")
  print(f"Extract words from this sentence: chạy chậm ì à ì ạch -> {v_trie.extract_words('chạy chậm ì à ì ạch')}")
  print(f"Extract words from this sentence: xin chào Việt Nam -> {v_trie.extract_words('xin chào Việt Nam')}")
  print(f"Extract words from this sentence: tôi thích đi du lịch châu Âu -> {v_trie.extract_words('tôi thích đi du lịch châu Âu')}")