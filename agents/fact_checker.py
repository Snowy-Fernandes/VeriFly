def fact_check_claim(claim, live_weather, num_sources=1):
    claim_low = claim.lower()
    status = (live_weather.get("status", "") or "").lower()

    base_prob = 50

    if "rain" in claim_low:
        if "rain" in status or "shower" in status:
            base_prob = 70
        else:
            base_prob = 20
    elif "sun" in claim_low or "clear" in claim_low:
        if "clear" in status or "sun" in status:
            base_prob = 70
        elif "cloud" in status:
            base_prob = 50
        else:
            base_prob = 20

    prob = min(100, base_prob + 5 * (num_sources - 1))

    if prob > 75:
        flag = "🟢"
        note = "Strongly supported by data and multiple sources"
    elif prob > 45:
        flag = "🟡"
        note = "Partly supported, check carefully"
    else:
        flag = "🔴"
        note = "Not supported, likely false"

    return flag, prob, note
