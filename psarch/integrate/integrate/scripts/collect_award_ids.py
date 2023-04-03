import pandas as pd

page = pd.read_html(
    "https://praw.readthedocs.io/en/stable/code_overview/models/comment.html"
)
award_ids = {}
for row in page[1].iterrows():
    award_ids[row[1]["Gild Type"]] = {"name": row[1]["Name"], "cost": row[1]["Cost"]}

print(award_ids)
