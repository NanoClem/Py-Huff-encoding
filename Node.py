import json



class HuffNode(object):
    
    def __init__(self, label: str, freq: int, left=None, right=None) -> None:
        self.label = label
        self.freq  = freq
        self.left  = left
        self.right = right
        self.code  = ""


    ##TODO: behavior when "other" is None or not instance of Node class
    def __lt__(self, other) -> bool:
        """Overrides the lower than operator for the HuffNode class.
        The lowest node is the one with the lowest frequency.

        Parameters
        -----
            other (HuffNode) -- HuffNode to compare
        
        Returns
        -----
            bool -- True if the current node is lower than the given one.
        """
        return self.freq < other.freq

    
    ##TODO: behavior when "other" is None or not instance of Node class
    def __gt__(self, other):
        """Overrides the greater than operator for the HuffNode class.
        The greater node is the one with the highest frequency.

        Parameters
        -----
            other (HuffNode) -- HuffNode to compare
        
        Returns
        -----
            bool -- True if the current node is greater than the given one.
        """
        return self.freq > other.freq


    def __add__(self, other):
        """Overrides the addition operator for the Huffnode class.
        An addition operation on this instance consists in creating a new node whose frequency is equal
        to the addition of the two previous ones. The left node is always the one with the highest frequency.
        
        Parameters
        -----
            other (HuffNode) -- HuffNode to add
        
        Returns
        -----
            HuffNode -- new resulting HuffNode
        """
        nodes = [self, other]
        return HuffNode(label='#', freq=self.freq+other.freq, left=max(nodes), right=min(nodes))


    def __repr__(self) -> dict:
        """Defines an object representation of the HuffNode class instance.
        
        Returns
        -----
            dict -- object representation of the class instance.
        """
        return str({'label': self.label, 'freq': self.freq, 'left': self.left, 'right': self.right})


    def __str__(self) -> str:
        """Defines a string representation of the HuffNode class.
        
        Returns
        -----
            str -- object representation of the class.
        """
        return f'label: {self.label}, freq: {self.freq}, left: {self.left}, right: {self.right}'