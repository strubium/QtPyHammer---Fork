usingLanguage = "english"  # Default language

def setLanguage(language):
    global usingLanguage
    usingLanguage = language.lower()

def langOk(language=usingLanguage):
    match(language):
        case "english":
            return "Ok"
        case "spanish":
            return "De acuerdo"
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
            
def langRedo(language=usingLanguage):
    match(language):
        case "english":
            return "Redo"
        case _:
            return "Redo"

def langCompile(language=usingLanguage):
    match(language):
        case "english":
            return "Compile"
        case _:
            return "Compile"

def langExit(language=usingLanguage):
    match(language):
        case "english":
            return "Exit"
        case "french":
            return "Sortir"
        case _:
            return "Exit"

def langNo(language=usingLanguage):
    match(language):
        case "english":
            return "No"
        case "french":
            return "Non"
        case _:
            return "No"

def langNormal(language=usingLanguage):
    match(language):
        case "english":
            return "Normal"
        case "french":
            return "Normale"
        case _:
            return "Normal"

def langFast(language=usingLanguage):
    match(language):
        case "english":
            return "Fast"
        case "french":
            return "Rapide"
        case _:
            return "Fast"
