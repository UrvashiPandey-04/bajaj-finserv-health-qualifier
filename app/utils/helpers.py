import re
from app.utils.logger import logger

def parse_last_digit(reg_no: str) -> int:
    """
    Parses the registration number to extract its last numerical digit.
    If the last character is not a digit, it searches backwards for the first digit.
    
    Args:
        reg_no: The registration number string (e.g. 'REG12347' or '123456')
        
    Returns:
        The extracted digit as an integer.
        
    Raises:
        ValueError: If no digit is found in the registration number.
    """
    logger.info(f"Parsing registration number '{reg_no}' to determine odd/even logic...")
    
    # Clean the input
    cleaned_reg = reg_no.strip()
    
    # Extract all digits using regular expressions
    digits = re.findall(r"\d", cleaned_reg)
    
    if not digits:
        err_msg = f"Invalid registration number format. No numeric digits found in '{reg_no}'."
        logger.error(err_msg)
        raise ValueError(err_msg)
    
    last_digit = int(digits[-1])
    logger.info(f"Extracted last numerical digit: {last_digit}")
    return last_digit

def is_odd_registration(reg_no: str) -> bool:
    """
    Determines if the last digit of the registration number is odd.
    
    Args:
        reg_no: The registration number.
        
    Returns:
        True if the last numerical digit is odd, False if even.
    """
    last_digit = parse_last_digit(reg_no)
    is_odd = last_digit % 2 != 0
    parity = "ODD" if is_odd else "EVEN"
    logger.info(f"Parity of last digit ({last_digit}) is {parity}.")
    return is_odd
