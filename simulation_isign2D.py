import math as m
import random
from PIL import Image, ImageDraw
from matplotlib import pyplot as plt
from tqdm import trange,tqdm
import imageio
import time
import os






def process_data():
    time.sleep(0.02)

def del_files_from_dir(PATH=r'C:\Users\pawel\OneDrive\Dokumenty\2 stopien\2 semestr\PwZN\2_Lab_symulacja\etapy\\'):
    # default PATH - PATH WITH IMAGES
    files = os.listdir(PATH)
    for f in files:
        os.remove(PATH + '\\' + f)


def index_exists(table, i, j):  # usefull method for checking if index (i,j) exist
    try:
        table[i][j]
    except (ValueError, IndexError):
        return False
    else:
        return True


class simulation:
    def __init__(self):
        self.object = object

    def check_possibility(self, beta, energy):
        possibility = m.exp(-beta * energy)
        if abs(possibility) < random.random():
            return True
        else:
            return False

    def list_of_spins(self, size, spin_density):
        element = 0
        spins = [[-1 for x in range(size)] for y in range(size)]  # declaring '0' array size x size

        if spin_density < 1:
            el = random.sample(range(0, size * size - 1), int(spin_density * size * size))
            for rand_element in el:
                X = int(rand_element / size % size)
                Y = rand_element % size
                spins[X][Y] = 1
        else:
            pass
        return spins

    def change_spin_hamiltonian(self, size, spins, spin_density, i, j, J, B):
        e0 = ob.count_Hamiltionian(size, spins, J, B)
        spins = ob.change_spin(size, spin_density, i, j)
        e1 = ob.count_Hamiltionian(size, spins, J, B)
        if e1 - e0 < 0:
            pass
        else:
            if ob.check_possibility(B, e1 - e0) is False:
                spins = ob.change_spin(size, spin_density, i, j)
        return spins

    def change_spin(self, size, spin_density, i, j, ):
        spins = ob.list_of_spins(size, spin_density)
        if spins[i][j] == 1:
            spins[i][j] = -1
        else:
            spins[i][j] = 1
        return spins

    def make_table(self, size,
                   spins):  # dodać parametr spins - spiny defaultowe/zmianowe - v2 potem usuwam v1
        size_of_screen = 2000  # 2000 x 2000 px size of our screen
        background = Image.new('RGB', (size_of_screen, size_of_screen), (0, 200, 145))
        spin_size = size_of_screen / size
        for i in range(0, size):
            for j in range(0, size):
                rec = ImageDraw.Draw(background)
                if spins[i][j] == 1:
                    rec.rectangle([(i * spin_size, j * spin_size), ((i + 1) * spin_size, (j + 1) * spin_size)],
                                  fill='black',
                                  outline='yellow')
                else:
                    rec.rectangle([(i * spin_size, j * spin_size), ((i + 1) * spin_size, (j + 1) * spin_size)],
                                  fill='white',
                                  outline='yellow')
        plt.imshow(background)
        # plt.show()
        img = background
        return img

    def count_magnetization(self, size, spins, spins_density):
        sum_of_spins = 0  # variable to save sum
        # spins = ob.list_of_spins(size, spins_density)
        for i in range(0, size):
            for j in range(0, size):
                sum_of_spins += spins[i][j]
        return sum_of_spins / size

    def simulation_steps(self, number_of_steps, size, spin_density, J, B, name_of_gif=None,
                         name_of_image=None, name_of_file=None):

        imgs = []
        it = 0
        ob.make_table(size, ob.list_of_spins(size, spin_density))
        spins = ob.list_of_spins(size, spin_density)
        del_files_from_dir()  # in case of diffrent path,path is needed
        path = r'C:\Users\pawel\OneDrive\Dokumenty\2 stopien\2 semestr\PwZN\2_Lab_symulacja\etapy\\'
        if name_of_file is not None:
            f = open(name_of_file + '.txt', 'w')
        else:
            print('FILE NOT FOUND')
        # for step in trange(0, number_of_steps):
        #     time.sleep(0.0001)
        for step in tqdm (range(number_of_steps),desc='Steps',colour='green'):
            time.sleep(0.001)
            for el in tqdm(range(size*size),desc='changed spins',colour='white'):
                time.sleep(0.001)
                i = random.randint(0, size - 1)
                j = random.randint(0, size - 1)
                spins = ob.change_spin_hamiltonian(size, spins, spin_density, i, j, J, B)
                # imgs.append(ob.make_table(size, spins))
                img = ob.make_table(size, spins)
            try:
                f.write(f'{step}: {ob.count_magnetization(size, spins, spin_density)}\n')
            except UnboundLocalError:
                pass
            if name_of_image is None:
                pass
            else:
                img.save(path + name_of_image + str(it) + '.jpg')
                it += 1
            imgs.append(ob.make_table(size, spins))
        if name_of_gif is None:
            pass
        else:
            imageio.mimsave(name_of_gif + '.gif', imgs, fps=size)
        f.close()

    def count_Hamiltionian(self, size, spins, J, B):
        sum_of_spins = 0
        for i in range(0, size):
            for j in range(0, size):
                sum_of_spins += spins[i][j]
        term2 = -B * sum_of_spins
        sum_of_spins = 0
        for i in range(0, size):
            for j in range(0, size):
                if index_exists(spins, i, j) and index_exists(spins, i, j + 1):
                    sum_of_spins += spins[i][j] + spins[i][j + 1]
                if index_exists(spins, i, j) and index_exists(spins, i, j - 1):
                    sum_of_spins += spins[i][j] + spins[i][j - 1]
                if index_exists(spins, i, j) and index_exists(spins, i + 1, j):
                    sum_of_spins += spins[i][j] + spins[i + 1][j]
                if index_exists(spins, i, j) and index_exists(spins, i - 1, j):
                    sum_of_spins += spins[i][j] + spins[i - 1][j]
        Hamiltonian = term2 - J * sum_of_spins
        return Hamiltonian


ob = simulation()
ob.simulation_steps(10,4,0.5,1,1,'sim','img','magn2')

