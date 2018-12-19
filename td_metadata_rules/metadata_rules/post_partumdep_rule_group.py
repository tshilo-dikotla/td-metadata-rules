from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata_rules import CrfRule, CrfRuleGroup, register

from ..predicates import Predicates

app_label = 'td_maternal'
pc = Predicates()


@register()
class PostPartumDepressionRuleGroup(CrfRuleGroup):
    post_partumdepression = CrfRule(
        predicate=pc.func_show_postpartum_depression,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[(f'{app_label}.maternalpostpartumdep')])

    class Meta:
        app_label = app_label
