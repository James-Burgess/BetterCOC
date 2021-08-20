from time import sleep
import json

from loguru import logger

from ..coc_connector import CoC
from .. import db


def watch_game(game_id: str, session_id: str) -> dict:
    """
    Collect stats on game until complete:
        - wait for start of game
        - list players in game
        - get game question
        - wait for game complete
        - save stats
    :param game_id: id of the started coc game
    :param session_id: id of the session to save to
    :return: Object: stats of the watched game
    """
    coc = CoC()
    cnxn = db.create_connection()
    
    game = db.get_game(cnxn, game_id)

    if game and game.get("finished"):
        logger.debug("Game already saved")
        return game
    elif not game:
        db.add_game(cnxn, session_id, game_id)

    test_saved = True

    while 1:
        stats = coc.get_game_stats(game_id)
        db.update_game(cnxn, stats)

        if stats.get("finished"):
            logger.debug("Match Complete.")
            sleep(30)
            stats = coc.get_game_stats(game_id)
            db.update_game(cnxn, stats)
            return db.get_game(cnxn, game_id)

        if stats.get("started"):
            logger.debug("Match in progress")
            if not test_saved:
                test = coc.get_test(stats.get("test_id"))
                db.add_test(cnxn, test, game_id)
                test_saved = True

        else:
            logger.debug("Waiting for match to start")

        sleep(5)


def _test():
    watch_game("", "test-session")
    cnxn = db.create_connection()
    game = db.list_games(cnxn)[-1]
    logger.info(json.dumps(game, indent=4, sort_keys=True))


if __name__ == "__main__":
    _test()
