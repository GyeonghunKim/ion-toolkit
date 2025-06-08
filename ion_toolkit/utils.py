def L_str_to_int(L_str: str) -> int:
    if L_str == "S":
        return 0
    elif L_str == "P":
        return 1
    elif L_str == "D":
        return 2
    elif L_str == "F":
        return 3
    else:
        raise ValueError(f"Invalid L value: {L_str}")
    
    

