# Comment Keys & Values

Note that as reddit has evolved, the keys and data values pulled from the site by pushshift have also evolved. This page documents some of the normalization process.

Information was partially inferred and partially sourced from the PRAW [comment](https://praw.readthedocs.io/en/stable/code_overview/models/comment.html) documentation.

[comments key count sample](#drop)

- author_created_utc: the utc unix time the authors account was created

## `edited`

- AP = True
- datatypes
    - bool
    - int: unix datetime

### notes

> Whether or not the comment has been edited.

It is possible it may be useful, however, the data types are mixed between booleans and what appear to be unix timestamp values. It is unclear whether these timestamps are the edit time, or they are simply the time pushshift checked the comment, and found it had been edited. Furthermore, a single comment may have had multiple edits. For this reason, we reduce the unix values to simply `True`.

### examples

```json
[
    false,
    true,
    1457608008.0
]
```


## `parent_id`

- AP = True
- datatypes
    - str

### notes

> The ID of the parent comment (prefixed with t1_). If it is a top-level comment, this returns the submission ID instead (prefixed with t3_).

Useful for resolving response relationships. Furthermore, we add a resolver for whether the comment is a top level comment to the dataset.

### examples

```json
[
    "t1_c2b729",
    "t3_2b6ji",
    "t3_2b73h"
]
```

## `id`

- AP = True
- datatypes
    - str

### notes

> The ID of the comment.

Useful unique identifier for comments

### examples

```json
[
    "c2b750",
    "c2b751",
    "c2b752"
]
```

## `author_flair_text`

- AP = True
    - str
    - None

### notes

The flair text of an author. Probably useful.

### examples

```json
[
    null,
    "Professor|Computing|Machine Learning",
    "Professor | Computer Science"
]
```

## `author`

- AP = True
- datatypes
    - str

### notes

The username of the author who submitted the comment. Definitely useful.

### examples

```json
[
    "spez",
    "[deleted]"
]
```

## `retrieved_on`

- AP = False
- datatypes
    - int: unix datetime

### notes

Probably not useful.

### examples

```json
[
    1473761417,
    1473761418,
    1473761420
]
```


## `distinguished`

- AP = True
- datatypes
    - str
    - None

### notes

Seems to contain a string denoting whether the author of the comment is distinguished in the relevant sub. Seems unlikely to be useful.

### examples

```json
[
    null,
    "moderator",
    "admin",
    "special"
]
```

## various award fields

Given the platform has evolved over time, there appear to be numerous, somewhat redundant award fields. Ideally, the "awards" would simply be a single `float` representing the monetary value of all awards bestowed. There is some information lost here, because certain awards are used in certain contexts, but doing this would allow us to create a normalized `float` atemporal award value that accounts for the total award volume across the reddit platform, given that award usage has increased substantially through time.

### `gilded`

- AP = True
- datatypes
    - int

#### notes

Judging by praw docs, 0 = no award, 1 = silver, 2 = gold, 3 = platinum. There are other int values, however, and it is unclear what these represent. It could be that this field represents the total number of awards given.

Given the lack of certainty, this field is dropped.

#### examples

```json
[
    0,
    1,
    3
]
```

### `all_awardings`

- AP = False
- datatypes
  - list[dict[str, Any]]

#### notes

Is a list of dictionaries, where each dictionary element in the list for a comment represents a single award. Lots of redundant data here.

We are really just interested in the following subfields for each reward.

- name: the name of the award
- coin_price: number of coins the award costs
- id: the `gid_` value corresponding to the award name

Other potentially useful fields:

- award type: tells us whether the award is a global award (across all of reddit), or (presumably) a community specific award (still need to gather sample). might be useful but dropped for now.
- coin_reward: the number of coins awarded to the giftee, might be useful, but dropped for now
- count: might be useful if it was the count of that award type gifted, but this is unclear and it doesn't appear to be a key that universally appears.

#### examples

```json
[
    [
        {
            "award_type": "global",
            "coin_price": 500,
            "coin_reward": 100,
            "count": 1,
            "days_of_drip_extension": 0,
            "days_of_premium": 7,
            "description": "Gives the author a week of Reddit Premium, %{coin_symbol}100 Coins to do with as they please, and shows a Gold Award.",
            "end_date": null,
            "icon_height": 512,
            "icon_url": "https://www.redditstatic.com/gold/awards/icon/gold_512.png",
            "icon_width": 512,
            "id": "gid_2",
            "is_enabled": true,
            "name": "Gold",
            "resized_icons": [
                {
                    "height": 16,
                    "url": "https://www.redditstatic.com/gold/awards/icon/gold_16.png",
                    "width": 16
                },
                {
                    "height": 32,
                    "url": "https://www.redditstatic.com/gold/awards/icon/gold_32.png",
                    "width": 32
                },
                {
                    "height": 48,
                    "url": "https://www.redditstatic.com/gold/awards/icon/gold_48.png",
                    "width": 48
                },
                {
                    "height": 64,
                    "url": "https://www.redditstatic.com/gold/awards/icon/gold_64.png",
                    "width": 64
                },
                {
                    "height": 128,
                    "url": "https://www.redditstatic.com/gold/awards/icon/gold_128.png",
                    "width": 128
                }
            ],
            "start_date": null,
            "subreddit_coin_reward": 0,
            "subreddit_id": null
        }
    ],
    [
        {
            "award_type": "global",
            "coin_price": 100,
            "coin_reward": 0,
            "count": 1,
            "days_of_drip_extension": 0,
            "days_of_premium": 0,
            "description": "Shows the Silver Award... and that's it.",
            "end_date": null,
            "icon_height": 512,
            "icon_url": "https://www.redditstatic.com/gold/awards/icon/silver_512.png",
            "icon_width": 512,
            "id": "gid_1",
            "is_enabled": true,
            "name": "Silver",
            "resized_icons": [
                {
                    "height": 16,
                    "url": "https://www.redditstatic.com/gold/awards/icon/silver_16.png",
                    "width": 16
                },
                {
                    "height": 32,
                    "url": "https://www.redditstatic.com/gold/awards/icon/silver_32.png",
                    "width": 32
                },
                {
                    "height": 48,
                    "url": "https://www.redditstatic.com/gold/awards/icon/silver_48.png",
                    "width": 48
                },
                {
                    "height": 64,
                    "url": "https://www.redditstatic.com/gold/awards/icon/silver_64.png",
                    "width": 64
                },
                {
                    "height": 128,
                    "url": "https://www.redditstatic.com/gold/awards/icon/silver_128.png",
                    "width": 128
                }
            ],
            "start_date": null,
            "subreddit_coin_reward": 0,
            "subreddit_id": null
        }
    ]
]
```

### `associated_award`

~~It is not clear how this field differs from the previous one. It's possible it is the same field, but was renamed at some point, or that it is a duplicate field and they need to be consolidated.~~

~~After testing for co-occurrence, it appears that these fields are never both populated at the same time - it is either one or the other. This leads me to believe that they are the same field, but simply duplicated. I don't have conclusive proof of this, but I'm going to continue operating as though this is true. This was checked with the following comment handler across 1e7 comments from November 2020, and passed without errors.~~

```python
def comment_handler(comment: dict) -> int:
    if comment["all_awardings"] != []:
        assert comment["associated_award"] is None
    if comment["associated_award"] is not None:
        assert comment["all_awardings"] == []
```

Upon further inspection, it appears that while all_awards is a list of award dictionaries, associated award is a single award dictionary. Accordingly I'd infer that in the former case, there are multiple awards, and in the latter, there is a single award.

### `gildings`

- AP: False
- datatypes:
  - dict[str, int]

### notes

This field appears to contain a count of the unique gildings of a particular award. It should be consolidated with the previous fields.

- [x] Furthermore, the `gid_` labels need to be resolved into their associated award names, and included as a resource in the package.

Notably, it only seems to account for silver, gold, and platinum...

### examples

```json
{
    "gid_1": 5,
    "gid_2": 1
},
{
    "gid_1": 6,
    "gid_2": 1
}
```

### `top_awarded_type`

This field is dropped, it doesn't appear to be useful. And in the samples taken is always `null`.



## Complete Data

### Keep
- subreddit
- score
- created_utc

### Transmute

### Drop
- distinguished
- subreddit_id

### Add
- root (root comment)

### Uncertain
- edited
- parent_id
- id
- author_flair_text
- author
- gilded
- link_id
- controversiality
- body
- author_flair_css_class

## Partial Data


"retrieved_on": "2004035",
"stickied": 1083943,
"ups": 1283963,
"downs": 930093,
"score_hidden": 1220122,
"name": 1180118,
"archived": 1270151,
"all_awardings": 470024,
"associated_award": 440044,
"author_created_utc": 558439,
"author_flair_background_color": 570057,
"author_flair_template_id": 590059,
"author_flair_text_color": 570057,
"author_fullname": 533109,
"awarders": 190019,
"can_gild": 710071,
"can_mod_post": 350035,
"collapsed": 580058,
"collapsed_reason": 580058,
"gildings": 540054,
"is_submitter": 670067,
"locked": 470024,
"no_follow": 600060,
"permalink": 650065,
"quarantined": 240024,
"removal_reason": 483943,
"send_replies": 600060,
"steward_reports": 49969,
"subreddit_name_prefixed": 510051,
"subreddit_type": 640064,
"total_awards_received": 470024,
"author_flair_richtext": 513908,
"author_flair_type": 513908,
"author_patreon_flair": 477003,
"author_cakeday": 2304,
"author_premium": 377567,
"collapsed_because_crowd_control": 420042,
"media_metadata": 463,
"collapsed_reason_code": 250025,
"comment_type": 320032,
"top_awarded_type": 350035,
"treatment_tags": 380038,
"unrepliable_reason": 200020,
"editable": 28,
"rte_mode": 10001,
"author_is_blocked": 20002,
"retrieved_unix": 50005,
"approved_at_unix": 10001
