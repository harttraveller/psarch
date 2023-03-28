class Comment:
    @staticmethod
    def convert_edited(edited: int | bool) -> bool:
        return edited is not False

    @staticmethod
    def is_top_level_comment(parent_id: str) -> bool:
        return parent_id[:3] == "t3_"

    @staticmethod
    def combine_awards(
        gilded: int, all_awardings, associated_award, gildings: int, top_awarded_type
    ):
        pass

    @staticmethod
    def handler(comment: dict) -> dict:
        # ? edited: convert edited to bool
        if "edited" in comment.keys():
            comment["edited"] = Comment.convert_edited(comment["edited"])

        # * parent_id: leave in

        # ? top_level: infer if top level comment from parent id
        if "parent_id" in comment.keys():
            comment["top_level"] = Comment.is_top_level_comment(comment["parent_id"])

        # * id: leave in

        # * author_flair_text: leave in

        # * author: leave in

        # ! retrieved_on: delete
        if "retrieved_on" in comment.keys():
            del comment["retrieved on"]

        # ! distinguished: delete
        if "distinguished" in comment.keys():
            del comment["distinguished"]

        # ! gilded: delete
        if "gilded" in comment.keys():
            del comment["gilded"]
