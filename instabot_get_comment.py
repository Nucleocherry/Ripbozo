from instagrapi import Client
from pathlib import Path
from far import execute_it


PROMPT_FILE = Path("prompt.txt")

# --- 1️⃣ Connexion Insta ---
cl = Client()


cl.login("trashhernandez445@gmail.com", "Lerialerianew66")
cl.dump_settings("session.json")


username = "boz.orip"
user_id = cl.user_id_from_username(username)

# --- 2️⃣ Récupérer le dernier post ---
medias = cl.user_medias(user_id, 1)
if not medias:
    print("Pas de post récent.")
    exit()
last_post = medias[0]

# --- 3️⃣ Récupérer le commentaire le plus liké ---
comments = cl.media_comments(last_post.pk)
if comments:
    most_liked_comment = max(comments, key=lambda c: c.like_count)
    prompt = most_liked_comment.text
else:
    exit()

print("Commentaire utilisé comme légende :", prompt)

# --- 4️⃣ Générer l'image via SeleniumBase ---
nouveau_prompt = prompt

# --- Écraser le fichier avec le nouveau contenu ---
with open(PROMPT_FILE, "w", encoding="utf-8") as f:
    f.write(nouveau_prompt)

print(f"Le fichier {PROMPT_FILE} a été mis à jour avec :", nouveau_prompt)



execute_it()

caption = "Most liked comment get generated"

# --- 5️⃣ Publier sur Instagram ---
image_path = "photo/generated_photo.png"
cl.photo_upload(image_path, caption=caption)

print("Nouvelle image publiée avec le commentaire le plus liké ✅")
