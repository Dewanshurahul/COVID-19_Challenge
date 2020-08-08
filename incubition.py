import json
import pandas as pd
import os
from tqdm import tqdm
import re
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np

dirs = "document_parses"
num_files = 0

docs = []
for d in [dirs + "/pdf_json/"]:
    # print(d)
    files = os.listdir(d)
    num_files += len(files)
    for file in tqdm(files):
        file_path = d + file
        j = json.load(open(file_path, "rb"))
        # print(j)
        title = j["metadata"]["title"]
        try:
            abstract = j["abstract"][0]
        except:
            abstract = ""
        full_text = ""
        for text in j["body_text"]:
            # print(text["text"])
            full_text += text["text"] + "\n\n"

        # print(full_text)
        docs.append([title, abstract, full_text])

df = pd.DataFrame(docs, columns=["title", "abstract", "full_text"])

incubation = df[df['full_text'].str.contains("incubation")]
# print(incubation.head())

texts = incubation["full_text"].values
incubation_days = []
for t in texts:
    # print(t)
    for sentence in t.split(". "):
        if "incubation" in sentence:
            incubation_period = re.findall(r" \d{1,2} day", sentence)
            if len(incubation_period) == 1:
                # print(incubation_period[0])
                # print(sentence)
                days = incubation_period[0].split(" ")
                incubation_days.append(float(days[1]))
                # print()
# print(incubation_days)
print(len(incubation_days))
print(f"Mean Incubation Time is {np.mean(incubation_days)}")

style.use("ggplot")
plt.hist(incubation_days, bins=50)
plt.ylabel("Bins Count")
plt.xlabel("Incubation Time (in Days)")
plt.show()