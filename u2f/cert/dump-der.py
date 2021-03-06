from asn1crypto.keys import ECPrivateKey

def pk_to_c_array(name, pk_der):
    # parse der format
    pk = ECPrivateKey.load(pk_der)

    # extract private key
    pk_native = pk['private_key'].native

    # translate to hex string
    pk_hex = hex(pk_native)
    # remove leading 0x and trailing L
    pk_hex = pk_hex[2:-1]
    # pad with zeros to 32 bytes
    pk_hex = ("0" * (64 - len(pk_hex))) + pk_hex

    # split by pairs of characters
    hex_bytes = ["0x" + pk_hex[i:i + 2] for i in range(0, len(pk_hex), 2)]

    # make string C array declaration
    return "const uint8_t " + name + "[32] = {" + ", ".join(hex_bytes) + "};"

def cert_to_c_array(name, der):
    defname = name.upper() + "_LEN"
    hex_str = der.encode('hex')
    hex_bytes = ["0x" + hex_str[i:i + 2] for i in range(0, len(hex_str), 2)]

    define = "#define " + defname + " " + str(len(der))
    array = "const uint8_t " + name + "[" + defname + "] = {" + ", ".join(hex_bytes) + "};"
    return define + "\n" + array

with open("attestation.der", "r") as f:
    print cert_to_c_array("attestation_der", f.read())

with open("attestation_key.der", "r") as f:
    print pk_to_c_array("attestation_key", f.read())
