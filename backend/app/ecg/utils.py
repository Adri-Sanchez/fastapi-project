from typing import List
from .models import Lead

def count_zero_crossings(leads: List[Lead]) -> dict:
    zero_crossings = {}

    for lead in leads:
        zero_crossings[lead.identifier] = 0

        for i in range(1, len(lead.signal)):
            if (lead.signal[i - 1] > 0 > lead.signal[i]) or (lead.signal[i - 1] < 0 < lead.signal[i]):
                zero_crossings[lead.identifier] += 1

    return zero_crossings
