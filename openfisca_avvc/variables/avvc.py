from openfisca_core.periods import MONTH 
from openfisca_core.variables import Variable 
from openfisca_avvc.entities import Household
from numpy import select


class code_organisme(Variable):
    value_type = int
    entity = Household
    definition_period = MONTH

class montant_smic_35h(Variable):
    value_type = float
    entity = Household
    definition_period = MONTH

    def formula(household, period, parameters):
        code_orga = household("code_organisme", period)
        smic_mayotte = parameters(period).avvc.smic_net_35h_mayotte
        smic_met = parameters(period).avvc.smic_net_35h_met_dom
        if code_orga >= 976:
            return smic_mayotte
        else:
            return smic_met

class nombre_enfant_charge(Variable):
    value_type = int
    entity = Household
    definition_period = MONTH
    default_value = 0


class type_aide(Variable):
    value_type = str
    entity = Household
    definition_period = MONTH

    def formula(household, period):
        nb_enfant_charge = household("nombre_enfant_charge", period)
        total_des_ressources = household("total_ressources_foyer", period)
        smic_35h = household("montant_smic_35h", period)
        cas_possibles = [(nb_enfant_charge == 0) & (total_des_ressources > (1.5 * smic_35h)), 
                         (nb_enfant_charge == 1) & (total_des_ressources > (2.25 * smic_35h)), 
                         (nb_enfant_charge == 2) & (total_des_ressources > (2.7 * smic_35h)),
                         (nb_enfant_charge >= 3) & (total_des_ressources > (3.3 * smic_35h))
                         ]
        return select(
            cas_possibles, ["pret", "pret", "pret", "pret"], default="aide"
        )
        # print(result[0])
        # match (nb_enfant_charge, total_des_ressources, smic_35h):
        #     case (0, total_des_ressources) if total_des_ressources > (1.5 * smic_35h):
        #         return "pret"
        #     case (1, total_des_ressources) if total_des_ressources > (2.25 * smic_35h):
        #         return "pret"
        #     case (2, total_des_ressources) if total_des_ressources > (2.7 * smic_35h):
        #         return "pret"
        #     case (nb_enfant_charge, total_des_ressources) if nb_enfant_charge >= 3 and total_des_ressources > (3.3 * smic_35h):
        #         return "pret"
        #     case _:
        #         return "aide"


class montant_avvc_majore(Variable):
    value_type = float
    entity = Household
    definition_period = MONTH

    def formula(household, period, parameters):
        code_orga = household("code_organisme", period)
        nb_enfant_charge = household("nombre_enfant_charge", period)
        montant_base_rsa = parameters(period).avvc.montant_forfaitaire_RSA_mayotte if code_orga >= 970 else parameters(period).avvc.montant_forfaitaire_RSA_met_dom
        
        match(nb_enfant_charge):
            case 0:
                return montant_base_rsa
            case 1:
                return montant_base_rsa * 1.5
            case 2:
                return montant_base_rsa * 1.8
            case 3:
                return montant_base_rsa * 2.2
            case _:
                return montant_base_rsa * (2.2 + ((nb_enfant_charge - 3) * 0.4))


class taux_minoration_avvc(Variable):
    value_type = float
    entity = Household
    definition_period = MONTH

    def formula(household, period):

        total_des_ressources = household("total_ressources_foyer", period)
        mont_smic_35h = household("montant_smic_35h", period)
        match(total_des_ressources):
            case total_des_ressources if mont_smic_35h * 0.5 <= total_des_ressources < mont_smic_35h:
                return 0.2
            case total_des_ressources if mont_smic_35h <= total_des_ressources < mont_smic_35h * 1.5:
                return 0.4
            case total_des_ressources if mont_smic_35h * 1.5 <= total_des_ressources:
                return 0.6
            case _: 0


class montant_avvc(Variable):
    value_type = float
    entity = Household
    definition_period = MONTH

    def formula(household, period):
        montant_avvc_maj = household("montant_avvc_majore", period)
        taux_minoration = household("taux_minoration_avvc", period)

        return (montant_avvc_maj * (1 - taux_minoration))
