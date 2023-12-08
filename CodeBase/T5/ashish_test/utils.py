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
        for arg in [arg1,arg2]:
            if "const_m1" == arg:
                arg = -1
            elif "const" in arg:
                arg = float(arg.split("_")[1])  
        # Handling different operations
        if 'add' in op:
            description = f"Step {i+1}: Add {arg1} and {arg2}. This gives the result: {res}"
        elif 'subtract' in op or 'minus' in op:
            description = f"Step {i+1}: Subtract {arg2} from {arg1}. This gives the result: {res}"
        elif 'multiply' in op:
            description = f"Step {i+1}: Multiply {arg1} by {arg2}. This gives the result: {res}"
        elif 'divide' in op:
            description = f"Step {i+1}: Divide {arg1} by {arg2}. This gives the result: {res}"
        elif 'larger' in op:
            description = f"Step {i+1}: Check if {arg1} is greater than {arg2}. This gives the result: {res}"
        elif 'exp' in op:
            description = f"Step {i+1}: Raise {arg1} to the power of {arg2}. This gives the result: {res}"   
        elif 'table' in op:
            description = f"Step {i+1}: Apply '{op.split('-')[0]}' operation on table row. This gives the result: {res}"

        formatted_steps.append(description)
        results.append(res)  # Storing result for future reference

    return ' ####### '.join(formatted_steps)

from torch.utils.data import Dataset
import torch

class FinQA_Dataset(Dataset):
    def __init__(self, tokenizer, df, max_q_len, max_a_len):
        self.tokenizer = tokenizer
        self.q_len = max_q_len
        self.t_len = max_a_len
        self.data = df
        self.questions = self.data["question"]
        self.context = self.data["context"]
        self.answer = self.data['answer']        
    def __len__(self):
        return len(self.questions)
    def __getitem__(self, idx):
        question = self.questions[idx]
        context = self.context[idx]
        answer = self.answer[idx]
        question_tokenized = self.tokenizer(question, context, max_length=self.q_len, padding="max_length",
                                                    truncation=True, pad_to_max_length=True, add_special_tokens=True)
        answer_tokenized = self.tokenizer(answer, max_length=self.t_len, padding="max_length", 
                                          truncation=True, pad_to_max_length=True, add_special_tokens=True)
        labels = torch.tensor(answer_tokenized["input_ids"], dtype=torch.long)
        # labels[labels == 0] = -100
        
        return {
            "input_ids": torch.tensor(question_tokenized["input_ids"], dtype=torch.long),
            "attention_mask": torch.tensor(question_tokenized["attention_mask"], dtype=torch.long),
            "labels": labels,
            "decoder_attention_mask": torch.tensor(answer_tokenized["attention_mask"], dtype=torch.long)
        }

