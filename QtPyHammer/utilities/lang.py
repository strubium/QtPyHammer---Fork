
usingLanguage = "English"  # Default language

def setLanguage(language):
    global usingLanguage
    usingLanguage = language.lower()
    
def langFile(language=usingLanguage):
    match(language):
        case "english":
            return "File"
        case "spanish":
            return "Archivo"
        case "russian":
            return "Файл"
        case _:
            return "File"
            
def langEdit(language=usingLanguage):
    match(language):
        case "english":
            return "Edit"
        case "spanish":
            return "Editar"
        case "russian":
            return "Редактировать"
        case _:
            return "Edit"

def langTools(language=usingLanguage):
    match(language):
        case "english":
            return "Tools"
        case "spanish":
            return "Herramientas"
        case "russian":
            return "Инструменты"
        case _:
            return "Tools"
            
def langOk(language=usingLanguage):
    match(language):
        case "english":
            return "Ok"
        case "spanish":
            return "De acuerdo"
        case "russian":
            return "Хорошо"
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
        case "russian":
            return "Отменить"
        case _:
            return "Undo"
            
def langRedo(language=usingLanguage):
    match(language):
        case "english":
            return "Redo"
        case "spanish":
            return "Rehacer"
        case "russian":
            return "Повторить"
        case _:
            return "Redo"

def langCompile(language=usingLanguage):
    match(language):
        case "english":
            return "Compile"
        case "spanish":
            return "Compilar"
        case "russian":
            return "Скомпилировать"
        case _:
            return "Compile"

def langExit(language=usingLanguage):
    match(language):
        case "english":
            return "Exit"
        case "french":
            return "Sortir"
        case "spanish":
            return "Salida"
        case "russian":
            return "Выход"
        case _:
            return "Exit"

def langNo(language=usingLanguage):
    match(language):
        case "english":
            return "No"
        case "french":
            return "Non"
        case "russian":
            return "Нет"
        case _:
            return "No"

def langNormal(language=usingLanguage):
    match(language):
        case "english":
            return "Normal"
        case "french":
            return "Normale"
        case "spanish":
            return "Normala"
        case "russian":
            return "Нормальный"
        case _:
            return "Normal"

def langFast(language=usingLanguage):
    match(language):
        case "english":
            return "Fast"
        case "french":
            return "Rapide"
        case "spanish":
            return "Rapido"
        case "russian":
            return "Быстрый"
        case _:
            return "Fast"
