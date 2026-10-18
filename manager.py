import pandas as pd, numpy as np

class Manager:
    def __init__(self, board_array):
        self.board_array = board_array
        self.letters = self.get_csv('resources/letters.csv')
        self.current = None
        self.text_data = None # Current text data
        self.clock = 0

    def tick(self):
        # Update the board - all binary data in self.text_array
        self.clock += 1
        self.board_array = np.zeros((70, 15)) #start from column 70 and move to 0 

        if self.clock >= self.text_data["full_pass_duration"]:
            self.text_data = None
            self.current = None
            return

        sub_start = 0
        current_start = (70 - self.clock)
        if current_start < 0:
            sub_start = abs(current_start)
            current_start = 0


        i = 0
        upper_bound = min(70, current_start + (self.text_data["length"] - sub_start))
        for column in range(current_start, upper_bound):
            self.board_array[column][-(1+len(self.text_data["array"][sub_start + i])):-1] = self.text_data["array"][sub_start + i]
            i += 1
        

    def reset_clock(self):
        self.clock = 0

    def static_display(self):
        base = 1
        text = self.current.text.casefold()
        for i, letter in enumerate(text):
            data = self.ret_let_data(letter)
            binary = data['binary']
            inner_base = 0
            for x in range(data['width']):
                binary_column = [bit for q, bit in enumerate(binary)
                                     if q % data['width'] == x]
                self.board_array[base + inner_base][-(1+data['height']):-1] = binary_column
                inner_base += 1
            base += (data['width'] + 1)


    def start_display(self):
        text = self.current.text.casefold()
        text_array = []
        text_binary_array = []
        for letter in text:
            letter_data = self.ret_let_data(letter)
            text_array.append(letter_data)
            for y in range(letter_data['width']):
                sub_binary = []
                for x in range(len(letter_data['binary'])):
                    if x % letter_data['width'] == y:
                        sub_binary.append(letter_data['binary'][x])
                text_binary_array.append(sub_binary)
            text_binary_array.append(self.ret_let_data('letter_gap')['binary'])
        self.text_data = {
            "array": text_binary_array,
            "length": len(text_binary_array),
            "full_pass_duration": 70 + len(text_binary_array)
        }


    def ret_let_data(self, letter):
        if letter ==  " ": letter = 'space'
        letter_row = self.letters.loc[self.letters['letter'] == letter]
        letter_box = letter_row['box'].values[0].split('*')
        return {
            'binary': letter_row['box_on'].values[0],
            'width': int(letter_box[0]),
            'height': int(letter_box[1])
        }

    #Get + Set
    def get_board_array(self):
        return self.board_array
    def get_csv(self, file_path):
        return pd.read_csv(file_path, dtype=str)
    def get_ended_status(self):
        if self.current is None:
            return True
        else: return False

    def set_announcement(self, announcement):
        self.current = announcement
    
    #Print functions
    def print_ann_text(self):
        print(f'Current announcement text: {self.current.text}')
    def print_ann_static(self):
        print(f'Current anouncment static: {self.current.static}')

