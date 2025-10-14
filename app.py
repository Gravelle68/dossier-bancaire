import streamlit as st
import os
import tempfile
import shutil
from PIL import Image
import fitz  # PyMuPDF
import cv2
import numpy as np
from datetime import datetime
import io

# Configuration
st.set_page_config(
    page_title="Générateur Dossier Bancaire",
    page_icon="📁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS simplifié
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        padding: 0.75rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Catégories
CATEGORIES = {
    "IDENTITÉ": [
        "Carte d'identité (recto-verso)",
        "Livret de famille",
        "Acte de naissance"
    ],
    "DOMICILE": [
        "Justificatif de domicile récent (-3 mois)",
        "Taxe foncière (si propriétaire)",
        "Quittance de loyer (si locataire)"
    ],
    "REVENUS": [
        "3 derniers bulletins de salaire",
        "Contrat de travail",
        "Attestation employeur",
        "Avis d'imposition N-1",
        "Avis d'imposition N-2"
    ],
    "COMPTES BANCAIRES": [
        "3 derniers relevés compte courant",
        "3 derniers relevés livret A/épargne",
        "Attestation de prêts en cours"
    ],
    "PROJET IMMOBILIER": [
        "Compromis de vente",
        "Estimation du bien",
        "Plan de financement",
        "Devis travaux (si applicable)"
    ],
    "AUTRES DOCUMENTS": [
        "Justificatifs autres revenus",
        "Attestation assurance",
        "Documents spécifiques banque"
    ]
}

# Initialisation session state
if 'documents' not in st.session_state:
    st.session_state.documents = {cat: {doc: [] for doc in docs} for cat, docs in CATEGORIES.items()}

if 'temp_dir' not in st.session_state:
    st.session_state.temp_dir = tempfile.mkdtemp()

if 'info_garde' not in st.session_state:
    st.session_state.info_garde = {
        'porteur_projet': '',
        'type_bien': '',
        'localisation': '',
        'montant_sollicite': '',
        'date': datetime.now().strftime('%d/%m/%Y')
    }

if 'presentation_projet' not in st.session_state:
    st.session_state.presentation_projet = {
        'description': '',
        'surface': '',
        'prix_acquisition': '',
        'apport_personnel': '',
        'montant_emprunte': '',
        'duree_souhaitee': '',
        'revenus_mensuels': '',
        'charges_mensuelles': ''
    }

if 'selected_category' not in st.session_state:
    st.session_state.selected_category = None
if 'selected_doc_type' not in st.session_state:
    st.session_state.selected_doc_type = None

# Traitement carte d'identité
def traiter_carte_identite(chemin_image, nom_affichage):
    try:
        img = cv2.imread(chemin_image)
        if img is None:
            return chemin_image
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        gray = clahe.apply(gray)
        
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        cartes_detectees = []
        for contour in contours:
            epsilon = 0.02 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            
            if len(approx) == 4:
                area = cv2.contourArea(contour)
                if area > 50000:
                    x, y, w, h = cv2.boundingRect(contour)
                    ratio = w / h if w > h else h / w
                    if 1.4 <= ratio <= 1.8:
                        cartes_detectees.append((x, y, w, h, area))
        
        cartes_detectees.sort(key=lambda x: x[4], reverse=True)
        
        if len(cartes_detectees) >= 1:
            return creer_page_carte_identite(img, cartes_detectees, nom_affichage)
    except:
        pass
    
    return chemin_image

def creer_page_carte_identite(img_originale, cartes_detectees, nom_affichage):
    try:
        page_width, page_height = 2480, 3508
        page = np.ones((page_height, page_width, 3), dtype=np.uint8) * 255
        
        carte_width, carte_height = 800, 500
        
        if len(cartes_detectees) == 1:
            positions = [(page_width//2 - carte_width//2, page_height//2 - carte_height//2)]
        else:
            y_top = page_height//3 - carte_height//2
            y_bottom = 2*page_height//3 - carte_height//2
            x_center = page_width//2 - carte_width//2
            positions = [(x_center, y_top), (x_center, y_bottom)]
        
        for i, (carte_info, position) in enumerate(zip(cartes_detectees[:2], positions)):
            x, y, w, h, _ = carte_info
            pos_x, pos_y = position
            
            carte = img_originale[y:y+h, x:x+w]
            carte_resized = cv2.resize(carte, (carte_width, carte_height))
            carte_resized = cv2.bilateralFilter(carte_resized, 9, 75, 75)
            
            if pos_y + carte_height <= page_height and pos_x + carte_width <= page_width:
                page[pos_y:pos_y+carte_height, pos_x:pos_x+carte_width] = carte_resized
                
                label = "RECTO" if i == 0 else "VERSO"
                cv2.putText(page, label, (pos_x, pos_y-20), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        
        nouveau_chemin = os.path.join(st.session_state.temp_dir, f"carte_id_traitee_{nom_affichage}.jpg")
        cv2.imwrite(nouveau_chemin, page, [cv2.IMWRITE_JPEG_QUALITY, 95])
        
        return nouveau_chemin
    except:
        return None

# Génération PDF
def generer_pdf_complet(info_garde, presentation_projet):
    doc = fitz.open()
    
    # PAGE DE GARDE MODERNE
    page_garde = doc.new_page()
    
    # Fond gris dégradé
    page_garde.draw_rect(fitz.Rect(0, 0, 595, 842), color=(0.86, 0.86, 0.86), fill=(0.86, 0.86, 0.86))
    
    # Forme géométrique 1 (bas droite)
    page_garde.draw_quad(fitz.Quad(
        fitz.Point(300, 500),
        fitz.Point(650, 450),
        fitz.Point(650, 900),
        fitz.Point(200, 900)
    ), color=(0.75, 0.75, 0.75), fill=(0.75, 0.75, 0.75), overlay=False)
    
    # Ligne d'accent
    page_garde.draw_rect(fitz.Rect(0, 295, 270, 298), color=(0.17, 0.24, 0.31), fill=(0.17, 0.24, 0.31))
    
    # Titre principal
    page_garde.insert_text((60, 140), "DEMANDE DE",
                          fontsize=46, fontname="Helvetica-Bold", color=(0.1, 0.1, 0.1))
    page_garde.insert_text((60, 190), "FINANCEMENT",
                          fontsize=46, fontname="Helvetica-Bold", color=(0.1, 0.1, 0.1))
    
    page_garde.insert_text((60, 235), "Projet Immobilier",
                          fontsize=22, fontname="Helvetica", color=(0.16, 0.16, 0.16))
    
    # Informations structurées
    y_start = 450
    line_height = 50
    
    infos = [
        ("Porteur du projet", info_garde.get('porteur_projet', '[Non renseigné]')),
        ("Type de bien", info_garde.get('type_bien', '[Non renseigné]')),
        ("Localisation", info_garde.get('localisation', '[Non renseigné]')),
        ("Montant sollicité", info_garde.get('montant_sollicite', '[Non renseigné]')),
        ("Date", info_garde.get('date', datetime.now().strftime('%d/%m/%Y')))
    ]
    
    for i, (label, value) in enumerate(infos):
        y_pos = y_start + i * line_height
        
        page_garde.insert_text((60, y_pos), label,
                              fontsize=11, fontname="Helvetica-Bold", color=(0.1, 0.1, 0.1))
        
        page_garde.draw_line(fitz.Point(240, y_pos + 5), fitz.Point(520, y_pos + 5),
                            color=(0, 0, 0), width=0.5)
        
        page_garde.insert_text((240, y_pos), value,
                              fontsize=12, fontname="Helvetica", color=(0.23, 0.23, 0.23))
    
    page_garde.insert_text((420, 810), "DOCUMENT CONFIDENTIEL",
                          fontsize=8, fontname="Helvetica", color=(0.4, 0.4, 0.4))
    
    # PAGE PRÉSENTATION DU PROJET
    page_presentation = doc.new_page()
    
    # En-tête minimaliste
    page_presentation.draw_rect(fitz.Rect(0, 0, 595, 100), color=(0.17, 0.24, 0.31), fill=(0.17, 0.24, 0.31))
    page_presentation.insert_text((50, 55), "PRESENTATION DU PROJET",
                                 fontsize=28, fontname="Helvetica-Bold", color=(1, 1, 1))
    
    y_pos = 140
    
    # Description du projet
    if presentation_projet.get('description'):
        page_presentation.insert_text((50, y_pos), "Description du projet",
                                     fontsize=14, fontname="Helvetica-Bold", color=(0.17, 0.24, 0.31))
        y_pos += 25
        
        desc = presentation_projet['description']
        words = desc.split()
        lines = []
        current_line = []
        max_chars = 85
        
        for word in words:
            test_line = " ".join(current_line + [word])
            if len(test_line) > max_chars:
                if current_line:
                    lines.append(" ".join(current_line))
                    current_line = [word]
            else:
                current_line.append(word)
        if current_line:
            lines.append(" ".join(current_line))
        
        for line in lines[:6]:
            page_presentation.insert_text((50, y_pos), line,
                                        fontsize=11, fontname="Helvetica", color=(0.2, 0.2, 0.2))
            y_pos += 18
        
        y_pos += 30
    
    # Tableau des chiffres clés
    page_presentation.draw_rect(fitz.Rect(50, y_pos, 545, y_pos + 35), 
                               color=(0.17, 0.24, 0.31), fill=(0.17, 0.24, 0.31))
    page_presentation.insert_text((60, y_pos + 22), "CHIFFRES CLES",
                                 fontsize=13, fontname="Helvetica-Bold", color=(1, 1, 1))
    
    y_pos += 55
    
    chiffres = [
        ("Surface", presentation_projet.get('surface', '—')),
        ("Prix d'acquisition", presentation_projet.get('prix_acquisition', '—')),
        ("Apport personnel", presentation_projet.get('apport_personnel', '—')),
        ("Montant emprunté", presentation_projet.get('montant_emprunte', '—')),
        ("Durée souhaitée", presentation_projet.get('duree_souhaitee', '—')),
        ("Revenus mensuels nets", presentation_projet.get('revenus_mensuels', '—')),
        ("Charges mensuelles", presentation_projet.get('charges_mensuelles', '—'))
    ]
    
    for i, (label, value) in enumerate(chiffres):
        if i % 2 == 0:
            page_presentation.draw_rect(fitz.Rect(50, y_pos - 5, 545, y_pos + 20),
                                       color=(0.95, 0.95, 0.95), fill=(0.95, 0.95, 0.95))
        
        page_presentation.insert_text((60, y_pos + 12), label,
                                     fontsize=11, fontname="Helvetica-Bold", color=(0.2, 0.2, 0.2))
        page_presentation.insert_text((320, y_pos + 12), value,
                                     fontsize=11, fontname="Helvetica", color=(0.3, 0.3, 0.3))
        
        y_pos += 35
    
    page_numbers = {}
    current_page = 2
    
    # DOCUMENTS
    for category, docs in st.session_state.documents.items():
        if not any(docs.values()):
            continue
        
        intercalaire = doc.new_page()
        current_page += 1
        page_numbers[category] = current_page - 1
        
        # Style minimaliste
        intercalaire.draw_rect(fitz.Rect(0, 0, 595, 120), 
                            color=(0.17, 0.24, 0.31), fill=(0.17, 0.24, 0.31))
        
        intercalaire.insert_text((50, 70), category,
                                fontsize=32, fontname="Helvetica-Bold", color=(1, 1, 1))
        
        files_in_category = sum(len(files) for files in docs.values())
        intercalaire.insert_text((50, 100), 
                                f"{files_in_category} document{'s' if files_in_category > 1 else ''}",
                                fontsize=13, fontname="Helvetica", color=(0.85, 0.85, 0.85))
        
        y_pos = 170
        file_num = 1
        
        for doc_type, doc_files in docs.items():
            for file_index, doc_info in enumerate(doc_files):
                if file_num % 2 == 0:
                    intercalaire.draw_rect(fitz.Rect(50, y_pos-8, 545, y_pos+18),
                                        color=(0.96, 0.96, 0.96), fill=(0.96, 0.96, 0.96))
                
                intercalaire.insert_text((65, y_pos), 
                                        f"{file_num}. {doc_info['nom_affichage']}",
                                        fontsize=11, fontname="Helvetica", color=(0.2, 0.2, 0.2))
                
                y_pos += 26
                file_num += 1
        
        for doc_type, doc_files in docs.items():
            for file_index, doc_info in enumerate(doc_files):
                page_key = f"{category}_{doc_type}_{file_index}"
                
                if doc_info['type_fichier'] == 'PDF':
                    try:
                        pdf_source = fitz.open(doc_info['chemin'])
                        if pdf_source and pdf_source.page_count > 0:
                            page_numbers[page_key] = current_page
                            
                            for page_num in range(pdf_source.page_count):
                                nouvelle_page = doc.new_page()
                                current_page += 1
                                
                                nouvelle_page.draw_rect(fitz.Rect(0, 0, 595, 40), 
                                                    color=(0.95, 0.95, 0.95), fill=(0.95, 0.95, 0.95))
                                nouvelle_page.insert_text((15, 25), f"{category} - {doc_info['nom_affichage']}",
                                                        fontsize=11, fontname="Helvetica-Bold", color=(0.17, 0.24, 0.31))
                                
                                if pdf_source.page_count > 1:
                                    nouvelle_page.insert_text((500, 25), f"{page_num + 1}/{pdf_source.page_count}",
                                                            fontsize=9, fontname="Helvetica", color=(0.5, 0.5, 0.5))
                                
                                nouvelle_page.show_pdf_page(fitz.Rect(15, 50, 580, 792), pdf_source, page_num)
                            
                            pdf_source.close()
                    except:
                        pass
                else:
                    try:
                        page_numbers[page_key] = current_page
                        
                        page = doc.new_page()
                        current_page += 1
                        
                        page.draw_rect(fitz.Rect(0, 0, 595, 40), 
                                    color=(0.95, 0.95, 0.95), fill=(0.95, 0.95, 0.95))
                        page.insert_text((15, 25), f"{category} - {doc_info['nom_affichage']}",
                                    fontsize=11, fontname="Helvetica-Bold", color=(0.17, 0.24, 0.31))
                        
                        if os.path.exists(doc_info['chemin']):
                            page.insert_image(fitz.Rect(15, 50, 580, 792), 
                                            filename=doc_info['chemin'], keep_proportion=True)
                    except:
                        pass
    
    # SOMMAIRE
    sommaire_page = doc.new_page(pno=1)
    
    for key in page_numbers:
        page_numbers[key] += 1
    
    sommaire_page.draw_rect(fitz.Rect(0, 0, 595, 120), 
                        color=(0.17, 0.24, 0.31), fill=(0.17, 0.24, 0.31))
    sommaire_page.insert_text((50, 70), "SOMMAIRE",
                            fontsize=32, fontname="Helvetica-Bold", color=(1, 1, 1))
    
    y_position = 160
    
    # Lien vers présentation
    rect_pres = fitz.Rect(50, y_position-6, 470, y_position+18)
    lien_pres = {
        "kind": fitz.LINK_GOTO,
        "page": 1,
        "to": fitz.Point(50, 100),
        "from": rect_pres
    }
    sommaire_page.insert_link(lien_pres)
    
    sommaire_page.insert_text((60, y_position), "PRESENTATION DU PROJET",
                            fontsize=13, fontname="Helvetica-Bold", color=(0.17, 0.24, 0.31))
    sommaire_page.insert_text((500, y_position), "p.2",
                            fontsize=11, fontname="Helvetica", color=(0.4, 0.4, 0.4))
    
    y_position += 35
    
    for category, docs in st.session_state.documents.items():
        if any(docs.values()):
            rect_cat = fitz.Rect(50, y_position-6, 470, y_position+18)
            lien_cat = {
                "kind": fitz.LINK_GOTO,
                "page": page_numbers[category],
                "to": fitz.Point(50, 100),
                "from": rect_cat
            }
            sommaire_page.insert_link(lien_cat)
            
            sommaire_page.insert_text((60, y_position), category,
                                    fontsize=13, fontname="Helvetica-Bold", color=(0.17, 0.24, 0.31))
            sommaire_page.insert_text((500, y_position), f"p.{page_numbers[category]}",
                                    fontsize=11, fontname="Helvetica", color=(0.4, 0.4, 0.4))
            
            y_position += 28
            
            for doc_type, doc_files in docs.items():
                for file_index, doc_info in enumerate(doc_files):
                    page_key = f"{category}_{doc_type}_{file_index}"
                    
                    if page_key in page_numbers:
                        rect_doc = fitz.Rect(80, y_position-5, 480, y_position+14)
                        lien_doc = {
                            "kind": fitz.LINK_GOTO,
                            "page": page_numbers[page_key],
                            "to": fitz.Point(50, 100),
                            "from": rect_doc
                        }
                        sommaire_page.insert_link(lien_doc)
                        
                        sommaire_page.insert_text((90, y_position), 
                                                f"{doc_info['nom_affichage']}",
                                                fontsize=10, fontname="Helvetica", color=(0.3, 0.3, 0.3))
                        
                        sommaire_page.insert_text((505, y_position), f"p.{page_numbers[page_key]}",
                                                fontsize=9, fontname="Helvetica", color=(0.6, 0.6, 0.6))
                    
                    y_position += 20
            
            y_position += 15
    
    pdf_bytes = doc.tobytes()
    doc.close()
    
    return pdf_bytes

# Header
st.title("📁 Générateur de Dossier Bancaire")
st.caption("Crédit Immobilier Professionnel")

# Progression
total_types = sum(len(docs) for docs in CATEGORIES.values())
total_files = sum(len(files) for cat in st.session_state.documents.values() for files in cat.values())
progress = int((total_files / total_types) * 100) if total_types > 0 else 0

col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    st.progress(progress / 100)
with col2:
    st.metric("Progression", f"{progress}%")
with col3:
    st.metric("Fichiers", total_files)

st.divider()

# Sidebar
with st.sidebar:
    st.header("🎨 Informations page de garde")
    
    st.session_state.info_garde['porteur_projet'] = st.text_input(
        "Porteur du projet",
        value=st.session_state.info_garde['porteur_projet'],
        placeholder="Nom complet"
    )
    
    st.session_state.info_garde['type_bien'] = st.text_input(
        "Type de bien",
        value=st.session_state.info_garde['type_bien'],
        placeholder="Appartement / Maison / Immeuble"
    )
    
    st.session_state.info_garde['localisation'] = st.text_input(
        "Localisation",
        value=st.session_state.info_garde['localisation'],
        placeholder="Ville, Département"
    )
    
    st.session_state.info_garde['montant_sollicite'] = st.text_input(
        "Montant sollicité",
        value=st.session_state.info_garde['montant_sollicite'],
        placeholder="XXX XXX €"
    )
    
    st.divider()
    
    st.header("📊 Présentation du projet")
    
    with st.expander("Description", expanded=False):
        st.session_state.presentation_projet['description'] = st.text_area(
            "Description détaillée",
            value=st.session_state.presentation_projet['description'],
            height=100,
            placeholder="Décrivez votre projet immobilier..."
        )
    
    with st.expander("Chiffres clés", expanded=False):
        st.session_state.presentation_projet['surface'] = st.text_input(
            "Surface",
            value=st.session_state.presentation_projet['surface'],
            placeholder="120 m²"
        )
        
        st.session_state.presentation_projet['prix_acquisition'] = st.text_input(
            "Prix d'acquisition",
            value=st.session_state.presentation_projet['prix_acquisition'],
            placeholder="350 000 €"
        )
        
        st.session_state.presentation_projet['apport_personnel'] = st.text_input(
            "Apport personnel",
            value=st.session_state.presentation_projet['apport_personnel'],
            placeholder="70 000 €"
        )
        
        st.session_state.presentation_projet['montant_emprunte'] = st.text_input(
            "Montant emprunté",
            value=st.session_state.presentation_projet['montant_emprunte'],
            placeholder="280 000 €"
        )
        
        st.session_state.presentation_projet['duree_souhaitee'] = st.text_input(
            "Durée souhaitée",
            value=st.session_state.presentation_projet['duree_souhaitee'],
            placeholder="25 ans"
        )
        
        st.session_state.presentation_projet['revenus_mensuels'] = st.text_input(
            "Revenus mensuels nets",
            value=st.session_state.presentation_projet['revenus_mensuels'],
            placeholder="5 500 €"
        )
        
        st.session_state.presentation_projet['charges_mensuelles'] = st.text_input(
            "Charges mensuelles",
            value=st.session_state.presentation_projet['charges_mensuelles'],
            placeholder="800 €"
        )
    
    st.divider()
    
    if total_files == 0:
        st.warning("Ajoutez des documents d'abord")
    else:
        if st.button("🚀 Générer le PDF", type="primary", use_container_width=True):
            with st.spinner("Génération en cours..."):
                try:
                    pdf_bytes = generer_pdf_complet(
                        st.session_state.info_garde,
                        st.session_state.presentation_projet
                    )
                    
                    st.download_button(
                        label="📥 Télécharger le PDF",
                        data=pdf_bytes,
                        file_name=f"dossier_bancaire_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                        mime="application/pdf",
                        type="primary",
                        use_container_width=True
                    )
                    st.success("PDF généré avec succès!")
                except Exception as e:
                    st.error(f"Erreur: {str(e)}")

# Layout principal
col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("📋 Documents requis")
    
    for category, doc_types in CATEGORIES.items():
        files_in_cat = sum(len(st.session_state.documents[category][dt]) for dt in doc_types)
        
        with st.expander(f"📂 **{category}** - {len(doc_types)} types ({files_in_cat} fichiers)", expanded=True):
            for doc_type in doc_types:
                files = st.session_state.documents[category][doc_type]
                
                col_doc, col_status, col_btn = st.columns([4, 1, 1])
                
                with col_doc:
                    if files:
                        st.markdown(f"**📄 {doc_type}**")
                    else:
                        st.markdown(f"📄 {doc_type}")
                
                with col_status:
                    if files:
                        st.success(f"✓ {len(files)}")
                    else:
                        st.warning("—")
                
                with col_btn:
                    if st.button("➕", key=f"select_{category}_{doc_type}", help="Ajouter un document"):
                        st.session_state.selected_category = category
                        st.session_state.selected_doc_type = doc_type
                        st.rerun()
                
                if files:
                    for i, doc_info in enumerate(files):
                        col_file, col_del = st.columns([5, 1])
                        with col_file:
                            st.caption(f"  └─ {doc_info['nom_affichage']}")
                        with col_del:
                            if st.button("🗑️", key=f"del_{category}_{doc_type}_{i}", help="Supprimer"):
                                st.session_state.documents[category][doc_type].pop(i)
                                st.rerun()

with col_right:
    st.subheader("➕ Ajouter un document")
    
    if st.session_state.selected_category and st.session_state.selected_doc_type:
        st.info(f"**Catégorie :** {st.session_state.selected_category}\n\n**Type :** {st.session_state.selected_doc_type}")
        
        uploaded_files = st.file_uploader(
            "Glissez-déposez un ou plusieurs fichiers",
            type=['pdf', 'jpg', 'jpeg', 'png', 'bmp', 'tiff'],
            accept_multiple_files=True,
            key="file_uploader",
            help="Vous pouvez sélectionner ou glisser-déposer plusieurs fichiers en même temps"
        )
        
        if uploaded_files:
            st.write(f"**{len(uploaded_files)} fichier(s) sélectionné(s)**")
            
            rename_mode = st.radio(
                "Mode de nommage",
                ["Garder les noms d'origine", "Renommer individuellement"],
                horizontal=True
            )
            
            if rename_mode == "Renommer individuellement":
                noms_affiches = []
                for i, uploaded_file in enumerate(uploaded_files):
                    nom = st.text_input(
                        f"Nom pour '{uploaded_file.name}'",
                        value=os.path.splitext(uploaded_file.name)[0],
                        key=f"rename_{i}"
                    )
                    noms_affiches.append(nom)
            else:
                noms_affiches = [os.path.splitext(f.name)[0] for f in uploaded_files]
            
            if st.button("✅ Ajouter tous les fichiers", type="primary", use_container_width=True):
                fichiers_ajoutes = 0
                
                for uploaded_file, nom_affichage in zip(uploaded_files, noms_affiches):
                    extension = os.path.splitext(uploaded_file.name)[1]
                    nouveau_nom = f"{st.session_state.selected_category}_{st.session_state.selected_doc_type}_{nom_affichage}{extension}"
                    chemin = os.path.join(st.session_state.temp_dir, nouveau_nom)
                    
                    with open(chemin, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    if "carte" in st.session_state.selected_doc_type.lower() and "identite" in st.session_state.selected_doc_type.lower() and extension.lower() in ['.jpg', '.jpeg', '.png']:
                        try:
                            chemin = traiter_carte_identite(chemin, nom_affichage)
                        except:
                            pass
                    
                    doc_info = {
                        'chemin': chemin,
                        'nom_affichage': nom_affichage,
                        'type_fichier': 'PDF' if extension.lower() == '.pdf' else 'Image'
                    }
                    
                    st.session_state.documents[st.session_state.selected_category][st.session_state.selected_doc_type].append(doc_info)
                    fichiers_ajoutes += 1
                
                st.success(f"✅ {fichiers_ajoutes} fichier(s) ajouté(s)!")
                
                st.session_state.selected_category = None
                st.session_state.selected_doc_type = None
                st.rerun()
        
        if st.button("❌ Annuler", use_container_width=True):
            st.session_state.selected_category = None
            st.session_state.selected_doc_type = None
            st.rerun()
    else:
        st.info("👈 Cliquez sur le bouton ➕ à côté d'un type de document pour commencer")

st.divider()
st.caption("Application web - Fonctionne sur tous les appareils")
                                