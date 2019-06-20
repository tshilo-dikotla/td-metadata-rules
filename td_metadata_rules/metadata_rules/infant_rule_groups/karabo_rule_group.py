from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata_rules import CrfRule, CrfRuleGroup, register
from edc_metadata_rules import RequisitionRuleGroup, RequisitionRule
from td_labs import karabo_wb_pbmc_pl_panel, infant_paxgene_panel

from ...predicates import InfantPredicates

app_label = 'td_infant'
pc = InfantPredicates()


@register()
class KaraboTbRuleGroup(CrfRuleGroup):

    require_tb_form = CrfRule(
        predicate=pc.is_karabo_eligible,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[(f'{app_label}.karabotuberculosishistory')])

    class Meta:
        app_label = app_label
        source_model = f'{app_label}.infantvisit'


@register()
class KaraboOffstudyRuleGroup(CrfRuleGroup):

    show_offstudy = CrfRule(
        predicate=pc.show_karabo_offstudy,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[(f'{app_label}.karabooffstudy')])

    class Meta:
        app_label = app_label
        source_model = f'{app_label}.karabotuberculosishistory'


@register()
class KaraboRequisitionRuleGroup(RequisitionRuleGroup):
    
    require_heu_requisitions = RequisitionRule(
        predicate=pc.func_show_karabo_requisitions,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_panels=[infant_paxgene_panel, karabo_wb_pbmc_pl_panel])

    class Meta:
        app_label = app_label
        source_model = f'{app_label}.infantvisit'
        requisition_model = f'{app_label}.infantrequisition'
