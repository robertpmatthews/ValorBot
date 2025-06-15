import concurrent.futures
import Main_Functions


def multiple_summoners_threading(players, region):
    new_dict = {}
    new_dict_final = {}
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for key, value in players.items():
            new_dict[key] = executor.submit(Main_Functions.get_tier_faster, value, region)

        for key, value in new_dict.items():
            new_dict_final[key] = value.result()

    return new_dict_final
