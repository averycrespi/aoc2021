from collections import deque
from dataclasses import dataclass
import logging
import operator
from pythonjsonlogger import jsonlogger
from math import prod
from typing import Callable, Deque, Dict, Iterable, List, Sequence, Tuple
from helpers import read_input


logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
handler.setFormatter(formatter)
logger.addHandler(handler)


@dataclass
class Packet:
    version: int


@dataclass
class LiteralPacket(Packet):
    literal: int


@dataclass
class OperatorPacket(Packet):
    type_id: int
    sub_packets: Sequence[Packet]


def btoi(b: str) -> int:
    """Convert a bitstring into an integer."""
    return int(b, base=2)


def decode_literal_packet(version: int, stream: str) -> Tuple[LiteralPacket, str]:
    """Decode a literal packet, returning the packet and the remainder of the stream."""
    logger.info("decoding literal packet", extra={"version": version, "stream": stream})
    groups: List[str] = []
    while len(stream) >= 5:
        prefix, group, stream = stream[0], stream[1:5], stream[5:]
        groups.append(group)
        if prefix == "0":
            break
    literal = btoi("".join(groups))
    packet = LiteralPacket(version, literal)
    logger.info("decoded literal packet", extra={"packet": packet})
    return packet, stream


def decode_sub_packets_by_total_length(
    total_length: int, stream: str
) -> Tuple[Sequence[Packet], str]:
    """Decode sub-packets with a total length, returning the sub-packets and the remainder of the stream."""
    logger.info(
        "decoding sub-packet by total length",
        extra={"total_length": total_length, "stream": stream},
    )
    sub_packets: List[Packet] = []
    length = 0
    while length < total_length:
        original_length = len(stream)
        packet, stream = decode_packet(stream)
        sub_packets.append(packet)
        length += original_length - len(stream)
    assert length == total_length
    logger.info("decoded sub-packets by length", extra={"sub_packets": sub_packets})
    return sub_packets, stream


def decode_sub_packets_by_number(
    number: int, stream: str
) -> Tuple[Sequence[Packet], str]:
    """Decode a fixed number of sub-packets, returning the sub-packets and the remainder of the stream."""
    logger.info(
        "decoding sub-packets by number", extra={"number": number, "stream": stream}
    )
    sub_packets: List[Packet] = []
    for _ in range(number):
        packet, stream = decode_packet(stream)
        sub_packets.append(packet)
    logger.info("decoded sub-packets by number", extra={"sub_packets": sub_packets})
    return sub_packets, stream


def decode_operator_packet(
    version: int, type_id: int, stream: str
) -> Tuple[OperatorPacket, str]:
    """Decode an operator packet, returning the packet and the remainder of the stream."""
    logger.info(
        "decoding operator packet",
        extra={"version": version, "type_id": type_id, "stream": stream},
    )
    length_type_id, stream = stream[0], stream[1:]
    if length_type_id == "0":
        total_length, stream = btoi(stream[:15]), stream[15:]
        sub_packets, stream = decode_sub_packets_by_total_length(total_length, stream)
    elif length_type_id == "1":
        number, stream = btoi(stream[:11]), stream[11:]
        sub_packets, stream = decode_sub_packets_by_number(number, stream)
    else:
        raise ValueError(length_type_id)
    packet = OperatorPacket(version, type_id, sub_packets)
    logger.info("decoded operator packet", extra={"packet": packet})
    return packet, stream


def decode_packet(stream: str) -> Tuple[Packet, str]:
    """Decode a packet, returning the packet and the remainder of the stream."""
    logger.info("decoding packet", extra={"stream": stream})
    header, stream = stream[:6], stream[6:]
    version = btoi(header[:3])
    type_id = btoi(header[3:6])
    if type_id == 4:
        return decode_literal_packet(version, stream)
    else:
        return decode_operator_packet(version, type_id, stream)


def part1(packet: Packet) -> int:
    """What do you get if you add up the version numbers in all packets?"""
    version_sum = 0
    queue: Deque[Packet] = deque([packet])
    while len(queue) > 0:
        packet = queue.popleft()
        version_sum += packet.version
        if isinstance(packet, OperatorPacket):
            queue.extend(packet.sub_packets)
    return version_sum


def evaluate_operator_packet(packet: OperatorPacket) -> int:
    """Evaluate the expression associated with an operator packet."""
    functions: Dict[int, Callable[[Iterable[int]], int]] = {
        0: sum,
        1: prod,
        2: min,
        3: max,
    }
    operators: Dict[int, Callable[[int, int], bool]] = {
        5: operator.gt,
        6: operator.lt,
        7: operator.eq,
    }
    if 0 <= packet.type_id <= 3:
        return functions[packet.type_id](evaluate_packet(p) for p in packet.sub_packets)
    elif 4 <= packet.type_id <= 7:
        assert len(packet.sub_packets) == 2
        a, b = packet.sub_packets
        return int(operators[packet.type_id](evaluate_packet(a), evaluate_packet(b)))
    else:
        raise ValueError(packet.type_id)


def evaluate_packet(packet: Packet) -> int:
    """Evaluate the expression associated with a packet."""
    if isinstance(packet, LiteralPacket):
        return packet.literal
    elif isinstance(packet, OperatorPacket):
        return evaluate_operator_packet(packet)
    else:
        raise ValueError(packet)


def part2(packet: Packet) -> int:
    """What do you get if you evaluate the expression represented by your hexadecimal-encoded BITS transmission?"""
    return evaluate_packet(packet)


lines = read_input(16)
stream = bin(int(lines[0], base=16))[2:].zfill(len(lines[0] * 4))
packet, remainder = decode_packet(stream)
print(part1(packet))
print(part2(packet))
