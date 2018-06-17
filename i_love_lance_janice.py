#!/usr/bin/python

def answer(s):
    key_list = [chr(i) for i in range(ord('a'), ord('z') + 1)]
    value_list = [chr(j) for j in range(ord('z'), ord('a') - 1, -1)]
    my_dict = dict(list(zip(key_list, value_list)))
    decrypt = []

    for character in s:
        decrypt.append(my_dict[character] if character in my_dict else character)
    return (''.join(decrypt))


test_1 = "wrw blf hvv ozhg mrtsg'h vkrhlwv?"
# (string1) "did you see last night's episode?"
test_2 = "Yvzs! I xzm'g yvorvev Lzmxv olhg srh qly zg gsv xlolmb!!"
# (string2) "Yeah! I can't believe Lance lost his job at the colony!!"

print(answer(test_1))
print(answer(test_2))
