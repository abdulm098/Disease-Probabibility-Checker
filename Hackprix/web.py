import webbrowser
from flask import Flask, render_template, request, redirect,jsonify
import json

app = Flask(__name__)

# Define diseases and their symptoms
diseases = {
    "Flu": {"fever": 0.8, "cough": 0.6, "fatigue": 0.7, "sore throat": 0.5},
    "Common Cold": {"fever": 0.3, "cough": 0.5, "fatigue": 0.4, "sore throat": 0.6},
    "COVID-19": {"fever": 0.9, "cough": 0.8, "fatigue": 0.8, "loss of taste": 0.7},
    "Heart Attack": {"chest pain": 0.9, "shortness of breath": 0.8, "nausea": 0.7, "sweating": 0.6},
    "Diabetes": {"increased thirst": 0.8, "frequent urination": 0.7, "fatigue": 0.6, "blurred vision": 0.5},
    "Asthma": {"shortness of breath": 0.8, "wheezing": 0.7, "chest tightness": 0.6, "cough": 0.5},
    "Pneumonia": {"fever": 0.7, "cough": 0.8, "chills": 0.6, "shortness of breath": 0.7},
    "Stomach Flu": {"nausea": 0.7, "vomiting": 0.8, "diarrhea": 0.7, "stomach pain": 0.6},
    "Migraine": {"headache": 0.9, "nausea": 0.7, "sensitivity to light": 0.8, "blurred vision": 0.6},
    "Hypertension": {"headache": 0.6, "dizziness": 0.7, "blurred vision": 0.5, "shortness of breath": 0.4}
}

def get_remedies(symptoms):
    remedies = []
    # Here you can implement logic to fetch remedies based on the symptoms
    # For demonstration purposes, I'll just return some dummy remedies based on the symptoms provided

    # Check if symptoms are present and fetch remedies accordingly
    
    if "fever" in symptoms:
        remedies.append("Drink plenty of fluids and stay hydrated.")
        remedies.append("Rest as much as possible.")
        remedies.append("Take over-the-counter fever-reducing medication such as acetaminophen (Tylenol).")
    if "cough" in symptoms:
        remedies.append("Stay hydrated by drinking warm liquids.")
        remedies.append("Use a humidifier to moisten the air and ease coughing.")
        remedies.append("Gargle with warm salt water to soothe a sore throat caused by coughing.")
    if "fatigue" in symptoms:
        remedies.append("Get plenty of rest and sleep.")
        remedies.append("Eat a balanced diet rich in vitamins and minerals.")
        remedies.append("Engage in light exercise or physical activity to boost energy levels.")
    if "sore throat" in symptoms:
        remedies.append("Drink warm liquids such as tea with honey to soothe a sore throat.")
        remedies.append("Use throat lozenges or hard candy to keep the throat moist.")
        remedies.append("Avoid irritants such as cigarette smoke or pollution.")
    if "loss of taste" in symptoms:
        remedies.append("Try strong flavors like garlic, onions, or ginger.")
        remedies.append("Rinse your mouth with a mixture of warm water and salt.")

    if "chest pain" in symptoms:
        remedies.append("If it's mild, take rest and avoid strenuous activities.")
        remedies.append("If severe or prolonged, seek immediate medical attention.")

    if "nausea" in symptoms:
        remedies.append("Eat small, bland meals throughout the day.")
        remedies.append("Drink clear fluids to stay hydrated.")
        remedies.append("Ginger tea or ginger ale might help settle the stomach.")

    if "vomiting" in symptoms:
        remedies.append("Stay hydrated by sipping clear fluids like water or broth.")
        remedies.append("Avoid solid foods until vomiting subsides.")
        remedies.append("If vomiting persists, seek medical advice.")

    if "shortness of breath" in symptoms:
        remedies.append("Sit upright and practice deep breathing exercises.")
        remedies.append("Use a fan or open windows for fresh air.")
        remedies.append("Seek medical help if breathing difficulties worsen.")

    if "sweating" in symptoms:
        remedies.append("Wear loose, breathable clothing.")
        remedies.append("Stay hydrated with water or sports drinks.")
        remedies.append("Use a fan or air conditioning to cool down.")

    if "increased thirst" in symptoms:
        remedies.append("Drink plenty of water throughout the day.")
        remedies.append("Limit caffeine and sugary drinks.")
        remedies.append("Eat water-rich fruits and vegetables like watermelon or cucumber.")

    if "blurry vision" in symptoms:
        remedies.append("Rest your eyes by taking regular breaks from screens.")
        remedies.append("Ensure proper lighting when reading or working.")
        remedies.append("If blurry vision persists, consult an eye specialist.")

    if "frequent urination" in symptoms:
        remedies.append("Limit intake of caffeine and alcohol.")
        remedies.append("Practice bladder training exercises.")
        remedies.append("Monitor fluid intake, especially before bedtime.")

    if "wheezing" in symptoms:
        remedies.append("Use a rescue inhaler if prescribed by a doctor.")
        remedies.append("Avoid triggers like smoke, pollen, or pet dander.")
        remedies.append("Sit upright and try controlled breathing techniques.")

    if "chest tightness" in symptoms:
        remedies.append("Use a warm compress on the chest to relax muscles.")
        remedies.append("Practice deep breathing exercises.")
        remedies.append("Avoid triggers like smoke or strong odors.")

    if "diarrhea" in symptoms:
        remedies.append("Stay hydrated with electrolyte-rich drinks.")
        remedies.append("Eat bland, easy-to-digest foods like rice, bananas, or toast.")
        remedies.append("Avoid dairy, fatty foods, and caffeine.")

    if "stomach pain" in symptoms:
        remedies.append("Apply a warm compress to the abdomen for relief.")
        remedies.append("Avoid spicy, greasy, or acidic foods.")
        remedies.append("Drink peppermint or chamomile tea to soothe the stomach.")

    if "headache" in symptoms:
        remedies.append("Rest in a quiet, dark room.")
        remedies.append("Apply a cold compress to the forehead or temples.")
        remedies.append("Take over-the-counter pain relievers like ibuprofen or acetaminophen as directed.")

    if "sensitivity to light" in symptoms:
        remedies.append("Wear sunglasses or a hat with a brim when outdoors.")
        remedies.append("Adjust screen brightness on electronic devices.")
        remedies.append("Use dim lighting indoors and avoid fluorescent lights if possible.")

    if "dizziness" in symptoms:
        remedies.append("Sit or lie down in a comfortable position.")
        remedies.append("Stay hydrated and avoid sudden movements.")
        remedies.append("If dizziness persists, seek medical attention.")
    

    # Format remedies as an HTML list
    html_remedies = "<ul>"
    for remedy in remedies:
        html_remedies += f"<li>{remedy}</li>"
    html_remedies += "</ul>"
    
    return html_remedies
# Function to calculate probabilities
def calculate_probabilities(user_symptoms, diseases):
    probabilities = {disease: 1.0 for disease in diseases}
    
    for disease, symptoms in diseases.items():
        for symptom in symptoms:
            if symptom in user_symptoms:
                probabilities[disease] *= symptoms[symptom]
            else:
                probabilities[disease] *= (1 - symptoms[symptom])
    
    # Normalize the probabilities to sum to 100%
    total_prob = sum(probabilities.values())
    for disease in probabilities:
        probabilities[disease] = (probabilities[disease] / total_prob) * 100
    
    return probabilities

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        user_input = request.form['symptoms'].strip().lower().split(", ")
        probabilities = calculate_probabilities(user_input, diseases)
        
        sorted_probabilities = sorted(probabilities.items(), key=lambda x: x[1], reverse=True)
        top_probabilities = sorted_probabilities[:5]
        
        return render_template('result.html', symptoms=user_input, top_probabilities=top_probabilities,remedies=None)
    else:
        return redirect('/')  # Redirect to the home page if accessed via GET request

@app.route('/remedies', methods=['POST'])
def show_remedies():
    if request.method == 'POST':
        symptoms = request.form.get('symptoms').strip().lower().split(", ")
        top_probabilities = json.loads(request.form.get('top_probabilities'))
        
        if request.form['remedies'] == 'Yes':
            remedies = get_remedies(symptoms)
            return render_template('result.html', symptoms=symptoms, top_probabilities=top_probabilities, remedies=remedies)
        else:
            return redirect('/')
    else:
        return redirect('/')

if __name__ == '__main__':
    webbrowser.open_new('http://127.0.0.1:5000/result')
    app.run(debug=True)