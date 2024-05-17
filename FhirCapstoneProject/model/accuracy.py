# Authors: Iain Richey
# Description: contains the current accuracy model we are using

def calc_accuracy(ep_responses: list, model_output: dict) -> list:
    """
    Calculates the accuracy score of endpoint responses to a specific query, based off
    of the analysis model output.

    Calculation is based off of how many elements an endpoint output shared with the anaylsis model output divided by total number

    :param parameters: A list of dicts (endpoint responses) and a dict that is the output of our model.
    :return: The resulting list of flattened data, now with an accuracy score on each.
    """
    acc_output = ep_responses
    query_num = 0
    for query in acc_output:  # loop through each endpoint query
        query_num += 1
        if query is not None:  # some endpoints might not have the person

            # matches unique features (ie no repeats)
            acc_score = 0
            for index, (key, value) in enumerate(query.items()):
                if value == model_output[key] and key != "Endpoint":
                    acc_score += 1

            query["Accuracy"] = round(
                acc_score / (len(model_output) - 1), 2
            )  # -1 for endpoint

    return acc_output
