import os

import torch
from flask import Blueprint, Flask, jsonify, request
from transformers import AutoModelForCausalLM, AutoTokenizer

bp = Blueprint("routes", __name__)

model_name = os.environ.get("MODEL_NAME")
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)


def generate_neox_response(prompt, max_length=100):
    input_ids = tokenizer.encode(prompt, return_tensors="pt")
    with torch.no_grad():
        output_ids = model.generate(input_ids, max_length=max_length)
    return tokenizer.decode(output_ids[0], skip_special_tokens=True)


@bp.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("user_input", "")
    bot_response = generate_neox_response(user_input)
    return jsonify({"response": bot_response})


@bp.route("/")
def index():
    return "Hello, this is a placeholder for the index page."
