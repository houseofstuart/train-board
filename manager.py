import pandas as pd, numpy as np

class Manager:
    def __init__(self, board_array):
        self.board_array = board_array
        self.letters = self.get_csv('resources/letters.csv')
        self.current = None
        self.text_array = None
        self.clock = 0

    def tick(self):
        # Update the board - all binary data in self.text_array
        self.clock += 1
        self.board_array = np.zeros((70, 15)) #start from column 70 and move to 0 

        text_start = (70 - self.clock)
        if text_start < -(len(self.text_array)):
            return #moved all the way left
        i = 0
        for column in range(text_start, text_start+len(self.text_array)):
            if column >= 70:
                break
            self.board_array[column][-(1+len(self.text_array[i])):-1] = self.text_array[i]
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
        total_length = 0
        for letter in text:
            letter_data = self.ret_let_data(letter)
            text_array.append(letter_data)
            total_length += letter_data["width"]
            for y in range(letter_data['width']):
                sub_binary = []
                for x in range(len(letter_data['binary'])):
                    if x % letter_data['width'] == y:
                        sub_binary.append(letter_data['binary'][x])
                text_binary_array.append(sub_binary)
            text_binary_array.append(self.ret_let_data('letter_gap')['binary'])
        self.text_array = text_binary_array

                

        



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

    def set_announcement(self, announcement):
        self.current = announcement
    
    #Print functions
    def print_ann_text(self):
        print(f'Current announcement text: {self.current.text}')
    def print_ann_static(self):
        print(f'Current anouncment static: {self.current.static}')

