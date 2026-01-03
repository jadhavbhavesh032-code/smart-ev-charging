
def recommend_station(battery, distance, stations):
    """
    battery: current battery percentage (0–100)
    distance: distance to destination (km)
    stations: list of stations from DB
    """

    reachable_stations = []

    # Assume: 1% battery ≈ 1 km (simple heuristic)
    max_distance = battery * 1

    for s in stations:
        name, location, chargers, price, green_score = s

        if max_distance >= distance:
            score = (green_score * 2) - price
            reachable_stations.append((score, s))

    if not reachable_stations:
        return None

    # Pick station with highest score
    reachable_stations.sort(reverse=True, key=lambda x: x[0])
    return reachable_stations[0][1]
