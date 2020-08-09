import json



class HuffNode(object):
    
    def __init__(self, label: str, freq: int, left=None, right=None) -> None:
        self.label = label
        self.freq  = freq
        self.left  = left
        self.right = right
        self.code  = ""


    def isLeaf(self) -> bool:
        """ Tell if the current node instance is a leaf.
        
        Returns
        -----
            bool -- True if the current instance is a leaf
        """
        return not self.left and not self.right


    def setLeft(self, newLeft) -> None:
        """[summary]
        
        Parameters
        -----
            newLeft ([type]) -- [description]
        
        Raises
        -----
            TypeError -- given instance should be a HuffNode
        """
        if not isinstance(newLeft, HuffNode):
            raise TypeError('not and instance of HuffNode')

        self.left = newLeft


    def setRight(self, newRight) -> None:
        """[summary]
        
        Parameters
        -----
            newRight ([type]) -- [description]
        
        Raises
        -----
            TypeError -- given instance should be a HuffNode
        """
        if not isinstance(newRight, HuffNode):
            raise TypeError('not and instance of HuffNode')

        self.left = newRight


    def setCode(self, newCode: str) -> None:
        """[summary]
        
        Parameters
        -----
            newCode (str) -- [description]
        
        Raises
        -----
            TypeError -- given instance should be a HuffNode
        """
        if not isinstance(newCode, str):
            raise TypeError('str expected')

        self.code = newCode


    def __lt__(self, other) -> bool:
        """Overrides the lower than operator for the HuffNode class.
        The lowest node is the one with the lowest frequency.

        Parameters
        -----
            other (HuffNode) -- HuffNode to compare

        Raises
        -----
            TypeError -- given instance should be a HuffNode
        
        Returns
        -----
            bool -- True if the current node is lower than the given one.
        """
        if not isinstance(other, HuffNode):
            raise TypeError('not an instance of HuffNode')

        return self.freq < other.freq

    
    def __gt__(self, other):
        """Overrides the greater than operator for the HuffNode class.
        The greater node is the one with the highest frequency.

        Parameters
        -----
            other (HuffNode) -- HuffNode to compare

        Raises
        -----
            TypeError -- given instance should be a HuffNode
        
        Returns
        -----
            bool -- True if the current node is greater than the given one.
        """
        if not isinstance(other, HuffNode):
            raise TypeError('not an instance of HuffNode')

        return self.freq > other.freq


    def __add__(self, other):
        """Overrides the addition operator for the Huffnode class.
        An addition operation on this instance consists in creating a new node whose frequency is equal
        to the addition of the two previous ones. The left node is always the one with the highest frequency.
        
        Parameters
        -----
            other (HuffNode) -- HuffNode to add

        Raises
        -----
            TypeError -- given instance should be a HuffNode
        
        Returns
        -----
            HuffNode -- new resulting HuffNode
        """
        if not isinstance(other, HuffNode):
            raise TypeError('not an instance of HuffNode')

        nodes = sorted([self, other], reverse=True)
        return HuffNode(label='#', freq=self.freq+other.freq, left=nodes[0], right=nodes[1])


    def __repr__(self) -> dict:
        """Defines an object representation of the HuffNode class instance.
        
        Returns
        -----
            dict -- object representation of the class instance.
        """
        return str({'label': self.label, 'freq': self.freq, 'left': self.left, 'right': self.right.code})


    def __str__(self) -> str:
        """Defines a string representation of the HuffNode class.
        
        Returns
        -----
            str -- object representation of the class.
        """
        return f'label: {self.label}, freq: {self.freq}, code: {self.code}'