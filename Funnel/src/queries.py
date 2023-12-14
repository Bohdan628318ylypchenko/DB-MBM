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
                     (OutId, Birth, SEXTYPENAME, 
                     REGNAME, AREANAME, TERNAME, REGTYPENAME, TerTypeName, ClassProfileNAME, ClassLangName, 
                     EONAME, EOTYPENAME, EORegName, EOAreaName, EOTerName, EOParent,
                     UkrTest, UkrTestStatus, UkrBall100, UkrBall12, UkrBall, UkrAdaptScale, UkrPTName, UkrPTRegName, UkrPTAreaName, UkrPTTerName,
                     HistTest, HistLang, HistTestStatus, HistBall100, HistBall12, HistBall, HistPTName, HistPTRegName, HistPTAreaName, HistPTTerName, 
                     MathTest, MathLang, MathTestStatus, MathBall100, MathBall12, MathBall, MathPTName, MathPTRegName, MathPTAreaName, MathPTTerName,
                     PhysTest, PhysLang, PhysTestStatus, PhysBall100, PhysBall12, PhysBall, PhysPTName, PhysPTRegName, PhysPTAreaName, PhysPTTerName,
                     ChemTest, ChemLang, ChemTestStatus, ChemBall100, ChemBall12, ChemBall, ChemPTName, ChemPTRegName, ChemPTAreaName, ChemPTTerName,
                     BioTest, BioLang, BioTestStatus, BioBall100, BioBall12, BioBall, BioPTName, BioPTRegName, BioPTAreaName, BioPTTerName,
                     GeoTest, GeoLang, GeoTestStatus, GeoBall100, GeoBall12, GeoBall, GeoPTName, GeoPTRegName, GeoPTAreaName, GeoPTTerName,
                     EngTest, EngTestStatus, EngBall100, EngBall12, EngDPALevel, EngBall, EngPTName, EngPTRegName, EngPTAreaName, EngPTTerName,
                     FraTest, FraTestStatus, FraBall100, FraBall12, FraDPALevel, FraBall, FraPTName, FraPTRegName, FraPTAreaName, FraPTTerName,
                     DeuTest, DeuTestStatus, DeuBall100, DeuBall12, DeuDPALevel, DeuBall, DeuPTName, DeuPTRegName, DeuPTAreaName, DeuPTTerName,
                     SpaTest, SpaTestStatus, SpaBall100, SpaBall12, SpaDPALevel, SpaBall, SpaPTName, SpaPTRegName, SpaPTAreaName, SpaPTTerName,
                     YearOfAttempt) 
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