V_word_search

Overview

V_word_search is a Vietnamese word extraction tool that uses a Trie data structure to efficiently find and extract Vietnamese words from sentences. The project scrapes a Vietnamese dictionary and builds a Trie for fast lookups.

Features

Web Scraping: Scrapes Vietnamese words from VDict and stores them in words.txt.

Trie Data Structure: Implements a Trie for efficient word search and extraction.

Word Extraction: Identifies and extracts valid Vietnamese words from input sentences.

Command-Line Interface: Provides a simple way to test the Trie’s functionality.

Example

v_trie.has_word('đẹp đẽ') --> True
v_trie.has_word('hello') --> False
Extract words from this sentence: tiếng đàn piano thăng trầm du dương -> ['tiếng', 'đàn', 'piano', 'thăng trầm', 'du dương']
