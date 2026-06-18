from scapy.all import fragment


FRAGMENTATION = False


def fragment_packet(packet):

    return fragment(
        packet,
        fragsize=8
    )