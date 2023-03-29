class AwardResolver:
    @staticmethod
    def process(comment: dict) -> None:
        if "associated_award" in comment.keys():
            pass
        elif "all_awardings" in comment.keys():
            pass

    @staticmethod
    def resolve_awards(comment: dict) -> None:
        # TODO: gilded may be necessary for resolving older comments
        # if "gilded" in comment.keys():
        #     del comment["gilded"]
        award_dict = {"total": {"value": 0, "count": 0}, "unique": {}, "awarders": []}
        if "associated_award" in comment.keys():
            if comment["associated_award"] is not None:
                name = comment["associated_award"]["name"]
                price = comment["associated_award"]["coin_price"]
                count = 1
                value = comment["associated_award"]["coin_price"]
                award_dict["total"]["count"] += count
                award_dict["total"]["value"] += value
                award_dict["unique"][name] = dict()
                award_dict["unique"][name]["count"] = count
                award_dict["unique"][name]["price"] = price
                award_dict["unique"][name]["value"] = value
            del comment["associated_award"]
        if "all_awardings" in comment.keys():
            if len(comment["all_awardings"]):
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
            del comment["all_awardings"]
        comment["awards"] = award_dict
        if "awarders" in comment.keys():
            comment["awards"]["awarders"] = comment["awarders"]
            del comment["awarders"]
        if "top_awarded_type" in comment.keys():
            del comment["top_awarded_type"]
        if "total_awards_received" in comment.keys():
            del comment["total_awards_received"]
