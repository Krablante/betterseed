#!/usr/bin/env python3
"""Build the history fix from the checksum-pinned last BetterSeed release.

Only classes.dex and the manifest version change. Resources/native libraries are
copied unchanged. Output is aligned but unsigned; signing is a separate step.
"""

import argparse
import hashlib
import struct
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

sys.dont_write_bytecode = True
from patch_history import patch


BASE_SHA256 = "cc67b58477e43769fa59b17ccb9078844837e9a7c0f81d1e851ddd59bd1c3bd7"
VERSION_CODE = 1435393
VERSION_NAME = "2.22.0-bs.260922"


def version_manifest(data: bytes) -> bytes:
    """Change version attributes without recompiling the app's resources."""
    result = bytearray(data)
    offset = struct.unpack_from("<H", data, 2)[0]
    resource_ids = ()
    changed = 0
    while offset < len(data):
        kind, header_size, size = struct.unpack_from("<HHI", data, offset)
        if kind == 0x180:  # RES_XML_RESOURCE_MAP_TYPE
            resource_ids = struct.unpack_from(
                f"<{(size - header_size) // 4}I", data, offset + header_size)
        elif kind == 0x102:  # RES_XML_START_ELEMENT_TYPE
            extension = offset + header_size
            attr_start, attr_size, count = struct.unpack_from("<HHH", data, extension + 8)
            for index in range(count):
                attr = extension + attr_start + index * attr_size
                name = struct.unpack_from("<I", data, attr + 4)[0]
                if name < len(resource_ids) and resource_ids[name] == 0x0101021B:
                    if struct.unpack_from("<I", data, attr + 16)[0] != 1435392:
                        raise ValueError("Unexpected base versionCode")
                    struct.pack_into("<I", result, attr + 16, VERSION_CODE)
                    changed += 1
        offset += size
    if changed != 1:
        raise ValueError("Expected exactly one versionCode attribute")
    # Equal-length string-pool replacement keeps all binary XML offsets intact.
    old_name = "2.22.0.633363672"
    names_changed = 0
    for encoding in ("utf-8", "utf-16le"):
        old, new = old_name.encode(encoding), VERSION_NAME.encode(encoding)
        if len(old) != len(new):
            raise ValueError("Version name must keep the base string-pool length")
        names_changed += result.count(old)
        result = result.replace(old, new)
    if names_changed != 1:
        raise ValueError("Expected exactly one versionName string")
    return bytes(result)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("base", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    if hashlib.sha256(args.base.read_bytes()).hexdigest() != BASE_SHA256:
        parser.error("Base APK must be BetterSeed-20260410T193231Z.apk")
    if args.output.exists():
        parser.error("Output already exists; choose a new build path")
    if not args.output.parent.is_dir():
        parser.error("Output parent directory must exist")
    with tempfile.TemporaryDirectory(prefix="betterseed-build-", dir=args.output.parent) as tmp:
        work = Path(tmp)
        decoded = work / "decoded"
        subprocess.run(["apktool", "d", "-r", "-o", str(decoded), str(args.base.resolve())], check=True)
        patch(decoded)
        dex = work / "classes.dex"
        subprocess.run(["smali", "assemble", "--api", "35", "-j", "2",
                        "-o", str(dex), str(decoded / "smali")], check=True)
        unsigned = work / "unsigned.apk"
        with zipfile.ZipFile(args.base) as source, zipfile.ZipFile(unsigned, "w") as target:
            for entry in source.infolist():
                name = entry.filename
                if name.startswith("META-INF/") and (
                    name.upper().endswith((".SF", ".RSA", ".DSA", ".EC"))
                    or name == "META-INF/MANIFEST.MF"
                ):
                    continue
                data = source.read(name)
                if name == "classes.dex":
                    data = dex.read_bytes()
                elif name == "AndroidManifest.xml":
                    data = version_manifest(data)
                target.writestr(entry, data)
        subprocess.run(["zipalign", "-p", "4", str(unsigned), str(args.output.resolve())], check=True)
    print(f"Built unsigned APK: {args.output} (versionCode {VERSION_CODE})")


if __name__ == "__main__":
    main()
