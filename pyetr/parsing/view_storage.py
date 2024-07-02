from dataclasses import dataclass
from typing import Optional

from pyetr.dependency import DependencyRelation
from pyetr.issues import IssueStructure
from pyetr.stateset import Stage, Supposition
from pyetr.weight import Weights


@dataclass
class ViewStorage:
    stage: Stage
    supposition: Supposition
    dependency_relation: DependencyRelation
    issue_structure: IssueStructure
    weights: Optional[Weights]
    is_pre_view: bool = False
