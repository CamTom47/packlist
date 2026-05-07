def convert_to_map(data: dict):
    mapped_object: dict = {}
    
    for key in data:
        return_key = ''
        for char in key:
            if char.isupper():
                return_key += f"_{char.lower()}"
            else:
                return_key += char
        mapped_object[key] = return_key
    return mapped_object


def serialize(data: dict):
    map = convert_to_map(data)
    return_columns = []
    raw_values = []
    
        
    # 	// {firstName: 'Aliya', lastName: 'Smith'} => ['"first_name"=%s', '"last_name"=%s']
    for key, value in data.items():
        if key != 'id':
            col_name = map[key]
            return_columns.append(f"{col_name} = %s")
            raw_values.append(value)
    
    
    return {
        "set_cols": ", ".join(return_columns),
        "raw_values": raw_values
    }
# 	
