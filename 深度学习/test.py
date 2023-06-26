import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForSequenceClassification

tokenizer = AutoTokenizer.from_pretrained("textattack/bert-base-uncased-yelp-polarity")
model = AutoModelForSequenceClassification.from_pretrained("textattack/bert-base-uncased-yelp-polarity")
# To train a model on `num_labels` classes, you can pass `num_labels=num_labels` to `.from_pretrained(...)`
# num_labels = len(model.config.id2label)
# model = AutoModelForSequenceClassification.from_pretrained("textattack/bert-base-uncased-yelp-polarity", num_labels=num_labels)


with open('./input.txt', 'r') as f:
    lines = f.readline()
    while lines:
        sentence = lines[:-1]
        inputs = tokenizer(sentence, return_tensors="pt")
        with torch.no_grad():
            logits = model(**inputs).logits

        output = F.softmax(logits, dim=1)
        predicted_class_id = output.argmax().item()
        # pre_lable = model.config.id2label[predicted_class_id]
        print(sentence, predicted_class_id, torch.max(output).item())
        lines = f.readline()


