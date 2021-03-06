# De-nest each list node up to record level
def denest_list_nodes(this_json, data_key, list_nodes):
    new_json = this_json
    i = 0
    for record in list(this_json.get(data_key, [])):
        for list_node in list_nodes:
            this_node = record.get(list_node, {}).get(list_node, [])
            if not this_node == []:
                new_json[data_key][i][list_node] = this_node
            else:
                new_json[data_key][i].pop(list_node)
        i = i + 1
    return new_json

# De-nest conversation_parts from conversations w/ key conversation fields
def transform_conversation_parts(this_json, data_key):
    new_json = []
    for record in list(this_json.get(data_key, [])):
        conv_id = record.get('id')
        conv_created = record.get('created_at')
        conv_updated = record.get('updated_at')
        conv_total_parts = record.get('conversation_parts', {}).get('total_parts')
        conv_parts = record.get('conversation_parts', {}).get('conversation_parts', [])
        for conv_part in conv_parts:
            part = conv_part
            part['conversation_id'] = conv_id
            part['conversation_total_parts'] = conv_total_parts
            part['conversation_created_at'] = conv_created
            part['conversation_updated_at'] = conv_updated
            new_json.append(part)
    return new_json


# Run other transforms, as needed: denest_list_nodes, transform_conversation_parts
def transform_json(this_json, stream_name, data_key):
    new_json = this_json
    if stream_name in ('users', 'leads'):
        list_nodes = ['companies', 'segments', 'social_profiles', 'tags']
        denested_json = denest_list_nodes(new_json, data_key, list_nodes)
        new_json = denested_json
    elif stream_name == 'companies':
        list_nodes = ['segments', 'tags']
        denested_json = denest_list_nodes(new_json, data_key, list_nodes)
        new_json = denested_json
    elif stream_name == 'conversations':
        list_nodes = ['tags']
        denested_json = denest_list_nodes(new_json, data_key, list_nodes)
        new_json = denested_json
    elif stream_name == 'conversation_parts':
        denested_json = transform_conversation_parts(new_json, data_key)
        new_json = denested_json
    if data_key in new_json:
        return new_json[data_key]
    else:
        return new_json
