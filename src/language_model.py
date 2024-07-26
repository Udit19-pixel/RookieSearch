from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

def load_language_model(model_name="gpt2"):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    
    # Set pad_token_id to eos_token_id if it's not set
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token_id = tokenizer.eos_token_id
    
    if torch.cuda.is_available():
        model = model.to('cuda')
    
    return model, tokenizer

def generate_text(model, tokenizer, input_text, max_length=100):
    # Encode the input text and create attention mask
    inputs = tokenizer.encode_plus(
        input_text, 
        add_special_tokens=True, 
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=max_length
    )
    
    input_ids = inputs["input_ids"]
    attention_mask = inputs["attention_mask"]
    
    if torch.cuda.is_available():
        input_ids = input_ids.to('cuda')
        attention_mask = attention_mask.to('cuda')
    
    # Generate output with improved parameters
    output = model.generate(
        input_ids,
        attention_mask=attention_mask,
        max_length=max_length,
        num_return_sequences=1,
        no_repeat_ngram_size=2,
        do_sample=True,
        top_k=50,
        top_p=0.95,
        temperature=0.7
    )
    
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    return generated_text

# Test the language model
if __name__ == "__main__":
    model, tokenizer = load_language_model()
    
    input_text = "Python is a programming language that"
    generated_text = generate_text(model, tokenizer, input_text)
    
    print(f"Generated text: {generated_text}")