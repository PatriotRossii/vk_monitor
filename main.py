import typer
import vk
import pandas as pd
import time
import matplotlib.pyplot as plt
import schedule


VK_API_VERSION = "5.131"
timeseries_data = {"date": [], "online": []}


def plot(output_filename: str):
    dataframe = pd.DataFrame(timeseries_data, columns=[
        "date", "online"
    ]).set_index("date")

    plt.plot(dataframe["online"], marker="o")
    plt.xlabel("date")
    plt.ylabel("online")

    plt.savefig(output_filename)


def ping(api: vk.API, user_id: int) -> bool:
    return api.users.get(user_id=user_id, fields="online")[0]["online"]


def tick(api: vk.API, user_id: int, output_filename: str):
    timeseries_data["online"].append(ping(api, user_id))
    timeseries_data["date"].append(pd.to_datetime(time.time(), unit="s"))
    plot(output_filename)


def main(access_token: str, user_id: int, output_filename: str, seconds: int = 300):
    api = vk.API(vk.Session(), access_token=access_token, v=VK_API_VERSION)
    schedule.every(seconds).seconds.do(tick, api=api, user_id=user_id, output_filename=output_filename)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    typer.run(main)