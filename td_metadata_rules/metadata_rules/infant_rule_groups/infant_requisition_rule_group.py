from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata_rules import RequisitionRule, RequisitionRuleGroup, register
from td_labs import dbs_panel, dna_pcr, infant_elisa_panel

from ...predicates import InfantPredicates


app_label = 'td_infant'
pc = InfantPredicates()


@register()
class InfantRequisitionRuleGroup(RequisitionRuleGroup):

    require_dna_pcr = RequisitionRule(
        predicate=pc.func_infant_heu_require_pcr,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_panels=[dna_pcr])

    require_dbs = RequisitionRule(
        predicate=pc.func_require_infant_dbs,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_panels=[dbs_panel])

    require_elisa = RequisitionRule(
        predicate=pc.func_require_infant_elisa,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_panels=[infant_elisa_panel])

    class Meta:
        app_label = app_label
        source_model = f'{app_label}.infantvisit'
        requisition_model = f'{app_label}.infantrequisition'
