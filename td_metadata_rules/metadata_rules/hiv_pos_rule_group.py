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
        target_models=[(f'{app_label}.maternalrando'),
                       (f'{app_label}.maternalinterimidcc'),
                       (f'{app_label}.maternalhivinterimhx'),
                       (f'{app_label}.maternalarvpreg'),
                       (f'{app_label}.maternallifetimearvhistory'),
                       (f'{app_label}.maternalarvpost'),
                       (f'{app_label}.maternalarvpostadh')])

    class Meta:
        app_label = app_label
