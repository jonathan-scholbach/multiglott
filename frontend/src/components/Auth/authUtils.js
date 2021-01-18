function hasLowerCase(text) {
    return text.toUpperCase() != text
}   

function hasUpperCase(text) {
    return text.toLowerCase() != text
}


function contains(char, text){
    return text.includes(char)
}

function hasCharacter(text, charArray) {
    return charArray.some((char) => contains(char, text))
}

export function validatePassword(password, repeatedPassword, userName) {
    console.log("INSIDE")
    let errors = []

    if (!password) {
        errors.push("Password required.")
    }
    
    if (!repeatedPassword) {
        errors.push("Repeated password required.")
    }

    if (password != repeatedPassword) {
        errors.push("Passwords don't match.")
    }

    if (password.length < 8){
        errors.push("Password must contain at least 8 characters.")
    }

    if (!hasLowerCase(password)) {
        errors.push("Password must contain at least one lowercase character.")
    }

    if (!hasUpperCase(password)) {
        errors.push("Password must contain at least one uppercase character.")
    }

    const SPECIAL_CHARACTERS = [
        "!", 
        "§", 
        "@", 
        "$", 
        "%",
        "&",
        "/",
        "(",
        ")",
        "=",
        "?",
        "#",
        "*",
        "+",
        "-",
        ":",
        ".",
        ",",
        ";",
        "#",
        "~",
        "}",
        "{",
        "[",
        "]",
    ]

    if (!hasCharacter(password, SPECIAL_CHARACTERS)){
        errors.push(
            "Password must contain at least one of the following special characters: " + 
            SPECIAL_CHARACTERS
        )
    }

    if (password.includes(userName)){
        errors.push("Password must not contain the user name.")
    }

    return errors    
}