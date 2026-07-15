alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

def rotate(cipher_text, rotation):
    decipher_text = []
    for i in cipher_text:
        for j in range(26):
            if i == alphabet[j]:
                if j + rotation >= 26:
                    decipher_text.append(alphabet[j + rotation - 26])
                elif j + rotation < 0:
                    decipher_text.append(alphabet[j + rotation + 26])
                else:
                    decipher_text.append(alphabet[j + rotation])

    return "".join(decipher_text)

def test_case(cipher_text):
    cipher_text = cipher_text.lower()
    
    for rotation in range(1, 26):
        output = []

        for i in cipher_text.split(" "):
            output.append(rotate(i, rotation))

        print("Rotation level = ", rotation)
        print(*output)
        print("")


cipher_text = "Otkz D zvmizy v amzz kjdio! di ocz wjs wzgjr"
test_case(cipher_text)