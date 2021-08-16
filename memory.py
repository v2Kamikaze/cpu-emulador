from array import array


memory: array = array("L", [0]) * (1 * 512 * 512//4)


def read_word(word_addr: int) -> int:
    """
        Recebe o endereço de uma word e retorna seu conteúdo (os 4 bytes).
    """
    word_addr = word_addr & 0b111111111111111111
    return memory[word_addr]


def write_word(word_addr: int, value: int) -> None:
    """
        Recebe o endereço de uma word, e escreve o valor passado nesse endereço de memória.
    """
    word_addr = word_addr & 0b111111111111111111
    memory[word_addr] = value


def read_byte(byte_addr: int) -> int:

    """
        Recebe um endereço de um byte da memória e retorna o conteúdo desse byte.
    """
    word = byte_addr >> 2
    byte = byte_addr & 0b11
    byte_shift = byte << 3
    
    value = read_word(word)
    value = value >> byte_shift
    value = value & 0xFF
    
    return value


def write_byte(byte_addr: int, value: int) -> None:
    """
        Recebe um endereço de um byte da memória e escreve o valor recebido nesse byte.
    """
    word_address = byte_addr >> 2
    word_address = word_address & 0b111111111111111111
    byte = byte_addr & 0b11
    byte_sft = byte << 3

    mask = ~(0xFF << byte_sft)
    valr = memory[word_address] & mask
    value = value << byte_sft

    memory[word_address] = (value | valr)
