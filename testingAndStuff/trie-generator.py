class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
    
    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word
    
    def starts_with(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True

# Create trie with similar and different words
trie = Trie()
words = [
    "cat", "cats", "category",  # similar words
    "dog", "dogs", "dogma",     # another similar set
    "car", "care", "career",    # another similar set
    "computer", "computation",  # technical words
    "mouse", "house", "spouse", # rhyming words
    "mice", "ice", "dice",      # another rhyming set
    "sport",
]

# Insert words
for word in words:
    trie.insert(word)

# Demonstration of searches
# print("Searching for 'cat':", trie.search("cat"))
# print("Searching for 'cats':", trie.search("cats"))
# print("Starts with 'ca':", trie.starts_with("ca"))
# print("Searching for 'car':", trie.search("car"))
# print("Starts with 'comp':", trie.starts_with("comp"))

def trie_to_mermaid(trie):
    from collections import deque
    node_queue = deque([(trie.root, 0, None, "")])
    visited = {trie.root: 0}
    mermaid_lines = ["graph TD"]

    while node_queue:
        node, node_id, parent_id, char = node_queue.popleft()
        if parent_id is not None:
            mermaid_lines.append(f"{parent_id}-->{node_id}({char})")
        for c, child in node.children.items():
            if child not in visited:
                visited[child] = len(visited)
                node_queue.append((child, visited[child], node_id, c))

    return "\n".join(mermaid_lines)

with open("testingAndStuff/trie.md", "w") as f:
    f.write('```mermaid\n' + 
        trie_to_mermaid(trie) + '\n```')
