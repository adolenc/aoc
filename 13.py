# https://adventofcode.com/2020/day/13
import sys
import math


input = [line.strip() for line in sys.stdin]


# part 1
ts = int(input[0])
buses = list([(int(bus), offset) for offset, bus in enumerate(input[1].split(',')) if bus != 'x'])

depart_ts, bus_id = min((math.ceil(ts / b) * b, b) for b, _ in buses)
print((depart_ts - ts) * bus_id)

# part 2
def lcm(a, b): return abs(a * b) // math.gcd(a, b)

ts_offset, ts_step = 0, 1
for bus_step, bus_offset in buses:
    while (ts_offset + bus_offset) % bus_step != 0:
        ts_offset += ts_step
    ts_step = lcm(ts_step, bus_step)

print(ts_offset)
