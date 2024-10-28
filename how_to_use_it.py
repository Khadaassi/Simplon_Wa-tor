from PygameWrapper import PygameWrapper
from UserImage import UserImage

wrapper = PygameWrapper()

tab = [ ["~" for _ in range(16)] for _ in range(9) ]
wrapper.set_tab(tab)

x_test_image = 8 -1
y_test_image = 4 -1
tab[y_test_image][x_test_image] = wrapper.shark_image

x_test_image_2 = 3 -1
y_test_image_2 = 1 -1
tab[y_test_image_2][x_test_image_2] = wrapper.fish_image

wrapper.show()


