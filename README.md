# 🎬 CineMatch AI 

**A machine learning-based movie recommendation system that helps users discover movies based on movie similarity, genres, tags, and ratings.**

## 🚀 **Overview**

CineMatch AI is a movie recommendation system built using Python and machine learning techniques.

The project analyzes movie information, user ratings, genres, and tags to identify relationships between movies and generate relevant recommendations.

The system also integrates movie posters to provide a more engaging movie discovery experience.

## ✨ **Features**

- 🎬 Movie recommendations
- ⭐ Rating analysis
- 🏷️ Genre and tag-based analysis
- 🧠 Machine learning-based recommendation
- 🔎 Movie similarity analysis
- 🖼️ Movie poster integration
- 📊 Exploratory Data Analysis
- 🌐 Interactive Streamlit application

## 🛠️ **Tech Stack**

<p align="center">
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" width="50" height="50" alt="Python"/>
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/pandas/pandas-original.svg" width="50" height="50" alt="Pandas"/>
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/numpy/numpy-original.svg" width="50" height="50" alt="NumPy"/>
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/scikitlearn/scikitlearn-original.svg" width="50" height="50" alt="Scikit-learn"/>
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/jupyter/jupyter-original.svg" width="50" height="50" alt="Jupyter"/>
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/streamlit/streamlit-original.svg" width="50" height="50" alt="Streamlit"/>
</p>

<p align="center">
Python • Pandas • NumPy • Scikit-learn • Jupyter Notebook • Streamlit • OMDb API
</p>

## 📂 **Project Structure**

```text
CineMatch-AI/
│
├── Data/
│   ├── README.md
│   ├── Links.csv
│   ├── Movies.csv
│   ├── Ratings.csv
│   └── Tags.csv
│
├── Notebooks/
│   ├── Eda.ipynb
│   └── 2_model_explanation.ipynb
│
├── Src/
│   ├── Poster.py
│   └── Recommendor.py
│
├── App.py
├── Requirements.txt
├── .gitignore
└── README.md
```
«"Data/README.md" contains the original dataset documentation and licensing information.» 

## 📊 **Dataset**

CineMatch AI uses movie data containing information about movies, user ratings, tags, and external movie identifiers.

### **Movies.csv**

Contains movie information such as:

- Movie ID
- Movie title
- Genres

### **Ratings.csv**

Contains user rating information:

- User ID
- Movie ID
- Rating
- Timestamp

### **Tags.csv**

Contains user-generated tags associated with movies.

### **Links.csv**

Contains external identifiers associated with movies.

## 🧠 **Recommendation Pipeline**

```text
Movie Dataset
      ↓
Data Preprocessing
      ↓
Feature Engineering
      ↓
Movie Representation
      ↓
Similarity Calculation
      ↓
Top Recommendations
      ↓
Poster Integration
      ↓
Streamlit Application
```

The system processes relevant movie information into features and calculates similarity between movies to generate recommendations for the selected movie.

## 📓 **Notebooks**

### **Eda.ipynb**

Contains the exploratory data analysis performed on the movie dataset, including:

- Dataset exploration
- Rating distribution
- Genre analysis
- Movie statistics
- Data patterns and observations

### **2_model_explanation.ipynb**

Contains the development and explanation of the recommendation model, including feature processing and similarity-based recommendation.

## 🧩 **Source Code**

### **Recommendor.py**

Contains the core recommendation logic used to generate movie recommendations.

### **Poster.py**

Handles movie poster retrieval and integration into the application.

## 🖥️ **Application**

`App.py` contains the Streamlit application through which users can interact with CineMatch AI and explore movie recommendations.

## ⚙️ **Installation**

### **1. Clone the repository**

```bash
git clone https://github.com/arjunsrivatsa13/CineMatch-AI.git
cd CineMatch-AI
```

### **2. Create a virtual environment**

```bash
python -m venv venv
```

Activate it:

**macOS / Linux**

```bash
source venv/bin/activate
```

**Windows**

```bash
venv\Scripts\activate
```

### **3. Install dependencies**

```bash
pip install -r Requirements.txt
```

### **4. Run the application**

```bash
streamlit run App.py
```

## 🎯 **Objective**

The goal of CineMatch AI is to demonstrate how machine learning, data analysis, recommendation algorithms, and API integration can be combined to create an interactive movie discovery platform.
