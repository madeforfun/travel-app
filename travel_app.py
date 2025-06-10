

import streamlit as st
import groq
import os
from datetime import datetime
import random
import time
import json

# Set page config with travel-friendly colors
st.set_page_config(
    page_title="Travel Budyy's French Coffee Trip",
    page_icon="🗼✈️",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "Made for our travel adventures together"
    }
)

# Custom CSS for travel theme
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        color: #2C3E50;
    }
    .main-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
    }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #FFF8F0;
        border: 2px solid #E8D5C4;
        border-radius: 15px;
    }
    .stButton>button {
        background: linear-gradient(45deg, #4e54c8, #8f94fb);
        color: white;
        border-radius: 25px;
        border: none;
        padding: 12px 30px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(78, 84, 200, 0.3);
    }
    .french-lesson {
        background: linear-gradient(45deg, #FFF8F0, #F8E8D8);
        border-left: 6px solid #4e54c8;
        padding: 1.5rem;
        margin: 1rem 0;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    .travel-note {
        background: linear-gradient(45deg, #E8F4FD, #D4E7FA);
        border: 2px solid #4e54c8;
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        position: relative;
    }
    .travel-header {
        text-align: center;
        background: linear-gradient(45deg, #4e54c8, #8f94fb);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .coffee-counter {
        background: linear-gradient(45deg, #8B4513, #D2691E);
        color: white;
        padding: 1rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
    }
    .progress-globe {
        color: #4e54c8;
        font-size: 24px;
    }
    .tab-content {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin-top: 1rem;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    .country-card {
        background: white;
        border-radius: 15px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 3px 10px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    .country-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    .flag-emoji {
        font-size: 2rem;
        margin-right: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Groq client
try:
    client = groq.Client(api_key="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")
    groq_available = True
except:
    groq_available = False
    st.warning("🌟 Groq API not available - using demo mode for now!")

# Static French travel phrases database (enhanced for travelers)
STATIC_TRAVEL_PHRASES = {
    "Greetings & Politeness": {
        "Bonjour": "Hello (Good day)",
        "Bonsoir": "Good evening", 
        "Salut": "Hi/Bye (casual)",
        "Excusez-moi": "Excuse me",
        "S'il vous plaît": "Please",
        "Merci beaucoup": "Thank you very much",
        "De rien": "You're welcome",
        "Pardon": "Sorry",
        "Comment allez-vous?": "How are you?",
        "Enchanté(e)": "Nice to meet you"
    },
    "Coffee & Food Adventures": {
        "Un café, s'il vous plaît": "A coffee, please",
        "Deux cafés": "Two coffees (for us!)",
        "L'addition, s'il vous plaît": "The bill, please",
        "C'est délicieux": "It's delicious",
        "Qu'est-ce que vous recommandez?": "What do you recommend?",
        "Je voudrais...": "I would like...",
        "Avez-vous du lait d'avoine?": "Do you have oat milk?",
        "Un croissant pour partager": "A croissant to share",
        "Nous prenons notre temps": "We're taking our time",
        "C'est pour emporter": "To take away"
    },
    "Navigation & Travel": {
        "Où est...?": "Where is...?",
        "Comment aller à...?": "How to get to...?",
        "À droite": "To the right",
        "À gauche": "To the left",
        "Tout droit": "Straight ahead",
        "La gare": "The train station",
        "L'aéroport": "The airport",
        "L'hôtel": "The hotel",
        "Nous sommes perdus": "We are lost (together!)",
        "C'est loin d'ici?": "Is it far from here?",
        "Un billet pour deux, s'il vous plaît": "One ticket for two, please"
    },
    "Shopping & Transactions": {
        "Combien ça coûte?": "How much does it cost?",
        "Je peux payer par carte?": "Can I pay by card?",
        "C'est trop cher": "It's too expensive",
        "Je prends ça": "I'll take this",
        "Avez-vous une taille plus grande?": "Do you have a bigger size?",
        "Je regarde juste": "I'm just looking",
        "Où sont les cabines d'essayage?": "Where are the fitting rooms?",
        "C'est un cadeau": "It's a gift"
    },
    "Emergencies & Help": {
        "Au secours!": "Help!",
        "Appelez la police": "Call the police",
        "J'ai besoin d'un médecin": "I need a doctor",
        "Où est l'hôpital?": "Where is the hospital?",
        "J'ai perdu mon passeport": "I lost my passport",
        "Pouvez-vous m'aider?": "Can you help me?",
        "Je ne me sens pas bien": "I don't feel well"
    }
}

# Dynamic phrase generation themes (travel-focused)
DYNAMIC_THEMES = [
    "Airport & Transportation",
    "Hotel & Accommodation", 
    "Restaurant & Dining",
    "Shopping & Markets",
    "Sightseeing & Tours",
    "Nightlife & Entertainment",
    "Public Transport",
    "Making Friends",
    "Photography Spots",
    "Local Customs",
    "Weather Conversations",
    "Hiking & Nature",
    "Beach & Swimming",
    "Museums & Culture",
    "Festivals & Events"
]

# Beautiful countries to visit (with emoji flags)
BEAUTIFUL_COUNTRIES = {
    "Europe": {
        "🇫🇷 France": ["Paris", "Nice", "Provence", "French Alps"],
        "🇮🇹 Italy": ["Rome", "Venice", "Florence", "Amalfi Coast"],
        "🇪🇸 Spain": ["Barcelona", "Madrid", "Seville", "Ibiza"],
        "🇬🇷 Greece": ["Athens", "Santorini", "Mykonos", "Crete"],
        "🇵🇹 Portugal": ["Lisbon", "Porto", "Algarve", "Madeira"],
        "🇨🇭 Switzerland": ["Zurich", "Geneva", "Interlaken", "Zermatt"],
        "🇳🇱 Netherlands": ["Amsterdam", "Rotterdam", "Keukenhof", "Giethoorn"],
        "🇦🇹 Austria": ["Vienna", "Salzburg", "Innsbruck", "Hallstatt"],
        "🇭🇷 Croatia": ["Dubrovnik", "Split", "Hvar", "Plitvice Lakes"],
        "🇳🇴 Norway": ["Oslo", "Bergen", "Fjords", "Tromsø"]
    },
    "World": {
        "🇯🇵 Japan": ["Tokyo", "Kyoto", "Osaka", "Hokkaido"],
        "🇨🇦 Canada": ["Vancouver", "Toronto", "Montreal", "Banff"],
        "🇳🇿 New Zealand": ["Auckland", "Queenstown", "Rotorua", "Fiordland"],
        "🇦🇺 Australia": ["Sydney", "Melbourne", "Gold Coast", "Great Barrier Reef"],
        "🇺🇸 USA": ["New York", "Los Angeles", "Las Vegas", "Grand Canyon"],
        "🇹🇭 Thailand": ["Bangkok", "Phuket", "Chiang Mai", "Krabi"],
        "🇮🇸 Iceland": ["Reykjavik", "Blue Lagoon", "Golden Circle", "Northern Lights"],
        "🇧🇷 Brazil": ["Rio de Janeiro", "São Paulo", "Iguazu Falls", "Amazon"],
        "🇿🇦 South Africa": ["Cape Town", "Johannesburg", "Kruger Park", "Garden Route"],
        "🇲🇦 Morocco": ["Marrakech", "Casablanca", "Fes", "Sahara Desert"]
    }
}

def generate_dynamic_phrases(theme, count=5):
    """Generate dynamic French phrases for specific themes using AI"""
    if not groq_available:
        # Fallback phrases when AI is not available
        fallback_phrases = {
            f"Phrase {i+1}": f"A useful French phrase for {theme.lower()}"
            for i in range(count)
        }
        return fallback_phrases
    
    try:
        prompt = f"""
        Generate {count} essential French phrases for travelers related to "{theme}".
        
        Format as JSON-like structure:
        "French phrase": "English translation"
        
        Focus on:
        1. Practical phrases Himanshu and Anastasiya would actually use
        2. Common situations they might encounter
        3. Keep translations clear and helpful
        4. They are good best friends who recently becames friends and they are so alike 
        5. She has promised to yake him out for a cofee in every country they both travel together
        6. Make this fun learning experience experience, playful but not much romantic as they are still friends, impress her
        7. she likes pink roses and tulips more
        8. mention them as travel buddies and friendsn snf svoid mentioning them as best friends or besties .

        
        Make them authentic and useful for real travel situations.
        Only return the phrases, no extra text.
        """
        
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-70b-8192",
            temperature=0.7
        )
        
        # Parse the response to extract phrases
        content = response.choices[0].message.content
        phrases = {}
        
        # Simple parsing - look for quoted phrases
        lines = content.split('\n')
        for line in lines:
            if ':' in line and '"' in line:
                try:
                    # Extract French phrase and English translation
                    parts = line.split(':', 1)
                    if len(parts) == 2:
                        french = parts[0].strip().strip('"').strip("'")
                        english = parts[1].strip().strip('"').strip("'")
                        if french and english:
                            phrases[french] = english
                except:
                    continue
        
        # If parsing failed, create some default phrases
        if not phrases:
            themes_map = {
                "Airport & Transportation": {
                    "Où est le comptoir d'enregistrement?": "Where is the check-in counter?",
                    "Notre vol est à quelle heure?": "What time is our flight?",
                    "Où puis-je récupérer mes bagages?": "Where can I collect my luggage?",
                    "Je voudrais changer de siège": "I'd like to change seats",
                    "Où est la sortie?": "Where is the exit?"
                },
                "Hotel & Accommodation": {
                    "Nous avons une réservation": "We have a reservation",
                    "Où est la piscine?": "Where is the pool?",
                    "À quelle heure est le petit déjeuner?": "What time is breakfast?",
                    "La clé ne fonctionne pas": "The key doesn't work",
                    "Nous restons deux nuits": "We're staying two nights"
                }
            }
            phrases = themes_map.get(theme, {f"Phrase {i+1}": f"Useful for {theme}" for i in range(count)})
        
        return phrases
        
    except Exception as e:
        # Fallback on error
        return {f"Phrase {i+1}": f"A useful French phrase for {theme.lower()}" for i in range(count)}

def get_combined_phrases():
    """Combine static and dynamic phrases"""
    combined = STATIC_TRAVEL_PHRASES.copy()
    
    # Add dynamic phrases from session state
    if "dynamic_phrases" in st.session_state:
        for theme, phrases in st.session_state.dynamic_phrases.items():
            combined[f"🌟 {theme}"] = phrases
    
    return combined

# Inside jokes and memories
INSIDE_JOKES = [
    "Remember: Coffee in every second country! ☕",
    " Lets get lost to find cool places! ✨",
    "Our travel dreams are coming true! 🌍",
    "Two dreamers, infinite adventures! 💫",
    "From strangers to travel partners! 🤝",
    "Every coffee has a story! ✨ "
]

# Initialize session state
if "learned_phrases" not in st.session_state:
    st.session_state.learned_phrases = []
if "coffee_dates" not in st.session_state:
    st.session_state.coffee_dates = 0
if "countries_visited" not in st.session_state:
    st.session_state.countries_visited = ["India", "Russia"]
if "current_phrase" not in st.session_state:
    st.session_state.current_phrase = random.choice(list(STATIC_TRAVEL_PHRASES["Greetings & Politeness"].keys()))
if "messages" not in st.session_state:
    st.session_state.messages = []
if "travel_diary" not in st.session_state:
    st.session_state.travel_diary = []
if "dynamic_phrases" not in st.session_state:
    st.session_state.dynamic_phrases = {}
if "phrase_generation_count" not in st.session_state:
    st.session_state.phrase_generation_count = 0
if "selected_country" not in st.session_state:
    st.session_state.selected_country = None

# App header
st.markdown('<div class="main-container">', unsafe_allow_html=True)

st.markdown(f"""
<div class="travel-header">
       Travel Buddy's French Trip 🗼✈️
</div>
<div style="text-align: center; margin-bottom: 2rem;">
    <h3 style="color: #4e54c8;">Learn French Together for Your Travel Adventures</h3>
    <p style="color: #8f94fb;">"{random.choice(INSIDE_JOKES)}"</p>
    <div class="coffee-counter">
        ☕ Coffee Dates Planned: {st.session_state.coffee_dates} | Countries Visited: {len(st.session_state.countries_visited)} 
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar with travel progress
with st.sidebar:
    st.markdown(f"""
    <div style="text-align: center; background: linear-gradient(45deg, #E8F4FD, #D4E7FA); padding: 1rem; border-radius: 15px;">
        <h3 style="color:blue;">Our Travel Stats</h3>
        <p style="color:blue;"><span class="progress-globe">🌍</span> {len(st.session_state.learned_phrases)} French phrases mastered!</p>
        <p style="color:blue;">✈️ Next destination: Paris!</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Travel mood tracker
    travel_mood = st.radio("How excited are you for our trip?", 
                   ["🤩 Over the moon!", "😍 Can't wait!", "✈️ Ready to fly!", "☕ Craving coffee adventures", "🗼 Dreaming of Paris"],
                   index=0)
    
    st.markdown("---")
    
    # Add coffee date button
    if st.button("☕ Take Himanshu Out for Another coffe? "):
        st.session_state.coffee_dates += 1
        st.success(f"Coffee date #{st.session_state.coffee_dates} planned!")
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; font-size: small; background: linear-gradient(45deg, #4e54c8, #8f94fb); color: white; padding: 1rem; border-radius: 10px;">
        <p>Made for our travel adventures</p>
        <p>Two travelers, one journey ✈️</p>
    </div>
    """, unsafe_allow_html=True)

# Main content tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["🗺️ Travel Phrases", "🌟 Dynamic Learning", "☕ Coffee Time", "✈️ Next Destination", "💬 Practice Together", "📔 Travel Diary"])

with tab1:
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    st.markdown("### 🌍 Essential French for Travelers")
    st.markdown("*Master the core travel phrases first!*")
    
    # Category selector - only static phrases
    selected_category = st.selectbox("Choose a category:", list(STATIC_TRAVEL_PHRASES.keys()))
    
    col1, col2 = st.columns([1, 2])
    with col1:
        current_phrases = STATIC_TRAVEL_PHRASES[selected_category]
        phrase_key = st.selectbox("Pick a phrase:", list(current_phrases.keys()))
        st.markdown(f"## 🇫🇷 {phrase_key}")
        st.markdown(f"#### *{current_phrases[phrase_key]}*")
        
        # Pronunciation help
        if st.button("🔊 How to pronounce?"):
            pronunciation_guide = {
                "Bonjour": "bon-ZHOOR",
                "Merci beaucoup": "mer-SEE bo-KOO",
                "S'il vous plaît": "see voo PLAY",
                "Un café, s'il vous plaît": "un ka-FAY see voo PLAY",
                "Excusez-moi": "ek-skew-ZAY mwah",
                "Où est...?": "oo-AY",
                "C'est délicieux": "say day-lee-see-UH"
            }
            if phrase_key in pronunciation_guide:
                st.info(f"🗣️ Pronunciation: {pronunciation_guide[phrase_key]}")
            else:
                st.info("🗣️ Practice with a French accent - try to sound natural!")
    
    with col2:
        if groq_available:
            try:
                prompt = f"""
                Explain the French phrase "{phrase_key}" meaning "{current_phrases[phrase_key]}" to Himanshu and Anastasiya who are learning French for their travel adventures.
                
                Include:
                1. When and where they might use this phrase while traveling
                2. Cultural context about using this in France
                3. A fun scenario where they might use it together
                4. Tips for pronunciation or usage
                5. They are good best friends who recently becames friends and they are so alike 
                6. She has promised to yake him out for a cofee in every country they both travel together
                7. Make this fun learning experience experience, playful but not much romantic as they are still friends, impress her
                8. she likes pink roses and tulips more
                9.mention them as travel buddies and friend and avoid mentioning them as best friends or besties .
                
                Make it travel-focused and mention their coffee dates tradition. Use emojis and keep it under 120 words.
                """
                
                response = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="llama3-70b-8192",
                    temperature=0.8
                )
                explanation = response.choices[0].message.content
            except:
                explanation = f"Perfect for your Paris adventure! You'll use '{phrase_key}' when ordering coffee together or exploring the city. Practice this phrase - it'll make your travels smoother! ☕🗼"
        else:
            explanation = f"Perfect for your Paris adventure! You'll use '{phrase_key}' when ordering coffee together or exploring the city. Practice this phrase - it'll make your travels smoother! ☕🗼"
        
        st.markdown(f'<div class="french-lesson">{explanation}</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("💾 Master this phrase!"):
            if phrase_key not in st.session_state.learned_phrases:
                st.session_state.learned_phrases.append(phrase_key)
                st.success(f"Added '{phrase_key}' to your travel vocabulary!")
            else:
                st.warning("You've already mastered this phrase! 🌟")
    
    with col2:
        if st.button("🎲 Surprise me!"):
            all_phrases = []
            for category in STATIC_TRAVEL_PHRASES.values():
                all_phrases.extend(list(category.keys()))
            st.session_state.current_phrase = random.choice(all_phrases)
            st.rerun()
    
    with col3:
        if st.button("🗼 Paris-ready phrases"):
            paris_phrases = ["Bonjour", "Un café, s'il vous plaît", "Excusez-moi", "Où est...?", "C'est délicieux"]
            selected_phrase = random.choice(paris_phrases)
            st.info(f"Paris essential: {selected_phrase}")
    
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    st.markdown("### 🌟 Dynamic Learning - Endless Adventures!")
    st.markdown("*Generate new phrases for any situation - learning never stops!*")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        selected_theme = st.selectbox("What do you want to explore today?", DYNAMIC_THEMES)
    with col2:
        phrase_count = st.slider("How many phrases?", 3, 10, 5)
    
    if st.button("🚀 Generate New Phrases!", use_container_width=True):
        with st.spinner(f"Creating amazing {selected_theme.lower()} phrases for your adventures..."):
            new_phrases = generate_dynamic_phrases(selected_theme, phrase_count)
            
            if selected_theme not in st.session_state.dynamic_phrases:
                st.session_state.dynamic_phrases[selected_theme] = {}
            
            # Merge new phrases with existing ones
            st.session_state.dynamic_phrases[selected_theme].update(new_phrases)
            st.session_state.phrase_generation_count += 1
            
            st.success(f"Generated {len(new_phrases)} new phrases for {selected_theme}! 🎉")
    
    # Display generated phrases
    if st.session_state.dynamic_phrases:
        st.markdown("---")
        st.markdown("### 📚 Your Dynamic Phrase Collection")
        
        theme_to_show = st.selectbox("Explore your generated themes:", 
                                   list(st.session_state.dynamic_phrases.keys()),
                                   key="dynamic_theme_selector")
        
        if theme_to_show:
            phrases = st.session_state.dynamic_phrases[theme_to_show]
            
            for french_phrase, english_meaning in phrases.items():
                with st.expander(f"🌟 {french_phrase} - {english_meaning}"):
                    if groq_available:
                        try:
                            context_prompt = f"""
                            Create a travel scenario for Himanshu and Anastasiya using the French phrase "{french_phrase}" ({english_meaning}) in the context of {theme_to_show}.
                            
                            Include:
                            1. A specific situation where they'd use this phrase
                            2. How it helps their travel experience
                            3. A fun moment between them
                            4. They are good best friends who recently becames friends and they are so alike 
                            5. She has promised to yake him out for a cofee in every country they both travel together
                            6. Make this fun learning experience experience, playful but not much romantic as they are still friends, impress her
                            7. she likes pink roses and tulips more
                            9.mention them as travel buddies and friends anf avoid mentioning them as best friends or besties .
                            
                            Keep it practical and fun. Use emojis.
                            """
                            
                            response = client.chat.completions.create(
                                messages=[{"role": "user", "content": context_prompt}],
                                model="llama3-70b-8192",
                                temperature=0.8
                            )
                            scenario = response.choices[0].message.content
                        except:
                            scenario = f"Perfect for {theme_to_show.lower()} adventures! You'll use '{french_phrase}' when exploring together. Every new phrase opens up new possibilities for your travels! 🌍"
                    else:
                        scenario = f"Perfect for {theme_to_show.lower()} adventures! You'll use '{french_phrase}' when exploring together. Every new phrase opens up new possibilities for your travels! 🌍"
                    
                    st.markdown(f'<div class="travel-note">{scenario}</div>', unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(f"💾 Master this!", key=f"master_{french_phrase}"):
                            if french_phrase not in st.session_state.learned_phrases:
                                st.session_state.learned_phrases.append(french_phrase)
                                st.success("Added to your mastered phrases! 🌟")
                            else:
                                st.info("Already mastered! ✨")
                    
                    with col2:
                        if st.button(f"🗣️ Practice together", key=f"practice_{french_phrase}"):
                            st.info("Practice makes perfect - especially together! ✈️")
    
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    st.markdown("### ☕ Coffee Date French Phrases")
    st.markdown("*Perfect for our coffee adventures in every second country!*")
    
    coffee_phrases = STATIC_TRAVEL_PHRASES["Coffee & Food Adventures"]
    
    for phrase, meaning in coffee_phrases.items():
        with st.expander(f"☕ {phrase} - {meaning}"):
            if groq_available:
                try:
                    coffee_prompt = f"""
                    Create a fun coffee date scenario for Himanshu and Anastasiya using the French phrase "{phrase}" ({meaning}).
                    
                    Make it travel-themed and mention their tradition of coffee dates in every second country.
                    Include how they would use this phrase together in a French café.
                    Keep it short and use emojis and keep this in mind-
                    1. They are good best friends who recently becames friends and they are so alike 
                    2. She has promised to yake him out for a cofee in every country they both travel together
                    3. Make this fun learning experience experience, playful but not romantic as they are still friends, it should sound like two best friends are going on a travel and not two couples, impress her
                    4. she likes pink roses and tulips more
                    mention them as travel buddies and friends and avoid mentioning them as best friends or besties .
                    keep this entirely focused towards two friends and do not use name of both directly, also make sure to keep it a bit generic and not much playful
                    """
                    
                    response = client.chat.completions.create(
                        messages=[{"role": "user", "content": coffee_prompt}],
                        model="llama3-70b-8192",
                        temperature=0.9
                    )
                    scenario = response.choices[0].message.content
                except:
                    scenario = f"Picture this: You two in a cozy Parisian café, practicing '{phrase}' together. The waiter brings your coffee, and you both realize - this is exactly what you dreamed of! ☕"
            else:
                scenario = f"Picture this: You two in a cozy Parisian café, practicing '{phrase}' together. The waiter brings your coffee, and you both realize - this is exactly what you dreamed of! ☕"
            
            st.markdown(f'<div class="travel-note">{scenario}</div>', unsafe_allow_html=True)
            
            if st.button(f"Practice '{phrase}' together", key=f"coffee_{phrase}"):
                st.success("Practicing together makes everything better! ☕")
    
    st.markdown('</div>', unsafe_allow_html=True)

with tab4:
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    
    if not st.session_state.selected_country:
        st.markdown("### 🌍 Choose Your Next Adventure")
        st.markdown("*Select a region to see beautiful countries to visit together*")
        
        region = st.radio("Select region:", ["Europe", "World"])
        
        st.markdown("---")
        st.markdown(f"### 🏆 Top 10 Most Beautiful {region} Countries")
        
        for country, highlights in BEAUTIFUL_COUNTRIES[region].items():
            with st.container():
                st.markdown(f"""
                <div class="country-card">
                    <div style="display: flex; align-items: center;">
                        <span class="flag-emoji">{country.split()[0]}</span>
                        <div>
                            <h4>{' '.join(country.split()[1:])}</h4>
                            <p>Highlights: {', '.join(highlights)}</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Select {country.split()[0]} {' '.join(country.split()[1:])}", key=f"select_{country}"):
                    st.session_state.selected_country = country
                    st.rerun()
    else:
        country_name = ' '.join(st.session_state.selected_country.split()[1:])
        flag = st.session_state.selected_country.split()[0]
        
        st.markdown(f"### {flag} Travel Plans for {country_name}")
        st.markdown("*Himanshu will update this with language learning soon!*")
        
        if groq_available:
            try:
                travel_prompt = f"""
                Create a 3-day travel itinerary for Himanshu and Anastasiya visiting {country_name}.
                
                Include:
                1. Must-see attractions
                2. Local food to try
                3. Coffee shop recommendations (for their tradition)
                4. Cultural tips
                5. Transportation advice
                mention them as travel buddies and friends and avoid mentioning them as best friends or besties .
                
                Make it practical but fun for two travel buddies. Use emojis.
                """
                
                response = client.chat.completions.create(
                    messages=[{"role": "user", "content": travel_prompt}],
                    model="llama3-70b-8192",
                    temperature=0.8
                )
                itinerary = response.choices[0].message.content
            except:
                itinerary = f"Adventure awaits in {country_name}! Here's a perfect itinerary for your trip together. Don't forget your coffee date tradition! ☕"
        else:
            itinerary = f"Adventure awaits in {country_name}! Here's a perfect itinerary for your trip together. Don't forget your coffee date tradition! ☕"
        
        st.markdown(f'<div class="travel-note">{itinerary}</div>', unsafe_allow_html=True)
        
        if st.button("← Choose a different country"):
            st.session_state.selected_country = None
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

with tab5:
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    st.markdown("### 💬 Practice French Together")
    st.markdown("*Chat in French and English - support each other!*")
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if prompt := st.chat_input("Practice French together (English/French mix welcome!)"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking in French..."):
                if groq_available:
                    try:
                        messages_for_llm = [{"role": "system", "content": """
                        You're helping Himanshu and Anastasiya practice French for their travels together.
                        They're learning partners who support each other. Respond naturally in English with French phrases mixed in.
                        keep in mind that-4. They are good best friends who recently becames friends and they are so alike 
                        1. She has promised to yake him out for a cofee in every country they both travel together
                        2. Make this fun learning experience experience, playful but not much romantic as they are still friends, impress her
                        3. she likes pink roses and tulips more
                        Guidelines:
                        - Be encouraging and supportive
                        - Correct gently if they make mistakes
                        - Suggest travel-relevant phrases
                        - Keep responses conversational and fun
                        - Reference their travel dreams and coffee dates occasionally
                        - Use emojis to keep it engaging
                        mention them as travel buddies and friends and avoid mentioning them as best friends or besties .
                        """}]
                        messages_for_llm += st.session_state.messages[-6:]
                        
                        response = client.chat.completions.create(
                            messages=messages_for_llm,
                            model="llama3-70b-8192",
                            temperature=0.8
                        )
                        reply = response.choices[0].message.content
                    except:
                        replies = [
                            "Très bien! (Very good!) Keep practicing together! ✨",
                            "That's perfect for your travel adventures! 🌍",
                            "You two are going to be amazing French speakers! 🗼",
                            "Practice makes perfect - and you have each other! ☕"
                        ]
                        reply = random.choice(replies)
                else:
                    replies = [
                        "Très bien! (Very good!) Keep practicing together! ✨",
                        "That's perfect for your travel adventures! 🌍", 
                        "You two are going to be amazing French speakers! 🗼",
                        "Practice makes perfect - and you have each other! ☕"
                    ]
                    reply = random.choice(replies)
                
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
    
    st.markdown('</div>', unsafe_allow_html=True)

with tab6:
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    st.markdown("### 📔 Our Travel Learning Diary")
    st.markdown("*Memories and milestones from our French learning journey*")
    
    # Add new diary entry
    if st.button("✍️ Add New Memory"):
        st.session_state.show_diary_input = True
    
    if st.session_state.get('show_diary_input', False):
        col1, col2 = st.columns(2)
        with col1:
            diary_title = st.text_input("Memory title:")
        with col2:
            diary_type = st.selectbox("Type:", ["Learning milestone", "Funny moment", "Travel plan", "Memory"])
        
        diary_content = st.text_area("Tell us about this memory...", height=100)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Save Memory"):
                st.session_state.travel_diary.append({
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "title": diary_title,
                    "content": diary_content,
                    "type": diary_type
                })
                st.success("Memory saved! ✨")
                st.session_state.show_diary_input = False
                st.rerun()
        
        with col2:
            if st.button("❌ Cancel"):
                st.session_state.show_diary_input = False
                st.rerun()
    
    # Display diary entries
    if st.session_state.travel_diary:
        st.markdown("---")
        for i, entry in enumerate(reversed(st.session_state.travel_diary)):
            with st.expander(f"📅 {entry['date']} - {entry.get('title', 'Memory')}"):
                st.markdown(f"**Type:** {entry.get('type', 'Memory')}")
                if 'content' in entry:
                    st.markdown(f"**Memory:** {entry['content']}")
    else:
        st.markdown(f'<div class="travel-note">Your travel diary is waiting for beautiful memories! Start adding entries about your French learning journey together. ✨</div>', unsafe_allow_html=True)
    
    # Progress summary
    st.markdown("---")
    st.markdown("### 🌟 Our Progress Together")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("French Phrases Learned", len(st.session_state.learned_phrases), "↗️")
    with col2:
        st.metric("Coffee Dates Planned", st.session_state.coffee_dates, "☕")
    with col3:
        st.metric("Diary Entries", len(st.session_state.travel_diary), "📔")
    
    # Motivational quote
    quotes = [
        "Together we can conquer any language! ✨",
        "Every phrase learned is a step closer to Paris! 🗼",
        "Two travel buddys, one dream, endless adventures! 🌍",
        "Coffee dates and French phrases - perfect combination! ☕",
        "Your travel dreams are becoming reality! ✈️"
    ]
    
    st.markdown(f'<div class="travel-note" style="text-align: center; font-size: 1.2em;"><strong>{random.choice(quotes)}</strong></div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; background: linear-gradient(45deg, #4e54c8, #8f94fb); color: white; padding: 2rem; border-radius: 15px; margin-top: 2rem;">
    <h4>🌍 Every phrase brings us closer to our dream! 🌍</h4>
    <p>Made for travel adventures</p>
    <p style="font-size: small;">From coffee dates to world travels - this is just the beginning! ☕✈️✨</p>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)