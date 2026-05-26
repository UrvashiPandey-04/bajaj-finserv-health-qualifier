from app.config import settings
from app.utils.logger import logger
from app.utils.helpers import is_odd_registration

# ==============================================================================
# SQL QUESTION 1 (ODD REGISTRATION NUMBER)
# ==============================================================================

# PostgreSQL Syntax
SQL_QUESTION_1_POSTGRESQL = """SELECT 
    p.AMOUNT AS SALARY,
    (e.FIRST_NAME || ' ' || e.LAST_NAME) AS NAME,
    EXTRACT(YEAR FROM AGE(CURRENT_DATE, e.DOB)) AS AGE,
    d.DEPARTMENT_NAME
FROM PAYMENTS p
JOIN EMPLOYEE e ON p.EMP_ID = e.EMP_ID
JOIN DEPARTMENT d ON e.DEPARTMENT = d.DEPARTMENT_ID
WHERE EXTRACT(DAY FROM p.PAYMENT_TIME) != 1
ORDER BY p.AMOUNT DESC
LIMIT 1;"""

# MySQL / MariaDB Syntax
SQL_QUESTION_1_MYSQL = """SELECT 
    p.AMOUNT AS SALARY,
    CONCAT(e.FIRST_NAME, ' ', e.LAST_NAME) AS NAME,
    TIMESTAMPDIFF(YEAR, e.DOB, CURDATE()) AS AGE,
    d.DEPARTMENT_NAME
FROM PAYMENTS p
JOIN EMPLOYEE e ON p.EMP_ID = e.EMP_ID
JOIN DEPARTMENT d ON e.DEPARTMENT = d.DEPARTMENT_ID
WHERE DAY(p.PAYMENT_TIME) != 1
ORDER BY p.AMOUNT DESC
LIMIT 1;"""


# ==============================================================================
# SQL QUESTION 2 (EVEN REGISTRATION NUMBER)
# ==============================================================================

# Fully dialect-agnostic standard SQL (Works on SQLite, MySQL, PostgreSQL, etc.)
# Logic: Employee A is younger than Employee B if A.DOB > B.DOB (born later means younger)
SQL_QUESTION_2_DIALECT_AGNOSTIC = """SELECT 
    e.EMP_ID, 
    e.FIRST_NAME, 
    e.LAST_NAME, 
    d.DEPARTMENT_NAME,
    (
        SELECT COUNT(*) 
        FROM EMPLOYEE e2 
        WHERE e2.DEPARTMENT = e.DEPARTMENT 
          AND e2.DOB > e.DOB
    ) AS YOUNGER_EMPLOYEES_COUNT
FROM EMPLOYEE e
JOIN DEPARTMENT d ON e.DEPARTMENT = d.DEPARTMENT_ID
ORDER BY e.EMP_ID DESC;"""


def get_sql_query(reg_no: str, dialect: str = "postgresql") -> str:
    """
    Selects the correct SQL query string based on the registration number's last digit.
    
    Odd Last Digit:
        Returns SQL Question 1 (highest salary, combined name, age, dept, 
        excluding transactions on the 1st of any month).
        
    Even Last Digit:
        Returns SQL Question 2 (number of younger employees in the same department).
        
    Args:
        reg_no: The registration number.
        dialect: SQL dialect style ('postgresql' or 'mysql').
        
    Returns:
        The exact SQL query string.
    """
    logger.info("==================================================")
    logger.info("PHASE 2: RESOLVING SQL QUERY SELECTION")
    logger.info("==================================================")
    
    # Check registration number last digit parity
    is_odd = is_odd_registration(reg_no)
    
    if is_odd:
        logger.info("-> Registration number is ODD. Selecting SQL Question 1.")
        if dialect == "mysql":
            logger.info("-> Using MySQL dialect for Question 1.")
            query = SQL_QUESTION_1_MYSQL
        else:
            logger.info("-> Using PostgreSQL dialect for Question 1.")
            query = SQL_QUESTION_1_POSTGRESQL
    else:
        logger.info("-> Registration number is EVEN. Selecting SQL Question 2.")
        logger.info("-> Using dialect-agnostic Standard SQL for Question 2.")
        query = SQL_QUESTION_2_DIALECT_AGNOSTIC
        
    logger.info("Selected SQL Query:")
    logger.info(f"\n{query}\n")
    return query
