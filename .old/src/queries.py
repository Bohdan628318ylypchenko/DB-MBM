class Query:
    """
    Represents sql query (template + args).
    """
    def __init__(self, template: str, q_args: tuple,
                 expect_return: bool):
        self._template = template
        self._q_args = q_args
        self._expect_return = expect_return

    def get_template(self) -> str:
        """
        Template getter.
        """
        return self._template
    
    def get_q_args(self) -> tuple:
        """
        Query args getter.
        """
        return self._q_args

    def expect_return(self) -> bool:
        """
        Expect return getter.
        """
        return self._expect_return


class QueryTemplates:
    """
    Placeholder for query templates
    """

    COMPLETED_TRANSACTION_COUNT = """
                                  SELECT completed
                                  FROM TransactionCounter
                                  """
    INCREMENT_COMPLETED_TRANSACTION_COUNT = """
                                            UPDATE TransactionCounter
                                            SET completed = completed + 1
                                            """
    INSERT_ZNO = """
                 INSERT INTO Zno (OutId, Birth, SEXTYPENAME, REGNAME, AREANAME, TERNAME, REGTYPENAME, TerTypeName, ClassProfileNAME, ClassLangName, EONAME, EOTYPENAME, EORegName, EOAreaName, EOTerName, EOParent,
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
                 VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                 """

    AVG_UKR_PASSED_BY_REGION = """
                               SELECT d2019.RegName, d2019.Ball, d2020.Ball AS test
                               FROM 
                               (
                                   SELECT RegName, AVG(UkrBall100) AS Ball 
                                   FROM Zno
                                   WHERE YearOfAttempt = 2019 AND UkrTestStatus = 'Зараховано'
                                   GROUP BY RegName
                               ) d2019
                               FULL OUTER JOIN
                               (
                                   SELECT RegName, AVG(UkrBall100) AS Ball 
                                   FROM Zno
                                   WHERE YearOfAttempt = 2020 AND UkrTestStatus = 'Зараховано'
                                   GROUP BY RegName
                               ) d2020
                               ON (d2019.RegName = d2020.RegName)
                               """