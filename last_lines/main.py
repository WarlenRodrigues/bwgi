import io

def last_lines(filename, buffer_size=io.DEFAULT_BUFFER_SIZE):

    # Open the file with filename using rb to read bytes
    with open(filename, 'rb') as f:
        # Positioning at the end of the file
        f.seek(0, io.SEEK_END)
        
        # Initialize list to hold read lines
        lines = []
        buffer = b''
        position = f.tell()
        
        # The pointer needs to get to the position 0
        while position > 0:

            # How much to move the pointer backwards
            move_back = min(buffer_size, position)
            position -= move_back

            # Reads the part between the pointer position and the previous position not read yet
            f.seek(position)
            buffer = f.read(move_back) + buffer  # Join read segment to buffer
            
        # Tries to decode buffer, need to care for utf8
        while buffer:
            try:
                decoded_buffer = buffer.decode('utf-8')
                break
            except UnicodeDecodeError:
                # If get error on decoding, does not decode
                raise Exception("Erro durante o processo de decode")
            
        # Proccesses the read lines
        while '\n' in decoded_buffer:
            line, decoded_buffer = decoded_buffer.split('\n', 1)
            lines.append(line + '\n')
        
        # If theres some remaining data, add line
        if decoded_buffer:
            lines.append(decoded_buffer + '\n')
        
        # Revert lines and return iter
        return iter(reversed(lines))

for line in last_lines('my_file.txt', 1):
    print(line, end='')

'''
    Testado com Olá, Mundo, &%.

    Usando file para abrir o arquivo para leitura de bytes. Iniciando com o "ponteiro" no final do arquivo e voltando a quantidade de bytes passado como parâmetro (ou a quantidade restante, se menor que o parâmetro). 

    Após leitura completa do arquivo, decodifica com tratamento de erro.

    Separa as linhas splitando por \n e adiciona na lista que será retornada

    Tempo: O(n) Memória O(n)

'''