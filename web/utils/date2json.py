def to_json(all_vendors):
    v = [ven.to_dict() for ven in all_vendors]
    return v
