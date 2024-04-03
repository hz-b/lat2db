
def filter_an_elements(tags, element_list, element_name):
    result = {}
    for element in element_list:
        if any(tag in element.tags for tag in tags):
            result.setdefault(f"{element_name}", []).append(element)
    return result