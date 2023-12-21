class Query:
    """
    Represents sql query (template + args).
    """

    def __init__(self, name: str, expression: str, args: tuple, expect_return: bool):
        self._name = name
        self._expression = expression
        self._args = args
        self._expect_return = expect_return

    def get_name(self) -> str:
        return self._name

    def get_expression(self) -> str:
        return self._expression

    def get_args(self) -> tuple:
        return self._args

    def expect_return(self) -> bool:
        return self._expect_return


# noinspection SqlNoDataSourceInspection
class QueryFactory:
    """
    Class - common query creation method holder.
    """

    @staticmethod
    def get_completed_tx_count() -> Query:
        return Query("GET_COMPLETED_TX_COUNT",
                     """
                     SELECT completed_transaction_count FROM funnel_status
                     """,
                     (), True)

    @staticmethod
    def get_funnel_status() -> Query:
        return Query("FUNNEL_STATUS",
                     """
                     SELECT * FROM funnel_status
                     """,
                     (), True)

    @staticmethod
    def set_funnel_status_done() -> Query:
        return Query("SET_FUNNEL_STATUS_DONE",
                     """
                     UPDATE funnel_status
                     SET is_done = TRUE
                     """,
                     (), False)

    @staticmethod
    def insert_zno(query_args: tuple) -> Query:
        return Query("INSERT_ZNO",
                     """
                     INSERT INTO zno 
                     (out_id, birth, sextypename, 
                     regname, areaname, tername, regtypename, tertypename, classprofilename, classlangname, 
                     eoname, eotypename, eoregname, eoareaname, eotertypename, eoparent,
                     ukr_test, ukr_test_status, ukr_ball100, ukr_ball12, ukr_ball, ukr_adapt_scale, ukr_pt_Name, ukr_pt_reg_name, ukr_pt_area_name, ukr_pt_ter_name,
                     hist_test, hist_lang, hist_test_status, hist_ball100, hist_ball12, hist_ball, hist_pt_name, hist_pt_reg_name, hist_pt_area_name, hist_pt_ter_name, 
                     math_test, math_lang, math_test_status, math_ball100, math_ball12, math_ball, math_pt_name, math_pt_reg_name, math_pt_area_name, math_pt_ter_name,
                     phys_test, phys_lang, phys_test_status, phys_ball100, phys_ball12, phys_ball, phys_pt_name, phys_pt_reg_name, phys_pt_area_name, phys_pt_ter_name,
                     chem_test, chem_lang, chem_test_status, chem_ball100, chem_ball12, chem_ball, chem_pt_name, chem_pt_reg_name, chem_pt_area_name, chem_pt_ter_name,
                     bio_test, bio_lang, bio_test_status, bio_ball100, bio_ball12, bio_ball, bio_pt_name, bio_pt_reg_name, bio_pt_area_name, bio_pt_ter_name,
                     geo_test, geo_lang, geo_test_status, geo_ball100, geo_ball12, geo_ball, geo_pt_name, geo_pt_reg_name, geo_pt_area_name, geo_pt_ter_name,
                     eng_test, eng_test_status, eng_ball100, eng_ball12, eng_dpa_level, eng_ball, eng_pt_name, eng_pt_reg_name, eng_pt_area_name, eng_pt_ter_name,
                     fra_test, fra_test_status, fra_ball100, fra_ball12, fra_dpa_level, fra_ball, fra_pt_Name, fra_pt_reg_name, fra_pt_area_name, fra_pt_ter_name,
                     deu_test, deu_test_status, deu_ball100, deu_ball12, deu_dpa_level, deu_ball, deu_pt_name, deu_pt_reg_name, deu_pt_area_name, deu_pt_ter_name,
                     spa_test, spa_test_status, spa_ball100, spa_ball12, spa_dpa_level, spa_ball, spa_pt_Name, spa_pt_reg_name, spa_pt_area_name, spa_pt_ter_name,
                     year_of_attempt) 
                     VALUES 
                     (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                     %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                     %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                     %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                     """,
                     query_args, False)

    @staticmethod
    def increment_completed_transaction_count() -> Query:
        return Query("INCREMENT_COMPLETED_TRANSACTION_COUNT",
                     """
                     UPDATE funnel_status
                     SET completed_transaction_count = completed_transaction_count + 1
                     """,
                     (), False)