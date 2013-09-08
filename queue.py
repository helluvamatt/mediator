from readjson import read_json

class TorrentQueues:

    def __init__(self, settings_file):

        self.settings_file = settings_file
        self.json_file = read_json(settings_file)
        self.todo_size, self.history_size, self.delta_size = -1, -1, -1
        self.todo_list, self.history_list, self.delta_list = [], [], []
        self.get_queue_size()

    def get_queue_size(self):

        with open(self.json_file["todo-log"]) as todo_items:
            for self.todo_size, n in enumerate(todo_items):
                pass

        with open(self.json_file["history-log"]) as history_items:
            for self.history_size, n in enumerate(history_items):
                pass

        with open(self.json_file["delta-log"]) as delta_items:
            for self.delta_size, n in enumerate(delta_items):
                pass
        return self.todo_size + 1, self.history_size + 1, self.delta_size + 1

    def get_queue(self, todo=False, history=False, delta=False):

        self.get_queue_size()

        # print one
        if (self.todo_size > -1) and todo:
            with open(self.json_file["todo-log"]) as todo_items:
                for torrent in todo_items:
                    self.todo_list.append(torrent)
            return self.todo_list

        if (self.history_size > -1) and history:
            with open(self.json_file["history-log"]) as history_items:
                for torrent in history_items:
                    self.history_list.append(torrent)
            return self.history_list

        if (self.delta_size > -1) and delta:
            with open(self.json_file["delta-log"]) as delta_items:
                for torrent in delta_items:
                    self.delta_list.append(torrent)
            return self.delta_list