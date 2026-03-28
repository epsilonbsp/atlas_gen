import struct
import zlib

def image_blit(dst, dst_w, src, src_w, src_h, dx, dy):
    for row in range(src_h):
        dst_off = ((dy + row) * dst_w + dx) * 4
        src_off = row * src_w * 4
        dst[dst_off:dst_off + src_w * 4] = src[src_off:src_off + src_w * 4]

def image_write_png(path, w, h, rgba):
    def chunk(tag, data):
        c = tag + data

        return struct.pack(">I", len(data)) + c + struct.pack(">I", zlib.crc32(c) & 0xffffffff)

    stride = w * 4
    raw = b"".join(b"\x00" + bytes(rgba[y * stride:(y + 1) * stride]) for y in range(h))

    with open(path, "wb") as f:
        f.write(
            b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(raw))
            + chunk(b"IEND", b"")
        )
