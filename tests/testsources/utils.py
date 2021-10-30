import os


def get_resource(filename):
    resources_dir = os.path.join(os.path.dirname(__file__), "../resources")
    return os.path.join(resources_dir, filename)
