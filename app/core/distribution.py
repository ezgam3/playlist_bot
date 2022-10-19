"""Module helps to distribute playlists between users."""

from random import shuffle

from loguru import logger


def distribute_playlists(members: list[int]) -> dict[int, list[int]]:
    """Distribute playlists between users.

    Args:
        members (list[int]): List of telegram ids.

    Returns:
        dict[int, list[int]]: Dict with telegram id as key and list of
            telegrams_id ids, the order of listening to playlists as value.
    """
    members_count = len(members)
    shuffle(members)
    logger.debug("Shuffled members={}", members)
    result = dict()
    for i in range(members_count):
        playlist = members.copy()
        playlist = playlist[i:] + playlist[:i]
        result[members[i]] = playlist[1:]
    return result


if __name__ == "__main__":
    print(distribute_playlists([1, 2, 3, 4, 5]))
