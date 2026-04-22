import sys

psuedo = ['ORG', 'END', 'DEC', 'HEX']
MRI = {
    'AND': '0000',
    'ADD': '0001',
    'LDA': '0010',
    'STA': '0011',
    'BUN': '0100',
    'BSA': '0101',
    'ISZ': '0110'
    }
RRI = {
    'CLA': '0111100000000000',
    'CLE': '0111010000000000', 
    'CMA': '0111001000000000', 
    'CME': '0111000100000000', 
    'CIR': '0111000010000000', 
    'CIL': '0111000001000000',
    'INC': '0111000000100000',
    'SPA': '0111000000010000',
    'SNA': '0111000000001000',
    'SZA': '0111000000000100',
    'SZE': '0111000000000010',
    'HLT': '0111000000000001'
    }
IORI = {
    'INP': '1111100000000000',
    'OUT': '1111010000000000',
    'SKI': '1111001000000000',
    'SKO': '1111000100000000',
    'ION': '1111000010000000',
    'IOF': '1111000001000000'
}


def to_binary(n, bits):
    return format(n & 0xFFFF, f'0{bits}b')

def read_file():
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        raise TypeError("File name expected but not found")

    with open(filename, 'r') as file:
        lines = file.readlines()
        clean_lines = []
        for line in lines:
            line = line.split('/')[0].strip()
            if line:
                clean_lines.append(line)
    return clean_lines


def write_file(output):
    with open("machine_code.txt", 'w') as file:
        for line in output:
            file.write(f"{line}\n")


def first_pass(lines):
    lc=0
    labels = {}
    for line in lines:
        words = line.split()
        if words[0] == 'ORG':
            lc = int(words[1])
            continue
        elif words[0] == 'END':
            break
        elif ',' in words[0]:
            label = words[0].replace(',', '')
            labels[label] = lc
        lc+=1
    return labels

def second_pass(lines, labels):
    lc=0
    output = []

    for line in lines:
        words = line.split()
        if words[0] == 'ORG':
            lc = int(words[1])
            continue
        elif words[0] == 'END':
            break
        if ',' in words[0]:
            instruction = words[1]
            if instruction == 'DEC':
                binary = to_binary(int(words[2]), 16)
            elif instruction == 'HEX':
                binary = to_binary(int(words[2], 16), 16)
            op_half = binary
        else:
            instruction = words[0]
            if instruction in MRI:
                op_code = MRI[instruction]
                addr_label = words[1]
                if addr_label in labels:
                    address = labels[addr_label]
                else:
                    address = int(addr_label)
                op_half = op_code + to_binary(address, 12)

            elif instruction in RRI:
                op_code = RRI[instruction]
                op_half = op_code
            elif instruction in IORI:
                op_code = IORI[instruction]
                op_half = op_code
            else:
                raise ValueError(f"Unknown assembler instruction: {instruction}")
        full_line = to_binary(lc, 12) + " " + op_half
        output.append(full_line)
        lc+=1
    return output


def main():
    lines = read_file()
    labels = first_pass(lines)
    output = second_pass(lines, labels)
    write_file(output)

main()
