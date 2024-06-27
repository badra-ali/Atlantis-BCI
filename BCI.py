import streamlit as st
import os
from streamlit_tags import st_tags  # For tag functionality
from PIL import Image
import PyPDF2
import textract
from transformers import pipeline

# Configuration de la page Streamlit
st.set_page_config(page_title="Analyse de sentiment", layout="wide")

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

# Exemple d'utilisation dans la section Accueil
#section = "🏠 Accueil"  # Cette variable peut être modifiée selon votre logique de navigation
if section == "🏠 Accueil":
    add_bg_image()  # Ajout de l'image en arrière-plan
    st.header("Bienvenue sur AtlantisBCI")
    st.write("""
    La Base de Connaissance Intelligente (BCI) est conçue pour améliorer la gestion des connaissances et la productivité.
    Utilisez la barre latérale pour naviguer entre les différentes sections de l'application.
    """)


if section == "📂 Stockage et Organisation":
    # Fonction pour extraire le contenu des fichiers PDF
    def extract_content(file_path):
        content = ""
        with open(file_path, 'rb') as f:
            reader = PdfFileReader(f)
            num_pages = reader.getNumPages()
            for page_num in range(num_pages):
                page = reader.getPage(page_num)
                content += page.extractText()
        return content
    
    # Analyse de sentiment
    def analyze_sentiment(text):
        sentiment_analyzer = pipeline("sentiment-analysis")
        result = sentiment_analyzer(text)
        return result
    
    # Interface utilisateur Streamlit
    uploaded_files = st.file_uploader("Choisissez des fichiers", accept_multiple_files=True)
    
    if uploaded_files:
        for file_num, uploaded_file in enumerate(uploaded_files):
            # Sauvegarde du fichier téléchargé temporairement
            file_path = os.path.join("temp_files", f"file_{file_num}_{uploaded_file.name}")
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Extraction du contenu du fichier PDF
            content = extract_content(file_path)
            
            # Affichage du contenu extrait
            st.write(f"Contenu extrait du fichier {uploaded_file.name} :")
            st.write(content)
            
            # Analyse de sentiment
            sentiment_result = analyze_sentiment(content)
            st.write(f"Résultat de l'analyse de sentiment du fichier {uploaded_file.name} :")
            st.write(sentiment_result)
            
            # Suppression du fichier temporaire après utilisation
            os.remove(file_path)


            
# Fonctionnalité de recherche
elif section == "🔍 Recherche":
    add_bg_image()
    st.header("Recherche et Extraction de Connaissances")
    
    # Sélection du type de recherche
    search_type = st.radio("Type de recherche", ["Web", "Bibliothèque", "Base de Connaissance"])
    search_query = st.text_input("Entrez votre requête de recherche")
    
    if st.button("Rechercher"):
        if search_type == "Web":
            st.write(f"Recherche sur le Web pour '{search_query}' :")
            # Simuler des résultats de recherche sur le web
            st.write("Résultat Web 1")
            st.write("Résultat Web 2")
        elif search_type == "Bibliothèque":
            st.write(f"Recherche dans la Bibliothèque pour '{search_query}' :")
            # Simuler des résultats de recherche dans la bibliothèque
            st.write("Document Bibliothèque 1")
            st.write("Document Bibliothèque 2")
        elif search_type == "Base de Connaissance":
            st.write(f"Recherche dans la Base de Connaissance pour '{search_query}' :")
            # Simuler des résultats de recherche dans la base de connaissances
            st.write("Document Base de Connaissance 1")
            st.write("Document Base de Connaissance 2")

# Fonctionnalité de collaboration
elif section == "🤝 Collaboration":
    add_bg_image()
    st.header("Collaboration et Partage")
    st.write("Partagez vos documents et collaborez avec votre équipe ici.")
    
    # Partage de documents
    share_with = st_tags(
        label="Partagez avec",
        text="Appuyez sur entrée pour ajouter un email",
        value=[],
        suggestions=["user1@example.com", "user2@example.com"]
    )
    if st.button("Partager"):
        st.write(f"Documents partagés avec : {', '.join(share_with)}")
        
    # Ajout de commentaires
    st.text_area("Ajoutez un commentaire")

# Fonctionnalité de sécurité
elif section == "🔒 Sécurité":
    add_bg_image()
    st.header("Sécurité et Confidentialité")
    st.write("Gérez les paramètres de sécurité et les permissions d'accès.")
    
    # Gestion des permissions
    user_permissions = st.selectbox("Choisissez un utilisateur", ["User 1", "User 2", "User 3"])
    permission_level = st.radio("Niveau de permission", ["Lecture", "Écriture", "Admin"])
    if st.button("Mettre à jour les permissions"):
        st.write(f"Permissions de {user_permissions} mises à jour vers {permission_level}.")

# Fonctionnalité d'intégration
elif section == "🔗 Intégration":
    add_bg_image()
    st.header("Intégration et Accessibilité")
    st.write("Intégrez Atlantis BCI avec d'autres outils et applications.")
    
    # Sélection d'outils à intégrer
    tools = st.multiselect("Choisissez les outils à intégrer", ["Google Drive", "Dropbox", "OneDrive", "Slack"])
    if st.button("Intégrer"):
        st.write(f"Outils intégrés : {', '.join(tools)}")

# Fonctionnalité de gestion de profil utilisateur
elif section == "👤 Profil Utilisateur":
    add_bg_image()
    st.header("Gestion de Profil Utilisateur")
    
    # Champs du profil utilisateur
    st.subheader("Informations du Profil")
    username = st.text_input("Nom d'utilisateur", "johndoe")
    email = st.text_input("Email", "johndoe@example.com")
    bio = st.text_area("Bio", "Développeur passionné par les technologies de l'information et de la communication.")
    
    if st.button("Mettre à jour le profil"):
        st.write("Profil mis à jour avec succès!")
    
    # Afficher les informations du profil
    st.subheader("Votre Profil")
    st.write(f"**Nom d'utilisateur** : {username}")
    st.write(f"**Email** : {email}")
    st.write(f"**Bio** : {bio}")
