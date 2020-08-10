import heapq
import os
from Node import HuffNode



class HuffmanCoding(object):


    def __init__(self) -> None:
        self._root = None
        self.heap = []
        self.codes = {}
        self.reverseMapping = {}


    def getRoot(self) -> HuffNode:
        """ Returns the root node of the Huffman Tree
        
        Returns
        -----
            HuffNode -- [description]
        """
        return self._root


    def _setRoot(self, newRoot: HuffNode) -> None:
        """ Set a new root for the Huffman Tree
        
        Parameters
        -----
            newRoot (HuffNode) -- new root of the tree
        """
        if not isinstance(newRoot, HuffNode):
            raise TypeError('not an instance of HuffNode')

        self._root = newRoot


    def scanTree(self, root: HuffNode) -> None:
        """Scan the given Huffman tree in depth and print each encountered node.
        
        Parameters
        -----
            root (HuffNode) -- given root node of the Huffman tree
        """
        if root:
            print(root)

        if root.left:
            self.scanTree(root.left)

        if root.right:
            self.scanTree(root.right)


    ##TODO: see if it's possible to use an iterator over the text
    def makeFreqMap(self, text: str) -> dict:
        """ Build the frequency map of each character
        in the given text.
        
        Parameters
        -----
            text (str) -- source text
        
        Returns
        -----
            dict -- dictionnary of word frequencies
        """
        freqMap = {}
        for char in text:
            if char not in freqMap.keys():
                freqMap[char] = 1
            else:
                freqMap[char] += 1

        return freqMap


    def writeFreqFile(self, freqFilename: str, freqMap: dict) -> None:
        """ Writes the given char frequencies mapping in a .dat file.
        Resulting data will be written by rows as a csv style.
        
        Parameters
        -----
            freqFilename (str) -- output file where data will be written
            freqMap (dict) -- mapping of char frequencies
        """
        try:
            with open(freqFilename, 'w') as f:
                for char,freq in freqMap.items():
                    char = ord(char)    # ascii code conversion
                    f.write(str(char) + ' ' + str(freq) + '\n')
        except IOError as e:
            print(f'Unable to open file {freqFilename} : {e}')


    def readFreqFile(self, freqFilename: str) -> dict:
        """ Builds a char frequencies mapping by reading data from the given file.
        
        Parameters
        -----
            freqFilename (str) -- file where mapping data are read
        
        Returns
        -----
            dict -- resulting char frequencies mapping
        """
        freqMap = {}
        try:
            with open(freqFilename, 'r') as f:
                line = f.readline()
                while line:
                    data = line[:-1].split(' ')     # remove trailing LF and get mapping data
                    char = chr(int(data[0]))        # converting ascii code to char
                    freqMap[char] = int(data[1])    # building mapping
                    line = f.readline()

        except IOError as e:
            print(f'Unable to open file {freqFilename} : {e}')

        finally:
            return freqMap


    def makeHeap(self, freqMap: dict) -> None:
        """Build a heap of Huffman nodes based on
        the given frequencies map.
        
        Parameters
        -----
            freqMap (dict) -- source frequencies map

        Returns
        -----
            list -- resulting heap as a list.
        """
        heap = []
        n = None

        for k,v in freqMap.items():
            n = HuffNode(k, v)          # key=label, value=freq 
            heapq.heappush(heap, n)
        
        return heap


    def mergeNodes(self, heap: list) -> None:
        """Merge each nodes from a given heap until only one is left.
        Each iteration adds the two lowest nodes by their frequencies, and merges them into a new one.
        
        Parameters
        -----
            heap (list) -- source heap containing Huffman nodes
        """
        n1, n2 = None, None
        father = None

        while(len(heap) > 1):
            n1 = heapq.heappop(heap)        # get the two nodes with the lowest
            n2 = heapq.heappop(heap)        # frequencies of the heap
            father = n1 + n2                # merging nodes by using the overrided add operator
            heapq.heappush(heap, father)    # adding the new father node

        self._setRoot(heap[0])   # set the final resulting node as root of the Huffman Tree


    def makeEncoding(self, root: HuffNode, code: str="") -> None:
        """[summary]
        
        Parameters
        -----
            root (HuffNode) -- [description]
            code (str) -- [description] (default: "")
        
        Raises
        -----
            TypeError -- given instance should be a HuffNode
        """
        if not root:
            return

        if root.isLeaf(): # root.label != '#':
            self.codes[root.label] = code           # insert code in mapping
            self.reverseMapping[code] = root.label  # filling reverse mapping
            root.setCode(code)                      # set code to the node

        self.makeEncoding(root.left, code + '0')    # encode left node
        self.makeEncoding(root.right, code + '1')   # encode right node


    def getEncodedText(self, text: str) -> str:
        """ Returns the str version of the encoded text.
        Note that the encoding should have been made before calling this function.
        
        Parameters
        -----
            text (str) -- source text
        
        Returns
        -----
            str -- encoded text as str
        """
        res = ""
        for char in text:
            res += self.codes[char]

        return res


    def addPadding(self, encodedText: str) -> str:
        """ Adds padding to the encoded text to have its lenght multiple of 8.
        The padding is added at the end of the str, and the padding length is written at 
        the begining as a binary integer.
        
        Parameters
        -----
            encodedText (str) -- encoded source text
        
        Returns
        -----
            str -- encoded source text with extra padding
        """
        padding    = 8 - len(encodedText) % 8
        paddingBin = f'{padding:08b}'
        return paddingBin + encodedText + '0'*padding


    def getByteArray(self, pEncodedText: str) -> bytearray:
        """Casts the given encoded text into a byte array.
        Note that the given encoded text should have been padded before calling this function.
        
        Parameters
        -----
            pEncodedText (str) -- encoded source text with extra padding

        Raises
        -----
            ValueError -- encoded text lenght isn't a multiple of 8
        
        Returns
        -----
            bytearray -- resulting byte
        """
        if len(pEncodedText) % 8 != 0:
            raise ValueError('given encoded text not properly padded')

        b = bytearray()
        for i in range(0, len(pEncodedText), 8):   
            byte = pEncodedText[i:i+8]              # taking 8 bit to form a byte
            b.append(int(byte, 2))

        return b


    def compression(self, input_file: str) -> str:
        """ Compress the given file with the Huffman method and
        write the result in a binary file.
        
        Parameters
        -----
            input_file (str) -- source file
        
        Returns
        -----
            str -- file path where the binary result is written
        """
        filename, extension = os.path.splitext(input_file)
        output_file = filename + '.bin'
        freq_file = filename + '.dat'

        try:
            with open(input_file, 'r') as f, open(output_file, 'wb') as output:
            
                # TEXT AND FREQ MAP
                text    = f.read()
                freqMap = self.makeFreqMap(text)    # building freq map

                # WRITING CHAR FREQ FILE
                self.writeFreqFile(freq_file, freqMap)

                # BUILD HUFFMAN TREE
                heap = self.makeHeap(freqMap)       # making heap
                self.mergeNodes(heap)               # building Huffman Tree
                root = self.getRoot()               # get the resulting tree

                # INIT ENCODING
                self.makeEncoding(root)                         # char encoding
                encodedText = self.getEncodedText(text)         # encode text
                pEncodedText = self.addPadding(encodedText)     # add padding

                # BYTE AND OUTPUT
                b = self.getByteArray(pEncodedText)     # get bytearray of padded encoded text
                output.write(bytes(b))                  # write it as binary in output file

        except IOError as e:
            print(f'Unable to open file : {e}')

        finally:
            return output_file


    def removePadding(self, pEncodedText: str) -> str:
        """ Removes the extra padding of the given padded encoding text.
        This function assumes that the given text is encoded, have an extra padding
        at the end and the padding size written as a binary integer.
        
        Parameters
        -----
            pEncodedText (str) -- encoded and padded source text
        
        Returns
        -----
            str -- encoded source text without extra padding
        """
        paddingBin   = pEncodedText[:8]         # get the padding size written in binary int
        padding      = int(paddingBin, 2)       # convert as int
        pEncodedText = pEncodedText[8:]         # keep the text without padding info at the begining

        return pEncodedText[:-1 * padding]      # removing extra padding from the end


    def decoding(self, encodedText: str) -> str:
        """ Decode a given text encoded by the Huffman method.
        Note that the given encoded text should not contain any padding.
        
        Parameters
        -----
            encodedText (str) -- source encoded text
        
        Returns
        -----
            str -- decoded source text
        """
        currentCode = ""
        decodedText = ""

        for bit in encodedText:
            currentCode += bit
            if currentCode in self.reverseMapping.keys():
                decodedText += self.reverseMapping[currentCode]
                currentCode = ""

        return decodedText


    def decompression(self, binaryFile: str, freqFile: str) -> str:
        """ Decompress a given binary file and returns 
        the filename of the result.
        
        Parameters
        -----
            binaryFile (str) -- previously compressed source binary file
        
        Returns
        -----
            str -- decompressed file    
        """
        filename, extension = os.path.splitext(binaryFile)
        decodedFile = filename + '_decompressed.txt' 

        with open(binaryFile, 'rb') as f, open(freqFile, 'r'), open(decodedFile, 'w') as output:
            bitCode = ""

            byte = f.read(1)        # read only 1 byte = 8 bits
            while len(byte) > 0:
                byte = ord(byte)
                bits = bin(byte)[2:].rjust(8, '0')
                bitCode += bits
                byte = f.read(1)

            encodedText = self.removePadding(bitCode)   # remove padding

            # READING FREQ MAP
            freqMap = self.readFreqFile(freqFile)

            # REBUILD HUFFMAN TREE
            heap = self.makeHeap(freqMap)       # making heap
            self.mergeNodes(heap)               # building Huffman Tree
            self.makeEncoding(self.getRoot())   # char encoding

            decompressedText = self.decoding(encodedText)
            output.write(decompressedText)

        return decodedFile