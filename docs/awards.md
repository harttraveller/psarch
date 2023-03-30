# Awards

As far as I can tell there are three separate "periods" for the awards. Unfortunately there is sometimes but not always duplicate information, or information in one field missing from another. I include some notes below and details on the way I attempted to solve this.

## Notes

In the first period, there was only reddit gold. For these comments, the `gilded` field simply counted an int value of how many times a comment had been gilded.

In the second period, there was gold, silver, and platinum. For these comments, the the `gildings` field is used. The `gilded` field is also used, but seemingly only sometimes.

In the third period, more advanced fields were used. With `all_awardings` containing a list of detailed award information, and `associated_award` containing a dictionary of award information, equivalent to an element from `all_awardings` - used when only one award was given to a comment. These final fields contain the most detailed and complete information.


## Solution

- If `all_awardings` is available, use this for reward information, return information, else...
- If `associated_award` is available, use this for reward information, return information, else...
- If `gildings` is available, use this for reward information, return information, else...
- Use `gilded` for reward information.