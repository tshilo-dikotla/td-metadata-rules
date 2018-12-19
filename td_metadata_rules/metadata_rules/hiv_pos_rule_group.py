from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata_rules import CrfRule, CrfRuleGroup, register

from ..predicates import Predicates

app_label = 'td_maternal'
pc = Predicates()


@register()
class HivPosRuleGroup(CrfRuleGroup):
    hiv_pos = CrfRule(
        predicate=pc.func_mother_pos,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[('td_maternal', 'maternalrando'),
                       ('td_maternal', 'maternalinterimidcc'),
                       ('td_maternal', 'maternalhivinterimhx'),
                       ('td_maternal', 'maternalarvpreg'),
                       ('td_maternal', 'maternallifetimearvhistory'),
                       ('td_maternal', 'maternalarvpost'),
                       ('td_maternal', 'maternalarvpostadh')])
