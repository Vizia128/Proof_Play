NONE = 0
MAIN = 1
ALT = 2
BEAT = 3
ENVIRO = 4
LETTER = 0
DASH = 1


class Words:
    def __init__(self):
        self.line_type = NONE
        self.sub_line_type = NONE
        self.string = ""
        self.scene_number = 1

    def words_to_letters(self, main_name, other_names, logic):
        self.line_type = NONE
        self.sub_line_type = NONE
        self.string = ""
        with open("proof.txt", "r+") as play:
            for line in play.readlines():
                if line.isnumeric():
                    continue
                if "ACT " in line:
                    self.string += line
                    continue
                if "Scene " + str(self.scene_number) in line:
                    self.line_type = NONE
                    self.sub_line_type = NONE
                    self.string += f"\n\n Scene {self.scene_number} \n\n"
                    self.scene_number += 1
                    continue
                for word in line.split():
                    if logic == LETTER:
                        self.string += str(self.letter_logic(main_name, other_names, word))
                    elif logic == DASH:
                        self.string += str(self.dash_logic(main_name, other_names, word))
            play.close()

        with open(f"proof_{main_name}_{logic}.txt", "w") as p:
            p.write(self.string)
            p.close()

    def letter_logic(self, main_name, other_names, word):
        if "Beat" in word:
            return "(b) "
        if "(" in word:
            self.sub_line_type = ENVIRO
            return "(e) "
        if ")" in word:
            self.sub_line_type = NONE
            return ''
        if self.sub_line_type is ENVIRO:
            return ''

        for other_name in other_names:
            if other_name in word and other_name != main_name:
                self.line_type = ALT
                return f"\n {other_name}: "
        if main_name in word:
            self.line_type = MAIN
            return f"\n {main_name}: "

        if self.line_type is MAIN:
            return word[:1] + ' '
        if self.line_type is ALT:
            return word + ' '
        if self.line_type is NONE:
            return ''

    def dash_logic(self, main_name, other_names, word):
        if "Beat" in word:
            return ''
        if "(" in word:
            self.sub_line_type = ENVIRO
            return ''
        if ")" in word:
            self.sub_line_type = NONE
            return ''
        if self.sub_line_type is ENVIRO:
            return ''

        for other_name in other_names:
            if other_name in word and other_name != main_name:
                self.line_type = ALT
                return f"\n {other_name}: "
        if main_name in word:
            self.line_type = MAIN
            return f"\n {main_name}: "

        if self.line_type is MAIN:
            return '- '
        if self.line_type is ALT:
            return word + ' '
        if self.line_type is NONE:
            return ''


if __name__ == "__main__":
    names = ["ORIGINAL_SCRIPT", "ROBERT", "CATHERINE", "HAL", "CLAIRE"]
    Proof = Words()
    for name in names:
        Proof.words_to_letters(name, names, LETTER)
        Proof.words_to_letters(name, names, DASH)

