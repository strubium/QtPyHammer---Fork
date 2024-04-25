usingLanguage = "english"  # Default language

def setLanguage(language):
    global usingLanguage
    usingLanguage = language.lower()

def langOk(language=usingLanguage):
    match(language):
        case "english":
            return "Ok"
        case "french":
            return "D'accord"
        case _:
            return "Ok"

def langUndo(language=usingLanguage):
    match(language):
        case "english":
            return "Undo"
        case "french":
            return "Annuler"
        case _:
            return "Undo"