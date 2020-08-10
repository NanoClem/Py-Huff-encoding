
#-------------------------------------------------------
#       CHECKING PROGRAMM ARGUMENTS
#-------------------------------------------------------
def checkOptns(args: list) -> None:
    """Checks if the program options are used correctly.
    
    Parameters
    -----
        args (list) -- list of program's arguments
    
    Raises
    -----
        SystemError -- Called if a wrong option is used
    """
    usage = f'USAGE : {args[0]} (--compression <textFile> | --decompression <binFile> <freqMap.dat>)'
    opts  = ['--help', '--compression', '--decompression']

    if len(args) < 2:
        raise SystemExit(f'Wrong number of arguments, {usage}')

    if args[1] not in opts:
        raise SystemError(f'Wrong program options, choose between {opts}, {usage}')


#-------------------------------------------------------
#       COMPRESSION
#-------------------------------------------------------
def execCompression(args: list) -> str:
    """[summary]
    
    Parameters
    -----
        args (list) -- [description]
    
    Returns
    -----
        str -- [description]
    """
    usage = f'USAGE : {args[0]} --compression <textFile>'

    # CHECKING ARGUMENTS
    if len(args) != 3:
        raise SystemExit(f'Wrong number of arguments, {usage}')
    
    if not args[2].endswith('.txt'):
        raise SystemExit(f'Wrong file type for compression, text file expected, {usage}')

    # INIT HUFFMAN COMPRESSION
    Huff = HuffmanCoding()

    print("-------- STARTING COMPRESSION")
    compressed = Huff.compression(args[2])
    print("-------- COMPRESSION COMPLETED")

    return compressed


#-------------------------------------------------------
#       DECOMPRESSION
#-------------------------------------------------------
def execDecompression(args: list) -> str:
    """[summary]
    
    Parameters
    -----
        args (list) -- [description]
    
    Returns
    -----
        str -- [description]
    """
    usage = f'{args[0]} --decompression <binFile> <freqMap.dat>'

    # CHECKING ARGUMENTS
    if len(args) != 4:
        raise SystemExit(f'Wrong number of arguments, {usage}')

    if not args[2].endswith('.bin'):
        raise SystemExit(f'Wrong file type for decompression, binary file expected, {usage}')

    if not args[3].endswith('.dat'):
        raise SystemExit(f'Wrong file type for map frequencies, .dat expected, {usage}')

    # INIT HUFFMAN DECOMPRESSION
    Huff = HuffmanCoding()

    print("-------- STARTING DECOMPRESSION")
    decompressed = Huff.decompression(args[2], args[3])
    print("-------- DECOMPRESSION COMPLETED")

    return decompressed


#-------------------------------------------------------
#       MAIN
#-------------------------------------------------------
if __name__ == "__main__":

    import sys
    from HuffmanCoding import HuffmanCoding
    
    checkOptns(sys.argv)

    if sys.argv[1] == '--help':
        print(f'USAGE : {sys.argv[0]} --help | --compression <textFile> | --decompression <binFile> <freqMap.dat>')

    if sys.argv[1] == '--compression':
        execCompression(sys.argv)

    ##TODO: get a freqmap file as a new argument
    if sys.argv[1] == '--decompression':
        execDecompression(sys.argv)
