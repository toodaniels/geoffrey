
def convert_channel(id):
    try:
        return int(id)
    except Exception as e:
        return id