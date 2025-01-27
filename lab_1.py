import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.family'] = 'Times New Roman' # Шрифт для всех подписей

# Определение символьных переменных
A = 10 # Амплитуда сигнала, В
A_0 = 10 # Начальная амплитуда
f = 6 # Частота сигнала, Гц
f_d = 18 # Частота дискретизации, Гц
b = 4 # Разрядность АЦП
phi = np.pi/4 #
t_min = 14 # Начальное время моделирования
t_max = 30 # Конечное время моделирования

# Моделирование аналогового сигнала
x = np.linspace(14, 30, 100)
x_a = A_0 + A * np.cos(2*np.pi*f*x + phi) # Формирование значений
plt.plot(x, x_a, color='blue')
plt.xlim (t_min, t_max)
plt.ylim (A_0-A, A_0+A)
#plt.xticks(np.linspace(t_min,t_max, 17))
#plt.yticks(np.linspace(A_0-A, A+A_0, 17))

plt.xlabel('Время, t, с') #Подпись для оси х
plt.ylabel('Сигнал, x(t), В') #Подпись для оси y
plt.title('Аналоговый сигнал') #Название
plt.show()

# Моделирование дискретного сигнала
t_d = np.linspace(t_min,t_max, (t_max-t_min)*f_d) # Формирование значений области определения
x_d = A_0 + A * np.cos(2*np.pi*f*t_d + phi) # Формирование значений
plt.plot(t_d, x_d, color = 'pink', marker= 'o', markersize = 5, mfc = 'blue', mec = 'green')
plt.xticks(np.linspace(t_min,t_max, 15)) # Задание значений и шага на ОХ
plt.yticks(np.linspace(A_0-A, A+A_0, 15)) # Задание значений и шага на ОУ

plt.xlabel('Дискретное время, n$T_{д}$, с') #Подпись для оси х
plt.ylabel('Cигнал x(n$T_{д}$), В') #Подпись для оси y
plt.title('Дискретный сигнал') #Название
plt.grid() # Сетка графика
plt.show()


# Моделирование квантового сигнала
N = 2**b # Количество уровней квантования
q = 2*A/(N-1) # Шаг квантования
levels = np.arange(A_0-A+q/2, A_0+A+q/2, q)
codebook = np.arange(A_0-A, A_0+A+q, q)
x_q = []

for i in range(len(x_d)):
    for j in range(len(levels)):
        if x_d[i] >= codebook[j] and x_d[i] < codebook[j+1]:
            x_q.append(levels[j])

plt.plot(t_d, x_q, marker = 'o', markersize = 5, mfc = 'blue', mec = 'green')
plt.xticks(np.linspace(t_min, t_max, 15))
plt.yticks(levels)
plt.xlabel('Дискретное время, n$T_{д}$, с') #Подпись для оси х
plt.ylabel('Cигнал x(n$T_{д}$ ), В') #Подпись для оси y
plt.title('Квантованный по уровню сигнал') # Название
plt.grid() # Сетка графика
plt.show()

# Моделирование цифрового сигнала
codes = np.arange(-N/2+1, N/2) # Массив кодированных значений
codescomp = []
t = []
d = []

for i in range(len(codes)):    #Перевод в двоичную СС красиво
    t.append(bin(int(codes[i])))
    d.append(t[i].replace("0b", ""))
    if int(d[i]) >= 0:
        codescomp.append('0')   # Формирование знакового разряда
    else:
        codescomp.append('1')

for i in range(len(codescomp)//2,len(codescomp)):  # Формирование разряда числа
    d[i] = d[i].rjust(3) # b = 4
    codescomp[i] += d[i].replace(" ", "0")

for i in range(0, len(codescomp)//2): # То же, для отрицательных чисел в обратном коде
    codescomp[i] += codescomp[i+len(codescomp)//2][1:]

x_a = [] # Цифровое значение
for i in range(len(x_d)):
    for j in range(len(levels)):
        if x_d[i] >= codebook[j] and x_d[i] < codebook[j+1]:
            x_a.append(codes[j])

fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax1.plot(t_d, x_a, color = 'pink', marker= 'o', markersize = 5, mfc = 'blue', mec = 'green')
ax2.plot(t_d, x_a, color = 'pink', marker= 'o', markersize = 5, mfc = 'blue', mec = 'green')
ax1.set_yticks(codes, codescomp)
ax2.set_yticks(codes)
plt.xticks(np.linspace(t_min, t_max, 15))
ax1.set_xlabel('Дискретное время, n$Т_{д}$, с') #Подпись для оси х
ax1.set_ylabel('Сигнал x(n$T_{д}$), обратный код')
ax2.set_ylabel('Сигнал x(n$T_{д}$), код')
plt.title('Цифровой сигнал в обратном коде') # Название
ax1.grid (axis='y') # Сетка графиков
ax1.grid (axis='x')
plt.show()

# Вычисление погрешности цифрового сигнала
ex = []
for i in range(len(t_d)):
    ex.append(x_q[i] - (list(x_d))[i])
plt.plot(t_d, ex, 'r-', marker = 'o', markersize = 5, mfc = 'orange', mec = 'red')
plt.xlabel('Дискретное время, n$T_{д}$, с') #Подпись для оси х
plt.ylabel('Погрешность, e(n$T_{д}$ ), В') #Подпись для оси y
plt.title('Абсолютная погрешность квантования сигнала') # Название
plt.show()

# Формирование гистограммы статистического распределения погрешности квантования сигнала
D = (t_max-t_min)/N # Шаг квантования
f_e = 1/D # Плотность вероятности
nBars = 8
edges = np.linspace(-A/(N-1),A/(N-1),nBars+1)

number = list(np.zeros(nBars)) # Частота встречающихся значений погрешности
for i in range(nBars):
    number[i] = int(number[i])

for i in range(len(ex)):
    for j in range(nBars):
        if ex[i] >= edges[j] and ex[i] <= edges[j+1]:
            number[j] += 1
w = edges[1] - edges[0]
rel_freq = []
for i in range(len(number)):
    rel_freq.append(number[i]/(len(ex)*w))

teor = []
for i in range(nBars):
    teor.append(1/((t_d[1]-t_d[0])*3*nBars))


lin = np.linspace(min(ex),max(ex), 8)
plt.bar(lin, rel_freq, label='Экспериментальная', width=0.2, alpha=0.5, edgecolor= 'purple')
plt.xticks(edges)
plt.xlabel('Абсолютная погрешность, e(n), В') #Подпись для оси х
plt.ylabel('Плотность вероятности, Ф(е), 1/В') #Подпись для оси y
plt.title('Гистограмма статистического распределения погрешности квантования сигнала') # Название
plt.bar(lin, teor, label='Теоретическая', width=0.2, alpha=0.5, color='green', edgecolor= 'black')
plt.legend()
plt.show()

