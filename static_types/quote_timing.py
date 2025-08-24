from enum import Enum

class QuoteTiming(str, Enum):
  OPEN = 'Open'
  CLOSE = 'Close'
  HIGH = 'High'
  LOW = 'Low'
  
