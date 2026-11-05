import hashlib
import os
import tempfile
import time
import urllib.error
import urllib.request

REPO_URL = "https://djunekz.github.io/termux-app-store"
KEY_URL = f"{REPO_URL}/termux-app-store.gpg"
PINNED_FINGERPRINTS = ("D39134A177717A5BEBEEAE7105D70CDBB6D80295",)
MAX_KEY_SIZE = 64 * 1024
ALLOWED_PACKET_TAGS = (2, 6, 13, 14, 17)
RETRY_AFTER_SECONDS = 6 * 3600


def _prefix() -> str:
    return os.environ.get("PREFIX", "/data/data/com.termux/files/usr")


def paths() -> dict:
    prefix = _prefix()
    apt = os.path.join(prefix, "etc/apt")
    keyring = os.path.join(apt, "keyrings", "termux-app-store.gpg")
    return {
        "apt": apt,
        "sources_dir": os.path.join(apt, "sources.list.d"),
        "sources_file": os.path.join(apt, "sources.list.d", "tas.list"),
        "keyring_dir": os.path.join(apt, "keyrings"),
        "keyring": keyring,
        "optout": os.path.join(apt, ".tas-no-auto-repo"),
        "retry": os.path.join(apt, ".tas-repo-retry"),
        "entry": f"deb [signed-by={keyring}] {REPO_URL} termux main",
    }


def is_termux() -> bool:
    return "com.termux" in _prefix() and os.path.isdir(paths()["apt"])


def pinned_fingerprints():
    override = os.environ.get("TAS_KEY_FPR", "").replace(" ", "").upper()
    return (override,) if override else PINNED_FINGERPRINTS


class KeyRejected(ValueError):
    pass


def _parse_packets(data: bytes):
    packets, pos, n = [], 0, len(data)
    try:
        while pos < n:
            hdr = data[pos]
            pos += 1
            if not hdr & 0x80:
                raise KeyRejected("not an OpenPGP packet stream")
            if hdr & 0x40:
                tag = hdr & 0x3F
                first = data[pos]
                if first < 192:
                    length, pos = first, pos + 1
                elif first < 224:
                    length, pos = ((first - 192) << 8) + data[pos + 1] + 192, pos + 2
                elif first == 255:
                    length, pos = int.from_bytes(data[pos + 1 : pos + 5], "big"), pos + 5
                else:
                    raise KeyRejected("unsupported packet length encoding")
            else:
                tag = (hdr >> 2) & 0x0F
                kind = hdr & 0x03
                if kind == 3:
                    raise KeyRejected("unsupported packet length encoding")
                size = (1, 2, 4)[kind]
                length = int.from_bytes(data[pos : pos + size], "big")
                pos += size
            if pos + length > n:
                raise KeyRejected("truncated key file")
            packets.append((tag, data[pos : pos + length]))
            pos += length
    except IndexError:
        raise KeyRejected("truncated key file")
    return packets


def verify_key_data(data: bytes):
    if len(data) > MAX_KEY_SIZE:
        raise KeyRejected("key file is too large")
    if data.startswith(b"-----BEGIN"):
        raise KeyRejected("key is ASCII-armored, a binary key is required")
    packets = _parse_packets(data)
    if not packets or packets[0][0] != 6:
        raise KeyRejected("file does not start with a public key")

    keys, primaries = [], 0
    for tag, body in packets:
        if tag not in ALLOWED_PACKET_TAGS:
            raise KeyRejected(f"unexpected OpenPGP packet type {tag}")
        if tag in (6, 14):
            if not body or body[0] != 4 or len(body) > 0xFFFF:
                raise KeyRejected("only version 4 public keys are supported")
            fpr = hashlib.sha1(b"\x99" + len(body).to_bytes(2, "big") + body).hexdigest().upper()
            if tag == 6:
                primaries += 1
                keys.append(("Key", fpr))
            else:
                keys.append(("Subkey", fpr))
    if primaries != 1:
        raise KeyRejected("file must contain exactly one primary key")
    if keys[0][1] not in pinned_fingerprints():
        raise KeyRejected("key fingerprint does not match the pinned fingerprint")
    return keys


def _active_lines(path: str):
    try:
        with open(path) as f:
            return [ln.strip() for ln in f if ln.strip() and not ln.strip().startswith("#")]
    except OSError:
        return []


def repo_is_configured() -> bool:
    p = paths()
    if not os.path.exists(p["keyring"]):
        return False
    return any(
        REPO_URL in ln and "signed-by=" in ln and "trusted=yes" not in ln
        for ln in _active_lines(p["sources_file"])
    )


def _download_key(timeout: float) -> bytes:
    req = urllib.request.Request(KEY_URL, headers={"User-Agent": "termux-app-store-repo-setup"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read(MAX_KEY_SIZE + 1)


def _remove_quiet(path: str) -> None:
    try:
        os.remove(path)
    except OSError:
        pass


def add_repo(timeout: float = 10.0) -> tuple:
    p = paths()
    try:
        data = _download_key(timeout)
    except (urllib.error.URLError, OSError, ValueError) as e:
        return False, f"could not download signing key: {e}"
    try:
        verify_key_data(data)
    except KeyRejected as e:
        return False, f"signing key rejected: {e}"

    tmp_path = None
    try:
        os.makedirs(p["keyring_dir"], exist_ok=True)
        os.makedirs(p["sources_dir"], exist_ok=True)
        fd, tmp_path = tempfile.mkstemp(dir=p["keyring_dir"], prefix=".tas-key-")
        with os.fdopen(fd, "wb") as f:
            f.write(data)
        os.chmod(tmp_path, 0o600)
        os.replace(tmp_path, p["keyring"])
        tmp_path = None
        with open(p["sources_file"], "w") as f:
            f.write(p["entry"] + "\n")
    except OSError as e:
        return False, f"could not write apt configuration: {e}"
    finally:
        if tmp_path:
            _remove_quiet(tmp_path)

    _remove_quiet(p["optout"])
    _remove_quiet(p["retry"])
    return True, "repository added"


def remove_repo() -> list:
    p = paths()
    removed = []
    for path in (p["sources_file"], p["keyring"]):
        if os.path.exists(path):
            os.remove(path)
            removed.append(path)
    try:
        with open(p["optout"], "w") as f:
            f.write("uninstall-repo was run; automatic repository setup is disabled\n")
    except OSError:
        pass
    return removed


def _auto_disabled() -> bool:
    if os.environ.get("TAS_NO_AUTO_REPO", "").strip() not in ("", "0"):
        return True
    return os.path.exists(paths()["optout"])


def _recently_failed() -> bool:
    try:
        return time.time() - os.path.getmtime(paths()["retry"]) < RETRY_AFTER_SECONDS
    except OSError:
        return False


def ensure_repo(printer=print) -> bool:
    try:
        if not is_termux() or _auto_disabled() or repo_is_configured():
            return False
        if _recently_failed():
            return False
        ok, msg = add_repo(timeout=5.0)
        if ok:
            printer("[termux-app-store] Apt repository added. Run `pkg update` to activate it.")
            return True
        try:
            with open(paths()["retry"], "w") as f:
                f.write(msg + "\n")
        except OSError:
            pass
        return False
    except Exception:
        return False
