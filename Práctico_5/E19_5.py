def cap(text):
    result = ""
    new_word = True

    for character in text:
        if new_word and 'a' <= character <= 'z':
            mayus = chr(ord(character) - 32)
            result += mayus
            new_word = False
        else:
            result += character
            new_word = character == " "

    return result

phrase = input("Ingrese una frase: ")
print(cap(phrase))