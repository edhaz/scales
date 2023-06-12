from dataclasses import dataclass


@dataclass
class Scale:
    instrument: str
    grade: int
    name: str
    octaves: int
    arp: bool
