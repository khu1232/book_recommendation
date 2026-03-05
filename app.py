# from flask import Flask,render_template,request
# import pickle
# import numpy as np

# popular_df = pickle.load(open('famous_df.pkl','rb'))
# pt = pickle.load(open('pt.pkl','rb'))
# books = pickle.load(open('books.pkl','rb'))
# similarity_scores = pickle.load(open('similarity_scores.pkl','rb'))

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('index.html',
#                            book_name = list(popular_df['Book-Title'].values),
#                            author=list(popular_df['Book-Author'].values),
#                            image=list(popular_df['Image-URL-S'].values),
#                            votes=list(popular_df['num_ratings'].values),
#                            rating=list(popular_df['avg_rating'].values)
#                            )

# @app.route('/recommend')
# def recommend_ui():
#     return render_template('recommend.html')

# @app.route('/recommend_books',methods=['post'])
# def recommend():
#     user_input = request.form.get('user_input')
#     index = np.where(pt.index == user_input)[0][0]
#     similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

#     data = []
#     for i in similar_items:
#         item = []
#         temp_df = books[books['Book-Title'] == pt.index[i[0]]]
#         item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
#         item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
#         item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-S'].values))

#         data.append(item)

#     print(data)

#     return render_template('recommend.html',data=data)

# if __name__ == '__main__':
#     app.run(debug=True)

import streamlit as st
import pickle
import numpy as np
import pandas as pd

# ----------------------------
# Load Data / Models
# ----------------------------
popular_df = pickle.load(open('famous_df.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl','rb'))

# ----------------------------
# Page Config
# ----------------------------
st.set_page_config(page_title="Book Recommendation System", layout="wide")
st.title("📚 Book Recommendation System")

# ----------------------------
# Tabs for Better UX
# ----------------------------
tab1, tab2 = st.tabs(["Recommend Books", "Popular Books"])

# ----------------------------
# Tab 1: Book Recommendation
# ----------------------------
with tab1:
    st.subheader("Find Books Similar to Your Choice")
    user_input = st.text_input("Enter a Book Name:")

    if st.button("Recommend"):
        if user_input not in pt.index:
            st.warning("Book not found! Check spelling or try another book.")
        else:
            index = np.where(pt.index == user_input)[0][0]
            similar_items = sorted(
                list(enumerate(similarity_scores[index])),
                key=lambda x: x[1],
                reverse=True
            )[1:5]

            st.subheader("Recommended Books")
            rec_cols = st.columns(4)  # 4 books per row
            for idx, i in enumerate(similar_items):
                item_col = rec_cols[idx % 4]
                temp_df = books[books['Book-Title'] == pt.index[i[0]]]
                book_title = temp_df['Book-Title'].drop_duplicates().values[0]
                author = temp_df['Book-Author'].drop_duplicates().values[0]
                img_url = temp_df['Image-URL-S'].drop_duplicates().values[0]

                with item_col:
                    st.image(img_url,width=70)
                    st.markdown(f"**{book_title}**")
                    st.markdown(f"*{author}*")
                    st.markdown("<br><br>", unsafe_allow_html=True)  # bigger gap

# ----------------------------
# Tab 2: Popular Books (Responsive Grid)
# ----------------------------
with tab2:
    st.subheader("Popular Books")
    books_per_row = 5  # change based on screen size
    for i in range(0, len(popular_df), books_per_row):
        cols = st.columns(books_per_row)
        for idx, col in enumerate(cols):
            if i + idx < len(popular_df):
                row = popular_df.iloc[i + idx]
                with col:
                    st.image(row['Image-URL-S'], width=60)
                    st.markdown(f"**{row['Book-Title']}**")
                    st.markdown(f"*{row['Book-Author']}*")
                    st.markdown(f"Votes: {row['num_ratings']}")
                    st.markdown(f"Rating: {row['avg_rating']}")
                    st.markdown("<br><br>", unsafe_allow_html=True)  # bigger gap