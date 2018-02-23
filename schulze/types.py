from abc import ABCMeta, abstractmethod

from typing import Any, Dict, Hashable, List, Tuple, TypeVar


class _Comparable(Hashable, metaclass=ABCMeta):
    @abstractmethod
    def __lt__(self, other: Any) -> bool: ...


Comparable = TypeVar('Comparable', bound=_Comparable)
Candidate = Comparable
Candidates = List[Candidate]
Ballots = List[Tuple[Tuple[Tuple[Candidate, ...], ...], int]]
RatedCandidates = Dict[Candidate, int]
ConvertResult = Tuple[Candidates, Ballots]
