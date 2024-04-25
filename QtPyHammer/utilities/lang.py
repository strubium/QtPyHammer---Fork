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
        case "spanish":
            return "De acuerdo"
        case "german":
            return "Ok"
        case "italian":
            return "Ok"
        case _:
            return "Ok"

def langUndo(language=usingLanguage):
    match(language):
        case "english":
            return "Undo"
        case "french":
            return "Annuler"
        case "spanish":
            return "Deshacer"
        case "german":
            return "Rückgängig machen"
        case "italian":
            return "Annulla"
        case _:
            return "Undo"