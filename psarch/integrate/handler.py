from tqdm import tqdm
from psarch.resource import AWARD_DICT

KEYS_UNUSED = [
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
    "ups",
    "gilded",
    "edited",
]

KEYS_FILTERED = {
    "parent_id",
    "id",
    "author_flair_text",
    "author",
    "link_id",
    "body",
    "created_utc",
    "score",
    "subreddit",
    "all_awardings",
    "associated_award",
    "gildings",
    "gilded",
}


class AwardResolver:
    @staticmethod
    def delete_old_reward_keys(comment: dict) -> dict:
        for key in [
            "associated_award",
            "all_awardings",
            "awarders",
            "top_awarded_type",
            "total_awards_received",
            "gilded",
            "gildings",
        ]:
            if key in comment.keys():
                del comment[key]
        return comment

    @staticmethod
    def update_awarders(comment: dict) -> dict:
        if "awarders" in comment.keys():
            if len(comment["awarders"]):
                comment["awards"]["awarders"] = comment["awarders"]
        return comment

    @staticmethod
    def insert_new_award_data(comment: dict, award_dict: dict) -> dict:
        if award_dict["total"]["count"]:
            comment["award.value.sum"] = award_dict["total"]["value"]
            comment["award.value.max"] = max(
                [award["value"] for award in award_dict["unique"].values()]
            )
            comment["award.value.min"] = min(
                [award["value"] for award in award_dict["unique"].values()]
            )
            comment["award.value.mean"] = sum(
                [award["value"] for award in award_dict["unique"].values()]
            ) / len(award_dict["unique"])
            # TODO: comment["award.value.median"]
            # TODO: comment["award.value.mode"]
            comment["award.count.total"] = award_dict["total"]["count"]
            comment["award.count.unique"] = len(award_dict["unique"])
        else:
            comment["award.value.sum"] = 0
            comment["award.value.max"] = 0
            comment["award.value.min"] = 0
            comment["award.value.mean"] = 0
            # comment["award.value.median"] = 0
            # comment["award.value.mode"] = 0
            comment["award.count.total"] = 0
            comment["award.count.unique"] = 0
        return comment

    @staticmethod
    def parse_all_awardings(comment: dict) -> dict:
        award_dict = {"total": {"value": 0, "count": 0}, "unique": {}}
        for award in comment["all_awardings"]:
            name = award["name"]
            price = award["coin_price"]
            count = award["count"]
            value = price * count
            award_dict["total"]["count"] += count
            award_dict["total"]["value"] += value
            award_dict["unique"][name] = dict()
            award_dict["unique"][name]["count"] = count
            award_dict["unique"][name]["price"] = price
            award_dict["unique"][name]["value"] = value
        comment = AwardResolver.insert_new_award_data(comment, award_dict)
        comment = AwardResolver.delete_old_reward_keys(comment)
        return comment

    @staticmethod
    def parse_associated_award(comment: dict) -> dict:
        award_dict = {"total": {"value": 0, "count": 0}, "unique": {}}
        name = comment["associated_award"]["name"]
        price = comment["associated_award"]["coin_price"]
        count = 1
        value = price
        award_dict["total"]["count"] += count
        award_dict["total"]["value"] += value
        award_dict["unique"][name] = dict()
        award_dict["unique"][name]["count"] = count
        award_dict["unique"][name]["price"] = price
        award_dict["unique"][name]["value"] = value
        comment = AwardResolver.insert_new_award_data(comment, award_dict)
        comment = AwardResolver.delete_old_reward_keys(comment)
        return comment

    @staticmethod
    def parse_gildings(comment: dict) -> dict:
        award_dict = {"total": {"value": 0, "count": 0}, "unique": {}}
        for award_id, award_count in comment["gildings"].items():
            if award_count:
                name = AWARD_DICT[award_id]["name"]
                price = AWARD_DICT[award_id]["cost"]
                count = award_count
                value = price * count
                award_dict["total"]["count"] += count
                award_dict["total"]["value"] += value
                award_dict["unique"][name] = dict()
                award_dict["unique"][name]["count"] = count
                award_dict["unique"][name]["price"] = price
                award_dict["unique"][name]["value"] = value
        comment = AwardResolver.insert_new_award_data(comment, award_dict)
        comment = AwardResolver.update_awarders(comment)
        comment = AwardResolver.delete_old_reward_keys(comment)
        return comment

    @staticmethod
    def parse_gilded(comment: dict) -> dict:
        award_dict = {"total": {"value": 0, "count": 0}, "unique": {}}
        name = "Gold"
        price = 500
        count = comment["gilded"]
        value = price * count
        if count:
            award_dict["total"]["count"] += count
            award_dict["total"]["value"] += value
            award_dict["unique"][name] = dict()
            award_dict["unique"][name]["count"] = count
            award_dict["unique"][name]["price"] = price
            award_dict["unique"][name]["value"] = value
        comment = AwardResolver.insert_new_award_data(comment, award_dict)
        comment = AwardResolver.delete_old_reward_keys(comment)
        return comment

    @staticmethod
    def process(comment: dict) -> None:
        if "all_awardings" in comment.keys():
            if len(comment["all_awardings"]):
                return AwardResolver.parse_all_awardings(comment)
        if "associated_award" in comment.keys():
            if comment["associated_award"] is not None:
                return AwardResolver.parse_associated_award(comment)
        if "gildings" in comment.keys():
            if len(comment["gildings"]):
                return AwardResolver.parse_gildings(comment)
        if "gilded" in comment.keys():
            if isinstance(comment["gilded"], int):
                return AwardResolver.parse_gilded(comment)
        raise Exception("no rewards keys")


class CommentHandler:
    @staticmethod
    def delete_unused(comment: dict) -> dict:
        for key in KEYS_UNUSED:
            if key in comment.keys():
                del comment[key]
        return comment

    @staticmethod
    def filter_keys(comment: dict) -> dict:
        out = dict()
        for key in comment.keys():
            if key in KEYS_FILTERED:
                out[key] = comment[key]
        return out

    @staticmethod
    def rename_keys(comment: dict) -> dict:
        comment["flair"] = comment.pop("author_flair_text")
        comment["created"] = comment.pop("created_utc")
        return comment

    @staticmethod
    def convert_edited(comment: dict) -> dict:
        comment["edited"] = comment["edited"] is not False
        return comment

    @staticmethod
    def is_root_comment(comment: dict) -> dict:
        comment["root"] = comment["parent_id"][:3] == "t3_"
        return comment

    @staticmethod
    def reformat_id(comment: dict) -> dict:
        comment["id.comment"] = comment.pop("id")
        comment["id.parent"] = comment.pop("parent_id")[3:]
        comment["id.post"] = comment.pop("link_id")[3:]
        return comment

    @staticmethod
    def parse(comment: dict) -> dict:
        comment = CommentHandler.filter_keys(comment)
        comment = CommentHandler.rename_keys(comment)
        # comment = CommentHandler.convert_edited(comment)
        comment = CommentHandler.is_root_comment(comment)
        comment = CommentHandler.reformat_id(comment)
        # comment = AwardResolver.process(comment)
        comment = AwardResolver.delete_old_reward_keys(comment)
        return comment

    @staticmethod
    def ingest(comments: list[dict], verbose: bool = False) -> list[dict]:
        for i in tqdm(range(len(comments)), disable=not verbose):
            comments[i] = CommentHandler.parse(comments[i])
        return comments
