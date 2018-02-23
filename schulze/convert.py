from collections import defaultdict
from typing import Any, List, Sequence
from schulze.types import ConvertResult, RatedCandidates


def flatten(nested: Sequence) -> List[Any]:
    result = []
    for item in nested:
        if isinstance(item, list) or isinstance(item, tuple):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result


def convert_rated_candidates(
        rated_candidates_seq: Sequence[RatedCandidates], reverse: bool = True) -> ConvertResult:
    """
    converts a list of rated candidates to a call-args tuple for compute_ranks
    :param rated_candidates_seq: a sequence of dicts where every candidate is mapped to a rating
    :param reverse: whether the rating is inverted or not.

    >>> import pprint
    >>> pprint.pprint(convert_rated_candidates([
    ... dict(a=1, b=2, c=3),
    ... dict(a=1, b=2, c=3),
    ... dict(a=3, b=1, c=2),
    ... dict(b=1, c=3, a=1)]))
    (['a', 'b', 'c'],
     [((('c',), ('b',), ('a',)), 2),
      ((('a',), ('c',), ('b',)), 1),
      ((('c',), ('a', 'b')), 1)])

    >>> import pprint
    >>> pprint.pprint(convert_rated_candidates(flatten([
    ... (dict(a=5, c=4, b=3, e=2, d=1), ) * 5,
    ... (dict(a=5, d=4, e=3, c=2, b=1), ) * 5,
    ... (dict(b=5, e=4, d=3, a=2, c=1), ) * 8,
    ... (dict(c=5, a=4, b=3, e=2, d=1), ) * 3,
    ... (dict(c=5, a=4, e=3, b=2, d=1), ) * 7,
    ... (dict(c=5, b=4, a=3, d=2, e=1), ) * 2,
    ... (dict(d=5, c=4, e=3, b=2, a=1), ) * 7,
    ... (dict(e=5, b=4, a=3, d=2, c=1), ) * 8,
    ... ])))
    (['a', 'b', 'c', 'd', 'e'],
     [((('a',), ('c',), ('b',), ('e',), ('d',)), 5),
      ((('a',), ('d',), ('e',), ('c',), ('b',)), 5),
      ((('b',), ('e',), ('d',), ('a',), ('c',)), 8),
      ((('c',), ('a',), ('b',), ('e',), ('d',)), 3),
      ((('c',), ('a',), ('e',), ('b',), ('d',)), 7),
      ((('c',), ('b',), ('a',), ('d',), ('e',)), 2),
      ((('d',), ('c',), ('e',), ('b',), ('a',)), 7),
      ((('e',), ('b',), ('a',), ('d',), ('c',)), 8)])
    """

    # create a list of rated candidates from the first item of the list
    candidates = sorted(list(list(rated_candidates_seq)[0].keys()))

    candidate_ranking_weights = defaultdict(lambda: 0)
    for rated_candidates in rated_candidates_seq:
        weighted_candidates = defaultdict(list)
        # first create a dict that maps a rating to a list of candidates
        for candidate, rating in rated_candidates.items():
            weighted_candidates[rating].append(candidate)
        # the create a list of tuples that contain a rating and a list of candidates,
        # but ordered by the rating
        ranked_candidates_lists = sorted(weighted_candidates.items(),
                                         key=lambda rcl: rcl[0], reverse=reverse)
        # now strip the rating and keep the candidate lists as tuples
        ranked_candidates = tuple([tuple(sorted(i[1])) for i in ranked_candidates_lists])
        # finally add weight to the item that conforms to this exact order of candidates tuples
        candidate_ranking_weights[ranked_candidates] += 1

    ballots = list(candidate_ranking_weights.items())
    return candidates, ballots


if __name__ == '__main__':
    import doctest

    doctest.testmod()
