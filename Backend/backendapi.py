from flask import Flask, jsonify, request
from flask_cors import CORS
# from recipe_recommender import input_query

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import string
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import datasets
import os
import google.generativeai as genai
from scipy.sparse import save_npz, load_npz
import joblib
import json
import os

# from recipe_recommender import input_query
# from recipe_recommender import input_query


# nltk.download("stopwords")
# nltk.download('punkt_tab')
# nltk.download('wordnet')
# nltk.download("stopwords")
# nltk.download('punkt_tab')
# nltk.download('wordnet')
dataset = datasets.load_dataset(
    "parquet", data_files="Backend/data/big_recipes.indexed.parquet")['train']  # requires the parquet file ofc

# Preprocessing function
digits = re.compile(r'\d')
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))
no_info = set(['need', 'making', 'make', 'cooking', 'take', 'use', 'used', 'recipe',
              'ingredient', 'doe', 'food', 'eaten', 'eat', 'eating',
               'ingredient', 'doe', 'food', 'eaten', 'eat', 'eating',
               'course', 'main', 'know', 'friend', 'want', 'like', 'craving', 'please'])
skip = stop_words.union(no_info)


def preprocess(doc):
    words = word_tokenize(doc)
    words = [text.translate(str.maketrans(
        '', '', string.punctuation)).lower() for text in words]
    words = [word for word in words if not digits.match(
        word) and not word in skip]
    words = [lemmatizer.lemmatize(word) for word in words if word]
    return words


"""
['RecipeId', 'Name', 'AuthorId', 'AuthorName', 'CookTime', 'PrepTime',
       'TotalTime', 'DatePublished', 'Description', 'Images', 'RecipeCategory',
       'Keywords', 'RecipeIngredientQuantities', 'RecipeIngredientParts',
       'AggregatedRating', 'ReviewCount', 'Calories', 'FatContent',
       'SaturatedFatContent', 'CholesterolContent', 'SodiumContent',
       'CarbohydrateContent', 'FiberContent', 'SugarContent', 'ProteinContent',
       'RecipeServings', 'RecipeYield', 'RecipeInstructions', 'name',
       'description', 'ingredients', 'ingredients_raw_str', 'serving_size',
       'servings', 'steps', 'tags', 'search_terms']
 """


all_columns = ["Name", "RecipeIngredientParts",
               "RecipeInstructions", "Keywords", "search_terms"]
dataset = dataset.map(lambda x: {"text": " ".join(
    [str(x[col]) for col in all_columns])})

new_data = dataset.remove_columns(all_columns)
dataset = dataset.remove_columns("text")

# TF-IDF implementation
# vectorizer = TfidfVectorizer(tokenizer=preprocess)
# vectorizer = TfidfVectorizer(tokenizer=preprocess)
# This function takes around 9 minutes rest of the code is way faster
# X = vectorizer.fit_transform(new_data['text'])
# joblib.dump(vectorizer, "vectorizer.joblib")
# save_npz("tfidf_matrix.npz", X)
# vectorizer_path = os.path.join(os.path.dirname(__file__), "data/vectorizer.joblib")
# r"C:\Users\jules\Desktop\KUL\FMMI\Backend\data\vectorizer.joblib"
vectorizer = joblib.load("Backend/data/vectorizer.joblib")
X = load_npz("Backend/data/tfidf_matrix.npz")


def string_to_vector(query_string):
    prep = preprocess(query_string)
    return vectorizer.transform([" ".join(prep)])


def relevant_docs(query_vector):
    cosine_similarities = cosine_similarity(query_vector, X)
    cos_ind = np.argpartition(
        cosine_similarities[0], -30)[-30:]  # Last N values
    cos_res = cos_ind[np.argsort(cosine_similarities[0][cos_ind])[::-1]]
    cos_results = [(dataset[i], cosine_similarities[0][i])
                   for i in cos_res.tolist()]
    actual_rel = [filtered[0] for filtered in cos_results if (
        filtered[1] > 0.121 and filtered[1] > cos_results[10][1])]  # Determine the amount of recipes
    return actual_rel


def docs_dic_to_string(rel_docs):
    recipes = ""
    for l in range(len(rel_docs)):
        recipes += f"Recipe: {l+1}\n"
        recipes += f"Id: {rel_docs[l]['RecipeId']}\n"
        recipes += f"Name: {rel_docs[l]['Name']}\n"
        recipes += f"Ingredients: {rel_docs[l]['RecipeIngredientParts']+rel_docs[l]['RecipeIngredientQuantities']}\n"
        recipes += f"Ingredients quantities: {rel_docs[l]['ingredients_raw_str']}\n"
        recipes += f"Steps: {rel_docs[l]['RecipeInstructions']}\n"
        recipes += f"Keywords: {rel_docs[l]['Keywords']}\n"
        recipes += f"Calories: {rel_docs[l]['Calories']}\n"
        recipes += f"Total fat: {rel_docs[l]['FatContent']}\n"
        # recipes += f"Estimated time: {rel_docs[l]['TotalTime']}\n \n"
    return recipes


def doc_to_string(doc):
    ret = ''
    ret += f"Id: {doc['RecipeId']}\n"
    ret += f"Name: {doc['Name']}\n"
    ret += f"Ingredients: {doc['RecipeIngredientParts'] + doc['RecipeIngredientQuantities']}\n"
    ret += f"Ingredients quantities: {doc['ingredients_raw_str']}\n"
    ret += f"Steps: {doc['RecipeInstructions']}\n"
    ret += f"Keywords: {doc['Keywords']}\n"
    ret += f"Calories: {doc['Calories']}\n"
    ret += f"Total fat: {doc['FatContent']}\n"
    # ret += f"Estimated time: {doc['TotalTime']}\n"
    return ret


# outputs all the columns of the recipes in a JSON format
def docs_dic_to_json(rel_docs):
    return json.dumps(rel_docs, indent=4)


# Read the file and set the API key
with open("Backend/data/apikey.txt", "r") as file:
    api_key = file.read().strip()  # Read and remove any trailing whitespace

os.environ["API_KEY"] = api_key  # Set API_KEY environment variable

genai.configure(api_key=os.environ["API_KEY"])

genai.configure(api_key=os.environ["API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")


def generate_health_explanations(own_query):
    prompt = f"""Provide explanations for each recipe focus on how they are healthy. (put these explanations in JSON format!)
    The recipes are: {docs_dic_to_string(relevant_docs(string_to_vector(own_query)))}. Be sure to add the recipe ID's to the JSON file!"""
    response = model.generate_content(f"{prompt}")
    return response.text.replace('```json\n', '').replace('\n```', '')

# print(prompt)
# print(response.text)


def input_query(query):
    data_to_return = {
        "recipes": docs_dic_to_json(relevant_docs(string_to_vector(query))),
        "explanations": generate_health_explanations(query)
    }
    return data_to_return


# print(input_query(own_query))
# print(input_query(own_query))

##############################################################################################################
##############################################################################################################
##############################################################################################################
##############################################################################################################
##############################################################################################################

app = Flask(__name__)
# Prod: CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
CORS(app)

# Example data
tasks = [
    {"hello": "world"}
]

# Home route


@app.route("/", methods=["GET"])
def home():
    return jsonify(tasks)

# Generate recipes


@app.route("/generate", methods=["POST"])
def generate():
    if not request.json or "dietary" not in request.json:  # body valid
        print("error invalid data")
        return jsonify({"error": "Invalid data"}), 400
    data = request.json
    diets_str = ", ".join(data["dietary"])
    cuisines_str = ", ".join(data["cuisine"])
    ingredients_str = ", ".join(data["ingredients"])
    client_query = f"Recipes that follow the diets {diets_str} from the cuisines {cuisines_str} with the ingredients {ingredients_str}"
    return jsonify(input_query(client_query)), 201


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
