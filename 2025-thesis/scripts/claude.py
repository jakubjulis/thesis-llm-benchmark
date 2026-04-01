import anthropic
import json
import time

client = anthropic.Anthropic(
    api_key="..."
)

# Načítanie otázok
with open("dataset.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

results = []

print(f"Spúšťam testovanie {len(questions)} otázok...")

# Prechádzanie otázok
for q in questions:
    question_text = q['question_text']
    options_list = []
    for opt in q['options']:
        option_id = opt['id']
        option_text = opt['text']
        options_list.append(f"{option_id}) {option_text}")
    options_text = "\n".join(options_list)
    prompt = f"{question_text}\n\nMožnosti:\n{options_text}\n\nOdpoveď:"

    # Volanie API
    response = client.messages.create(
        model="claude-3-7-sonnet-20250219",
        max_tokens=1024, # 8000 pre thinking
        temperature=1.0,
        messages=[
            {"role": "user", "content": prompt}
        ]
        # thinking={
        #     "type": "enabled",
        #     "budget_tokens": 6000
        # }
    )

    answer = response.content[0].text.strip()
    # text_blocks = [block.text for block in response.content if block.type == "text"]
    # answer = "\n".join(text_blocks).strip()

    print(f"[{q['id']}] Odpoveď získaná.")
    results.append({
        "id": q['id'],
        "prompt": prompt,
        "model_answer": answer
    })

    time.sleep(1) # Pauza kvôli rate limitu

# Uloženie výsledkov
with open("vysledky-anthropic-claude-3-7-sonnet-20250219.json", "w", encoding="utf-8") as f:
    # vysledky-anthropic-claude-3-7-sonnet-20250219-thinking.json
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"Hotovo! Výsledky ({len(results)} záznamov)")
