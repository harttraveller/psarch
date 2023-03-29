from tqdm import tqdm

UNUSED_KEYS = [
    "retrieved_on",
    "distinguished",
    "author_flair_background_color",
    "author_flair_css_class",
    "author_flair_richtext",
    "author_flair_template_id",
    "author_flair_text_color",
    "author_flair_type",
    "author_fullname",
    "author_patreon_flair",
    "can_gild",
    "can_mod_post",
    "author_premium",
    "controversiality",
    "locked",
    "no_follow",
    "quarantined",
    "send_replies",
    "subreddit_id",
    "subreddit_name_prefixed",
    "comment_type",
    "editable",
]


class CommentHandler:
    @staticmethod
    def delete_unused(comment: dict) -> None:
        for key in UNUSED_KEYS:
            if key in comment.keys():
                del comment[key]

    @staticmethod
    def convert_edited(comment: dict) -> None:
        comment["edited"] = comment["edited"] is not False

    @staticmethod
    def is_root_comment(comment: dict) -> None:
        comment["root"] = comment["parent_id"][:3] == "t3_"

    @staticmethod
    def parse(comment: dict) -> dict:
        CommentHandler.delete_unused(comment)
        CommentHandler.convert_edited(comment)
        CommentHandler.is_root_comment(comment)
        return comment

    @staticmethod
    def ingest(comments: list[dict], verbose: bool = False) -> list[dict]:
        for i in tqdm(range(len(comments)), disable=not verbose):
            comments[i] = CommentHandler.parse(comments[i])
        return comments
