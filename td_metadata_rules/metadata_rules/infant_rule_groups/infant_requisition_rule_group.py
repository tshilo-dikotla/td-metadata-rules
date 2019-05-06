from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata_rules import RequisitionRule, RequisitionRuleGroup, register
from td_labs import dbs_panel, dna_pcr, infant_elisa_panel

from ...predicates import InfantPredicates


app_label = 'td_infant'
pc = InfantPredicates()


@register()
class InfantRequisitionRuleGroup(RequisitionRuleGroup):

    require_heu_requisitions = RequisitionRule(
        predicate=pc.func_infant_heu,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_panels=[dna_pcr, dbs_panel, infant_elisa_panel])

    class Meta:
        app_label = app_label
        source_model = f'{app_label}.infantvisit'
        requisition_model = f'{app_label}.infantrequisition'
