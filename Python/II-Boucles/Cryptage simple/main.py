DECALAGE = 35

CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def get_letter(i):
    """
    Retourne la lettre correspondant à l'indice i dans l'alphabet.
    """
    #j est l'indice de position de la lettre compris entre 0 et 25 et associé à l'indice i
    j = (i + DECALAGE) % len(CHARS)
    return CHARS[j]

def crypter_message(message):
    """
    Crypte le message en utilisant le chiffrement par décalage.
    """
    message = message.upper()
    message_crypte = ""
    for caractere in message:
        if caractere in CHARS:
            i = CHARS.index(caractere)
            
            lettre_cryptee = get_letter(i)
            message_crypte += lettre_cryptee
        else:
            message_crypte += caractere  # On conserve les caractères non alphabétiques tels quels
    return message_crypte

if __name__ == "__main__":
    message = input("Entrez le message à crypter : ")
    message_crypte = crypter_message(message)
    print("Message crypté :", message_crypte)