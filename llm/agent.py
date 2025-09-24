# def get_response(prompt):
#     #  example — need to replace with LLM later
#     if "hello" or Congratulations!"in prompt.lower():
#         return "Hi there, how can I assist you today?"
#     return "I heard you, but can you please repeat?"

# import os
# import torch
# from transformers import AutoModelForCausalLM, AutoTokenizer

# # Choose a small quantized model
# MODEL_ID = "llmware/tiny-llama-chat-ov"  # quantized TinyLlama Chat (OpenVINO int4)
# # Or fallback: "TheBloke/Alpaca‑native‑4bit‑GGML" if you convert to a suitable format

# # Load tokenizer
# tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)

# # Load model for CPU (with quantization if supported)
# model = AutoModelForCausalLM.from_pretrained(
#     MODEL_ID,
#     device_map="cpu",
#     torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
#     low_cpu_mem_usage=True
# )

# def get_response(prompt: str, max_new_tokens: int = 50) -> str:
#     """
#     Generate a chat response from the model using CPU.
#     """
#     # Clean up prompt if needed
#     input_ids = tokenizer(prompt, return_tensors="pt", truncation=True, padding=True).input_ids.to("cpu")

#     # Generate
#     with torch.no_grad():
#         output_ids = model.generate(
#             input_ids,
#             max_new_tokens=max_new_tokens,
#             do_sample=True,
#             temperature=0.7,
#             top_p=0.9,
#         )

#     resp = tokenizer.decode(output_ids[0], skip_special_tokens=True)

#     # The model may repeat the prompt, so strip prompt from response
#     if resp.lower().startswith(prompt.lower()):
#         resp = resp[len(prompt):]

#     return resp.strip()

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-small")
model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-small")

def get_response(prompt: str) -> str:
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids
    output_ids = model.generate(input_ids, max_new_tokens=50)
    response = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return response
