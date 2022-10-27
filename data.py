import pickle

global bad_ips, ip_objs, country_dict, postal_code

save_file = 'whois.pkl'
file_to_analyze = 'ips'
# save_file = 'temp.pkl'
# file_to_analyze = 'ips_tmp'

class Data():
    def __init__(self):
        self.bad_ips = []
        self.ip_objs = {}
        self.country_dict = {}
        self.postal_code = {}

    def save_data(self):
        with open(save_file, 'wb') as f:
            pickle.dump(list(vars(self).values()), f)

    def load_data(self):
        try:
            with open(save_file, 'rb') as f:
                self.bad_ips, self.ip_objs, self.country_dict, self.postal_code = pickle.load(f)
        except (ValueError, FileNotFoundError):
            return [], {}, {}, {}

g = Data()

if __name__ == "__main__":
    # Inspect the order of variables on save/load
    # g.load_data()
    print(list(vars(g).keys()))
    print(list(vars(g).values()))
