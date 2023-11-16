def remove_space(text_in):
    res = []

    for tmp in text_in.split(" "):
        if tmp != "":
            res.append(tmp)

    return " ".join(res)

def table_row_to_text(header, row):
    '''
    use templates to convert table row to text
    '''
    res = ""
    if header[0]:
        res += (header[0] + " ")
    for head, cell in zip(header[1:], row[1:]):
        res += ("the " + row[0] + " of " + head + " is " + cell + " ; ")
    res = remove_space(res)
    return res.strip()


def format_steps(steps):
    formatted_steps = []
    results = []  # To store results for reference in subsequent steps

    for i, step in enumerate(steps):
        op = step['op']
        arg1 = step['arg1']
        arg2 = step['arg2']
        res = step['res']
        # Handling references to previous results
        if arg1.startswith('#'):
            arg1_index = int(arg1[1:])  # Extracting the index
            arg1 = results[arg1_index]  # Replacing reference with actual value
        if arg2.startswith('#'):
            arg2_index = int(arg2[1:])
            arg2 = results[arg2_index]
        # Handling different operations
        if 'add' in op:
            description = f"Step {i+1}: Add {arg1} and {arg2}. Result: {res}"
        elif 'subtract' in op or 'minus' in op:
            description = f"Step {i+1}: Subtract {arg2} from {arg1}. Result: {res}"
        elif 'multiply' in op:
            description = f"Step {i+1}: Multiply {arg1} by {arg2}. Result: {res}"
        elif 'divide' in op:
            description = f"Step {i+1}: Divide {arg1} by {arg2}. Result: {res}"
        elif 'greater' in op:
            description = f"Step {i+1}: Check if {arg1} is greater than {arg2}. Result: {res}"
        elif 'exp' in op:
            description = f"Step {i+1}: Raise {arg1} to the power of {arg2}. Result: {res}"
        elif 'table' in op:
            description = f"Step {i+1}: Apply '{op.split('-')[0]}' operation on table row. Result: {res}"

        formatted_steps.append(description)
        results.append(res)  # Storing result for future reference

    return '\n'.join(formatted_steps)


