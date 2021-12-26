# https://adventofcode.com/2021/day/16
import sys
from math import prod


input = [line.strip() for line in sys.stdin]
input = input[0]


# part 1
hex_to_bin = lambda hex_str: ''.join([format(int(i, 16), '04b') for i in hex_str])

def parse_str(bin_stream, n_bits):
    return bin_stream[:n_bits], bin_stream[n_bits:]

def parse_int(bin_stream, n_bits):
    return int(bin_stream[:n_bits], 2), bin_stream[n_bits:]

def parse_packet(bin_stream):
    packet = {}
    original_len_bin_stream = len(bin_stream)
    packet['version'], bin_stream = parse_int(bin_stream, 3)
    packet['id'], bin_stream = parse_int(bin_stream, 3)
    if packet['id'] == 4: # value packet
        is_final_group = False
        sub_vals = []
        while not is_final_group:
            group_header, bin_stream = parse_int(bin_stream, 1)
            is_final_group = group_header == 0
            sub_val, bin_stream = parse_str(bin_stream, 4)
            sub_vals.append(sub_val)
        packet['value'] = int(''.join(sub_vals), 2)
    else: # operator packet
        length_type_id, bin_stream = parse_int(bin_stream, 1)
        packet['subpackets'] = []
        if length_type_id == 0:
            total_len, bin_stream = parse_int(bin_stream, 15)
            parsed_len = 0
            while parsed_len != total_len:
                subpacket, bin_stream = parse_packet(bin_stream)
                parsed_len += subpacket['length']
                packet['subpackets'].append(subpacket)
        else:
            n_subpackets, bin_stream = parse_int(bin_stream, 11)
            for _ in range(n_subpackets):
                subpacket, bin_stream = parse_packet(bin_stream)
                packet['subpackets'].append(subpacket)
    packet['length'] = original_len_bin_stream - len(bin_stream)
    return packet, bin_stream

def version_sum(packet):
    return packet['version'] + sum(map(version_sum, packet.get('subpackets', [])))

packets, _ = parse_packet(hex_to_bin(input))
print(version_sum(packets))

# part 2
def eval(packet):
    if 'value' in packet: return packet['value']

    operators = {
        0: sum,
        1: prod,
        2: min,
        3: max,
        5: lambda vals: 1 if vals[0] > vals[1] else 0,
        6: lambda vals: 1 if vals[0] < vals[1] else 0,
        7: lambda vals: 1 if vals[0] == vals[1] else 0,
    }
    op = operators[packet['id']]
    return op(list(map(eval, packet.get('subpackets', []))))

print(eval(packets))
