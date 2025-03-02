from transformers import AutoModelForQuestionAnswering
from transformers import Trainer,TrainingArguments
from datasets import load_dataset
from transformers import AutoTokenizer

# Load the dataset
dataset = load_dataset("squad")

# Load the tokenizer (Same as model)
model_name = "distilbert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForQuestionAnswering.from_pretrained(model_name)

# Tokenization function with answer positions
def tokenize_function(example):
    # Tokenize question and context together
    inputs = tokenizer(
        example["question"],
        example["context"],
        truncation=True,
        padding="max_length",
        max_length=512,
        return_offsets_mapping=True,  
    )

    start_positions = []
    end_positions = []

    for i in range(len(example["context"])):  
        if len(example["answers"][i]["answer_start"]) > 0:  
            start_char = example["answers"][i]["answer_start"][0]  
            end_char = start_char + len(example["answers"][i]["text"][0])  

            offsets = inputs["offset_mapping"][i]
            start_token = end_token = 0

            for j, (start, end) in enumerate(offsets):
                if start_char >= start and start_char < end:
                    start_token = j
                if end_char >= start and end_char < end:
                    end_token = j

            start_positions.append(start_token)
            end_positions.append(end_token)
        else:
            start_positions.append(0)
            end_positions.append(0)

    inputs["start_positions"] = start_positions
    inputs["end_positions"] = end_positions
    

    return inputs

tokenized_datasets = dataset.map(tokenize_function, batched=True)

training_args = TrainingArguments(
    output_dir="./qa_model",  
    evaluation_strategy="epoch",  
    per_device_train_batch_size=8,  
    per_device_eval_batch_size=8,
    num_train_epochs=3, 
    save_strategy="epoch",  
    logging_dir="./logs",  
    logging_steps=50,  
    learning_rate=3e-5,  
    weight_decay=0.01,  
    save_total_limit=2,  
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["validation"],
)
trainer.train()  