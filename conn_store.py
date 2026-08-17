# -*- coding: utf-8 -*-
"""连接信息的加密存储。

将已保存的 Redis 连接信息(含密码)以 JSON 形式使用 AES-256-GCM 加密后
写入 ~/.config/redis.json,避免配置以明文落盘。
使用 pycryptodome 实现,不依赖系统 OpenSSL,方便 PyInstaller 打包。

文件格式: {"v": 1, "salt": <base64>, "nonce": <base64>, "tag": <base64>, "data": <base64>}
明文内容: {"connections": [{"name", "host", "port", "username", "password"}]}
"""
import base64
import json
import os

from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes

CONFIG_DIR = os.path.expanduser("~/.config")
CONFIG_FILE = os.path.join(CONFIG_DIR, "redis.json")

# 固定的口令,用于派生 AES 密钥(防止配置明文落盘;若要更强保护可换成主密码方案)
_PASSPHRASE = b"tkredis.connection.store.v1"
_KDF_ITERATIONS = 600_000


def _derive_key(salt):
    return PBKDF2(
        _PASSPHRASE, salt, dkLen=32, count=_KDF_ITERATIONS,
        hmac_hash_module=SHA256,
    )


def _encrypt(plaintext: bytes) -> dict:
    salt = get_random_bytes(16)
    nonce = get_random_bytes(12)
    cipher = AES.new(_derive_key(salt), AES.MODE_GCM, nonce=nonce)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)
    return {
        "v": 1,
        "salt": base64.b64encode(salt).decode(),
        "nonce": base64.b64encode(nonce).decode(),
        "tag": base64.b64encode(tag).decode(),
        "data": base64.b64encode(ciphertext).decode(),
    }


def _decrypt(payload: dict) -> bytes:
    salt = base64.b64decode(payload["salt"])
    nonce = base64.b64decode(payload["nonce"])
    tag = base64.b64decode(payload["tag"])
    ciphertext = base64.b64decode(payload["data"])
    cipher = AES.new(_derive_key(salt), AES.MODE_GCM, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag)


class ConnectionStore:
    """已保存连接的加密存储。"""

    def __init__(self, path=CONFIG_FILE):
        self.path = path
        self.connections = []
        self.load()

    def load(self):
        self.connections = []
        if not os.path.exists(self.path):
            return

        try:
            with open(self.path, "r", encoding="utf-8") as f:
                payload = json.load(f)
            plaintext = _decrypt(payload)
            data = json.loads(plaintext.decode("utf-8"))
            for item in data.get("connections", []):
                self.connections.append({
                    "name": item.get("name", ""),
                    "host": item.get("host", ""),
                    "port": int(item.get("port", 6379)),
                    "username": item.get("username", ""),
                    "password": item.get("password", ""),
                })
        except Exception:
            # 文件损坏或解密失败时从空列表开始
            self.connections = []

    def save(self):
        data = {"connections": self.connections}
        payload = _encrypt(json.dumps(data, ensure_ascii=False).encode("utf-8"))

        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        try:
            os.chmod(self.path, 0o600)
        except OSError:
            pass

    def find(self, host, port):
        port = int(port)
        for conn in self.connections:
            if conn["host"] == host and conn["port"] == port:
                return conn
        return None

    def upsert(self, conn):
        """按 host:port 去重保存连接。"""
        existing = self.find(conn["host"], conn["port"])
        if existing:
            existing.update(conn)
        else:
            self.connections.append(dict(conn))
        self.save()

    def delete(self, host, port):
        conn = self.find(host, port)
        if conn:
            self.connections.remove(conn)
            self.save()
            return True
        return False
