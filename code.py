import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import wordcloud

script_dir = os.path.dirname(os.path.abspath(__file__))

csv_file_path = os.path.join(script_dir, "INvideos.csv")

df = pd.read_csv(csv_file_path)

print("Current Working Directory:", os.getcwd())
print("Files in Current Directory:", os.listdir())
csv_file_path = os.path.join(os.getcwd(), "INvideos.csv")
print("Full Path to CSV File:", csv_file_path)

try:
    df = pd.read_csv("USvideos.csv")
    print("CSV File successfully read.")
except FileNotFoundError:
    print("CSV File not found.")
PLOT_COLORS = ["#268bd2", "#0052CC", "#FF5722", "#b58900", "#003f5c"]

custom_palette = ["#66c2a5", "#fc8d62", "#8da0cb", "#e78ac3", "#a6d854"]

sns.set_palette(custom_palette)


plt.style.use('ggplot')

font_properties = {'family': 'sans-serif', 'weight': 'normal', 'size': 12}
plt.rc('font', **font_properties)

plt.figure(figsize=(8, 5), dpi=100)

def contains_capitalized_word(s):
    for w in s.split():
        if w.isupper():
            return True
    return False

df["contains_capitalized"] = df["title"].apply(contains_capitalized_word)

value_counts = df["contains_capitalized"].value_counts().to_dict()
fig, ax = plt.subplots()
_ = ax.pie([value_counts[False], value_counts[True]], labels=['No', 'Yes'], 
           colors=['#003f5c', '#ffa600'], textprops={'color': '#040204'}, startangle=45)
_ = ax.axis('equal')
_ = ax.set_title('Title Contains Capitalized Word?')

df["title_length"] = df["title"].apply(lambda x: len(x))

fig, ax = plt.subplots()
_ = sns.distplot(df["title_length"], kde=False, rug=False, 
                 color=PLOT_COLORS[4], hist_kws={'alpha': 1}, ax=ax)
_ = ax.set(xlabel="Title Length", ylabel="No. of videos", xticks=range(0, 110, 10))

fig, ax = plt.subplots()
_ = ax.scatter(x=df['views'], y=df['title_length'], color=PLOT_COLORS[2], edgecolors="#000000", linewidths=0.5)
_ = ax.set(xlabel="Views", ylabel="Title Length")

# Exclude non-numeric columns from correlation calculation
numeric_columns = df.select_dtypes(include=np.number).columns
correlation_matrix = df[numeric_columns].corr()

# Plot heatmap using the correlation matrix
fig, ax = plt.subplots(figsize=(10,6))
_ = sns.heatmap(correlation_matrix, annot=True, cmap=sns.cubehelix_palette(as_cmap=True), ax=ax)

title_words = list(df["title"].apply(lambda x: x.split()))
title_words = [x for y in title_words for x in y]
wc = wordcloud.WordCloud(width=1200, height=500, 
                         collocations=False, background_color="white", 
                         colormap="tab20b").generate(" ".join(title_words))
plt.figure(figsize=(15,10))
plt.imshow(wc, interpolation='bilinear')
_ = plt.axis("off")

plt.show()
