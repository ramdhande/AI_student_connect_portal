# Premium Local Translation Engine for Regional Accessibility

DICTIONARY = {
    "hindi": {
        "Academic": "शैक्षणिक",
        "Events": "आयोजन",
        "Placement": "प्लेसमेंट",
        "Emergency": "आपातकालीन",
        "Administrative": "प्रशासनिक",
        "Notice Board": "सूचना पट्ट",
        "AI Based Student Connect Portal": "एआई-आधारित छात्र कनेक्ट पोर्टल",
        "Student Dashboard": "छात्र डैशबोर्ड",
        "Grievances": "शिकायतें",
        "Submit Grievance": "शिकायत दर्ज करें",
        "Chatbot": "चैटबॉट",
        "Hello! How can I help you today?": "नमस्ते! आज मैं आपकी क्या सहायता कर सकता हूँ?",
        "Please contact the college administration office.": "कृपया कॉलेज प्रशासन कार्यालय से संपर्क करें।"
    },
    "marathi": {
        "Academic": "शैक्षणिक",
        "Events": "कार्यक्रम",
        "Placement": "प्लेसमेंट",
        "Emergency": "कणीक/आणीबाणी",
        "Administrative": "प्रशासकीय",
        "Notice Board": "सूचना फलक",
        "AI Based Student Connect Portal": "एआय-आधारित विद्यार्थी कनेक्ट पोर्टल",
        "Student Dashboard": "विद्यार्थी डॅशबोर्ड",
        "Grievances": "तक्रारी",
        "Submit Grievance": "तक्रार दाखल करा",
        "Chatbot": "चॅटबॉट"
    },
    "spanish": {
        "Academic": "Académico",
        "Events": "Eventos",
        "Placement": "Reclutamiento",
        "Emergency": "Emergencia",
        "Administrative": "Administrativo",
        "Notice Board": "Tablón de Anuncios",
        "AI Based Student Connect Portal": "Portal de Conexión de Estudiantes IA",
        "Student Dashboard": "Panel del Estudiante",
        "Grievances": "Quejas",
        "Submit Grievance": "Presentar Queja",
        "Chatbot": "Asistente de Chat"
    }
}

# Standard English sentence mappings for college portal notices to Hindi/Marathi/Spanish
SENTENCE_MAPPINGS = {
    "hindi": {
        "Final Year Exams will commence from June 15. Attendance must be above 75%.": "अंतिम वर्ष की परीक्षाएं 15 जून से शुरू होंगी। उपस्थिति 75% से अधिक होनी चाहिए।",
        "Wipro recruitment drive is scheduled for next Monday. Register on portal immediately.": "विप्रो भर्ती अभियान अगले सोमवार को निर्धारित है। पोर्टल पर तुरंत पंजीकरण करें।",
        "Annual College Cultural Fest 'Tarang 2026' starts from June 1st. Registrations open!": "वार्षिक कॉलेज सांस्कृतिक उत्सव 'तरंग 2026' 1 जून से शुरू हो रहा है। पंजीकरण खुले हैं!",
        "Severe rainfall alert. College will remain closed tomorrow. Online classes scheduled.": "भारी बारिश की चेतावनी। कॉलेज कल बंद रहेगा। ऑनलाइन कक्षाएं निर्धारित हैं।",
        "All students must complete their fee clearance by the end of this week.": "सभी छात्रों को इस सप्ताह के अंत तक अपना शुल्क भुगतान पूरा करना होगा।"
    },
    "marathi": {
        "Final Year Exams will commence from June 15. Attendance must be above 75%.": "अंतिम वर्षाच्या परीक्षा 15 जूनपासून सुरू होतील. उपस्थिती 75% च्या वर असणे आवश्यक आहे.",
        "Wipro recruitment drive is scheduled for next Monday. Register on portal immediately.": "विप्रो भरती मोहीम पुढील सोमवारी नियोजित आहे. पोर्टलवर त्वरित नोंदणी करा.",
        "Annual College Cultural Fest 'Tarang 2026' starts from June 1st. Registrations open!": "वार्षिक कॉलेज सांस्कृतिक उत्सव 'तरंग 2026' 1 जूनपासून सुरू होत आहे. नोंदणी सुरू आहे!",
        "Severe rainfall alert. College will remain closed tomorrow. Online classes scheduled.": "मुसळधार पावसाचा इशारा. कॉलेज उद्या बंद राहील. ऑनलाइन वर्ग आयोजित केले आहेत.",
        "All students must complete their fee clearance by the end of this week.": "सर्व विद्यार्थ्यांनी या आठवड्याच्या शेवटीपर्यंत आपली फी थकबाकी पूर्ण करावी."
    },
    "spanish": {
        "Final Year Exams will commence from June 15. Attendance must be above 75%.": "Los exámenes de último año comenzarán a partir del 15 de junio. La asistencia debe ser superior al 75%.",
        "Wipro recruitment drive is scheduled for next Monday. Register on portal immediately.": "La campaña de reclutamiento de Wipro está programada para el próximo lunes. Regístrese en el portal de inmediato.",
        "Annual College Cultural Fest 'Tarang 2026' starts from June 1st. Registrations open!": "El festival cultural anual del colegio 'Tarang 2026' comienza el 1 de junio. ¡Inscripciones abiertas!",
        "Severe rainfall alert. College will remain closed tomorrow. Online classes scheduled.": "Alerta de fuertes lluvias. El colegio permanecerá cerrado mañana. Clases en línea programadas.",
        "All students must complete their fee clearance by the end of this week.": "Todos los estudiantes deben completar su liquidación de matrícula antes del final de esta semana."
    }
}

import urllib.request
import urllib.parse
import json

def translate_text(text, target_lang):
    target_lang = target_lang.lower().strip()
    
    # 1. Direct sentence match check from local mapping cache
    if target_lang in SENTENCE_MAPPINGS and text in SENTENCE_MAPPINGS[target_lang]:
        return SENTENCE_MAPPINGS[target_lang][text]

    # 2. Dynamic API Translation using public MyMemory Translation API
    try:
        lang_pairs = {
            'hindi': 'en|hi',
            'marathi': 'en|mr',
            'spanish': 'en|es'
        }
        if target_lang in lang_pairs:
            langpair = lang_pairs[target_lang]
            url = "https://api.mymemory.translated.net/get?q=" + urllib.parse.quote(text) + "&langpair=" + langpair
            
            req = urllib.request.Request(
                url, 
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            
            with urllib.request.urlopen(req, timeout=4) as response:
                data = json.loads(response.read().decode('utf-8'))
                translated = data.get('responseData', {}).get('translatedText', '')
                if translated:
                    return translated
    except Exception as e:
        # Silently fail and fall back to dictionary matching
        pass

    # 3. Partial / word replacement local dictionary fallback
    if target_lang not in DICTIONARY:
        return text

    words = text.split()
    translated_words = []
    for w in words:
        cleaned = w.strip(".,!?\"'")
        if cleaned in DICTIONARY[target_lang]:
            translated_words.append(w.replace(cleaned, DICTIONARY[target_lang][cleaned]))
        else:
            translated_words.append(w)

    return " ".join(translated_words)
