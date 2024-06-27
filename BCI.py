import streamlit as st
import os
from streamlit_tags import st_tags  # For tag functionality
from PIL import Image
import PyPDF2
import textract
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelForQuestionAnswering
import torch

# Configuration de la page Streamlit
st.set_page_config(page_title="Analyse de sentiment", layout="wide")

# Fonction pour diviser le texte en morceaux
def split_text_into_chunks(text, tokenizer, max_chunk_size):
    tokens = tokenizer(text, return_tensors='pt', truncation=False)['input_ids'][0]
    chunks = []
    for i in range(0, len(tokens), max_chunk_size):
        chunk = tokens[i:i + max_chunk_size]
        chunks.append(chunk)
    return chunks

# Fonction pour résumer le texte
def summarize_text(text):
    try:
        model_name = "facebook/bart-large-cnn"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)

        max_chunk_size = 512  # Taille maximale des morceaux
        chunks = split_text_into_chunks(text, tokenizer, max_chunk_size)

        summaries = []
        for chunk in chunks:
            chunk_text = tokenizer.decode(chunk, skip_special_tokens=True)
            summary = summarizer(chunk_text, max_length=150, min_length=30, do_sample=False)
            summaries.append(summary[0]['summary_text'])

        combined_summary = ' '.join(summaries)
        return combined_summary

    except Exception as e:
        return str(e)

# Option de thème
theme = st.sidebar.selectbox("Choisissez le thème", ["Clair", "Sombre"])

# Application du thème
if theme == "Sombre":
    st.markdown(
        """
        <style>
        body {
            background-color: #333;
            color: #fff;
        }
        .sidebar .sidebar-content {
            background-color: #444;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown(
        """
        <style>
        body {
            background-color: #fff;
            color: #000;
        }
        .sidebar .sidebar-content {
            background-color: #f0f0f0;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Titre de l'application
st.title("AtlantisBCI")

# Barre latérale pour la navigation avec icônes
section = st.sidebar.radio(
    "Option",
    [
        "🏠 Accueil",
        "📂 Stockage et Organisation",
        "🔍 Recherche",
        "🤝 Collaboration",
        "🔒 Sécurité",
        "🔗 Intégration",
        "👤 Profil Utilisateur"
    ]
)

# Fonction pour ajouter une image en arrière-plan
def add_bg_image():
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url('https://incubator.ucf.edu/wp-content/uploads/2023/07/artificial-intelligence-new-technology-science-futuristic-abstract-human-brain-ai-technology-cpu-central-processor-unit-chipset-big-data-machine-learning-cyber-mind-domination-generative-ai-scaled-1.jpg');
            background-size: cover;
            background-position: center;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

if section == "🏠 Accueil":
    add_bg_image()
    st.header("Bienvenue sur AtlantisBCI")
    st.write("""
    La Base de Connaissance Intelligente (BCI) est conçue pour améliorer la gestion des connaissances et la productivité.
    Utilisez la barre latérale pour naviguer entre les différentes sections de l'application.
    """)

if section == "📂 Stockage et Organisation":
    def extract_content(file_path):
        file_extension = file_path.split('.')[-1].lower()
        content = ""
        if file_extension in ["txt", "py", "md"]:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
        elif file_extension in ["jpg", "jpeg", "png", "gif"]:
            content = f"[Image: {file_path}]"
        elif file_extension == "pdf":
            with open(file_path, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                for page_num in range(len(reader.pages)):
                    page = reader.pages[page_num]
                    content += page.extract_text()
        else:
            content = textract.process(file_path).decode('utf-8')
        return content
    
    def display_file(file_path):
        file_extension = file_path.split('.')[-1].lower()
        if file_extension in ["txt", "py", "md"]:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
                st.text(content)
        elif file_extension in ["jpg", "jpeg", "png", "gif"]:
            st.image(file_path)
        elif file_extension == "pdf":
            with open(file_path, "rb") as file:
                st.download_button(label=f"Télécharger {file_path}", data=file, file_name=os.path.basename(file_path))
                st.write("Pour voir le PDF, téléchargez-le.")
        else:
            st.write(f"Format de fichier non pris en charge : {file_extension}")
    
    def delete_file(file_path):
        if os.path.exists(file_path):
            os.remove(file_path)
            st.success(f"Fichier '{os.path.basename(file_path)}' supprimé.")
    
    if 'section' not in st.session_state:
        st.session_state['section'] = None
    
    st.session_state['section'] = "📂 Stockage et Organisation"
    section = st.session_state['section']
    
    if section == "📂 Stockage et Organisation":
        add_bg_image()
        st.header("Stockage et Organisation des Connaissances")
        st.write("Téléchargez et organisez vos documents ici.")
        
        uploaded_files = st.file_uploader("Choisissez des fichiers", accept_multiple_files=True)
        if uploaded_files:
            for file in uploaded_files:
                file_path = os.path.join(storage_directory, file.name)
                with open(file_path, "wb") as f:
                    f.write(file.getbuffer())
                st.success(f"Fichier '{file.name}' téléchargé et sauvegardé.")
        
        st.subheader("Fichiers téléchargés")
        files = os.listdir(storage_directory)
        if files:
            for file in files:
                file_path = os.path.join(storage_directory, file)
                col1, col2, col3 = st.columns([4, 1, 1])
                with col1:
                    st.write(file)
                with col2:
                    if st.button(f"Voir", key=f"view_{file}"):
                        display_file(file_path)
                with col3:
                    if st.button(f"Supprimer", key=f"delete_{file}"):
                        delete_file(file_path)
                        st.experimental_rerun()
                content = extract_content(file_path)
                if content:
                    st.write(f"**Contenu extrait de {file} :**")
                    st.text_area(label="", value=content, height=300)
                    sentiment_result = summarize_text(content)
                    st.write(sentiment_result)
                    
        folder_name = st.text_input("Créer un nouveau dossier")
        if st.button("Créer Dossier"):
            new_folder_path = os.path.join(storage_directory, folder_name)
            if not os.path.exists(new_folder_path):
                os.makedirs(new_folder_path)
                st.success(f"Dossier '{folder_name}' créé.")
            else:
                st.warning(f"Le dossier '{folder_name}' existe déjà.")

    # Stocker le chemin du répertoire de stockage dans st.session_state
    storage_directory = "uploaded_files"
    if not os.path.exists(storage_directory):
        os.makedirs(storage_directory)
    st.session_state['storage_directory'] = storage_directory

elif section == "🔍 Recherche":
    add_bg_image()
    st.header("Recherche et Extraction de Connaissances")
    
    search_type = st.radio("Type de recherche", ["Web", "Bibliothèque", "Base de Connaissance"])
    search_query = st.text_input("Entrez votre requête de recherche")
    
    if st.button("Rechercher"):
        if search_type == "Web":
            st.write(f"Recherche sur le Web pour '{search_query}' :")
            st.write("Résultat Web 1")
            st.write("Résultat Web 2")
        elif search_type == "Bibliothèque":
            st.write(f"Recherche dans la Bibliothèque pour '{search_query}' :")
            
            # Charger un modèle de question-réponse de transformers
            model_name = "deepset/roberta-base-squad2"
            nlp = pipeline("question-answering", model=model_name)
            
            # Récupérer le répertoire de stockage depuis st.session_state
            storage_directory = st.session_state.get('storage_directory', 'uploaded_files')
            
            # Extraire le contenu des fichiers de la bibliothèque
            library_contents = []
            for file in os.listdir(storage_directory):
                file_path = os.path.join(storage_directory, file)
                content = extract_content(file_path)
                library_contents.append(content)
            
            # Combiner tous les contenus en un seul texte pour la recherche
            combined_content = " ".join(library_contents)
            result = nlp(question=search_query, context=combined_content)
            
            st.write(f"Réponse trouvée : {result['answer']}")
        elif search_type == "Base de Connaissance":
            st.write(f"Recherche dans la Base de Connaissance pour '{search_query}' :")
            st.write("Document Base de Connaissance 1")
            st.write("Document Base de Connaissance 2")

elif section == "🤝 Collaboration":
    add_bg_image()
    st.header("Collaboration et Partage")
    st.write("Partagez vos documents et collaborez avec votre équipe ici.")
    
    share_with = st_tags(
        label="Partagez avec",
        text="Appuyez sur entrée pour ajouter un email",
        value=[],
        suggestions=["user1@example.com", "user2@example.com"]
    )
    if st.button("Partager"):
        st.write(f"Documents partagés avec : {', '.join(share_with)}")
        
    st.text_area("Ajoutez un commentaire")

elif section == "🔒 Sécurité":
    add_bg_image()
    st.header("Sécurité et Confidentialité")
    st.write("Gérez les paramètres de sécurité et les permissions d'accès.")
    
    user_permissions = st.selectbox("Choisissez un utilisateur", ["User 1", "User 2", "User 3"])
    permission_level = st.radio("Niveau de permission", ["Lecture", "Écriture", "Admin"])
    if st.button("Mettre à jour les permissions"):
        st.write(f"Permissions de {user_permissions} mises à jour vers {permission_level}.")

elif section == "🔗 Intégration":
    add_bg_image()
    st.header("Intégration et Accessibilité")
    st.write("Intégrez Atlantis BCI avec d'autres outils et applications.")
    
    tools = st.multiselect("Choisissez les outils à intégrer", ["Google Drive", "Dropbox", "OneDrive", "Slack"])
    if st.button("Intégrer"):
        st.write(f"Outils intégrés : {', '.join(tools)}")

elif section == "👤 Profil Utilisateur":
    add_bg_image()
    st.header("Gestion de Profil Utilisateur")
    
    st.subheader("Informations du Profil")
    username = st.text_input("Nom d'utilisateur", "johndoe")
    email = st.text_input("Email", "johndoe@example.com")
    bio = st.text_area("Bio", "Développeur passionné par les technologies de l'information et de la communication.")
    
    if st.button("Mettre à jour le profil"):
        st.write("Profil mis à jour avec succès!")
    
    st.subheader("Votre Profil")
    st.write(f"**Nom d'utilisateur** : {username}")
    st.write(f"**Email** : {email}")
    st.write(f"**Bio** : {bio}")
