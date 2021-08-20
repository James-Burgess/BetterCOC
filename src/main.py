from time import sleep
import json

from dotenv import find_dotenv, load_dotenv

from coc_connector import CoC
import db

load_dotenv(find_dotenv())


def watch_game(game_id):
    """
    Collect stats on game until complete
    :param game_id: id of the started coc game
    :return: Object: stats of the watched game
    """

    # wait for start of game
    # list players in game
    # get game question
    # wait for game complete
    # save stats
    coc = CoC()
    cnxn = db.create_connection()
    game = db.get_game(cnxn, game_id)

    if game and game.get("finished"):
        print("Game already saved")
        return
    elif not game:
        db.add_game(cnxn, 'test-session', game_id)

    test_saved = True

    while 1:
        stats = coc.get_game_stats(game_id)
        db.update_game(cnxn, stats)

        started = stats.get("started")
        finished = stats.get("finished")

        if finished:
            print("Match Complete.")
            sleep(30)
            stats = coc.get_game_stats(game_id)
            db.update_game(cnxn, stats)
            return

        if started:
            print("Match in progress")
            if not test_saved:
                test = coc.get_test(stats.get("test_id"))
                db.add_test(cnxn, test, game_id)
                test_saved = True

        else:
            print("Waiting for match to start")

        sleep(5)


if __name__ == "__main__":
    # create session
    # get url
    # monitor game in thread
    # ingest url or show stats

    cnxn = db.create_connection()

    watch_game("")

    game = db.list_games(cnxn)
    print(json.dumps(game, indent=4, sort_keys=True))
