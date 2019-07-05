from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata_rules import CrfRule, CrfRuleGroup, register, P

from ...predicates import MaternalPredicates

app_label = 'td_maternal'
pc = MaternalPredicates()


@register()
class MaternalAntenatalEnrollmentRuleGroup(CrfRuleGroup):

    maternal_ultrasound_neg = CrfRule(
        predicate=P('number_of_gestations', 'eq', '1'),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.maternalobstericalhistory',
                       f'{app_label}.maternalmedicalhistory',
                       f'{app_label}.maternaldemographics',
                       f'{app_label}.maternalclinicalmeasurementsone'])

    class Meta:
        app_label = app_label
        source_model = f'{app_label}.maternalultrasoundinitial'
