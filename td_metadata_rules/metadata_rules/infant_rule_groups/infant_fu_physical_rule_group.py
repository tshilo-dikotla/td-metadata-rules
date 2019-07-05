from edc_constants.constants import YES
from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata_rules import CrfRule, CrfRuleGroup, register, P

from ...predicates import InfantPredicates


app_label = 'td_infant'
pc = InfantPredicates()


@register()
class InfantFuPhysicalRuleGroup(CrfRuleGroup):
    physical_assessment_yes = CrfRule(
        predicate=P('physical_assessment', 'eq', YES),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[(f'{app_label}.infantfuphysical')])

    class Meta:
        app_label = app_label
        source_model = f'{app_label}.infantfu'
