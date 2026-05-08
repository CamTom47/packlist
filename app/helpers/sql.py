def convert_to_map(data: dict):
    print('convert', type(data))
    mapped_object: dict = {}
    
    print('iofhdsahiof', data)
    
    for key in data.keys():
        return_key = ''
        for char in key:
            if char.isupper():
                return_key += f"_{char.lower()}"
            else:
                return_key += char
        mapped_object[key] = return_key
    return mapped_object


def serialize(data: dict):
    print('serialized data', data)
    map = convert_to_map(data)
    set_cols = []
    raw_values = []
    
        
    # 	// {firstName: 'Aliya', lastName: 'Smith'} => ['"first_name"=%s', '"last_name"=%s']
    for key, value in data.items():
        if key != 'id':
            col_name = map[key]
            set_cols.append(f"{col_name} = %s")
            raw_values.append(value)
    
    
    return {
        "set_cols": ", ".join(set_cols),
        "raw_values": raw_values
    }
# 	
