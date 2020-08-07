
from Node import HuffNode


if __name__ == "__main__":

    # %%
    from HuffmanCoding import HuffmanCoding
    
    Huff = HuffmanCoding()
    freqMap = {}

    # %%
    with open('alice.txt', 'r') as f:
        text = f.read()
        freqMap = Huff.makeFreqMap(text)

    # %%
    heap = Huff.makeHeap(freqMap)
    Huff.mergeNodes(heap)
    
    # %%
    Huff.scanTree(Huff.getRoot())