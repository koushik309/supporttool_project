# cert_utils.py
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from datetime import datetime, timedelta
from pathlib import Path

def generate_self_signed_cert(cert_dir: str = "certs", filename_prefix: str = ""):
    cert_path = Path(cert_dir)
    cert_path.mkdir(exist_ok=True)

    key_file = cert_path / f"{filename_prefix}key.pem"
    cert_file = cert_path / f"{filename_prefix}cert.pem"

    if key_file.exists() and cert_file.exists():
        return str(cert_file), str(key_file)

    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, u'localhost')
    ])
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.utcnow())
        .not_valid_after(datetime.utcnow() + timedelta(days=365))
        .sign(key, hashes.SHA256())
    )

    with open(key_file, "wb") as f:
        f.write(key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))

    with open(cert_file, "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))

    print(f"✔️ Self-signed certs generated in {cert_path}")
    return str(cert_file), str(key_file)
