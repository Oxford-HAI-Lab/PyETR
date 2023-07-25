from pyetr.dependency import DependencyRelation
from pyetr.parsing.parse_string import Implies, Item, Quantified
from pyetr.stateset import set_of_states
from pyetr.term import ArbitraryObject
from pyetr.view import View


def unparse_set_of_states(s: set_of_states) -> Item:
    print(s)
    raise NotImplementedError


def get_quantifiers(
    arb_objects: set[ArbitraryObject], dep_rel: DependencyRelation
) -> list[Quantified]:
    raise NotImplementedError


def unparse_view(v: View) -> list[Item]:
    main_item: Item
    if v.supposition.is_verum:
        main_item = unparse_set_of_states(v.stage)
    else:
        stage = unparse_set_of_states(v.stage)
        supposition = unparse_set_of_states(v.supposition)
        main_item = Implies([[supposition, stage]])
    all_arb = v.stage.arb_objects | v.supposition.arb_objects
    output: list[Quantified] = get_quantifiers(all_arb, v.dependency_relation)
    return [*output, main_item]
