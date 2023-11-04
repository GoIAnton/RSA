from random import choice
from tkinter import (NW, BooleanVar, Button, Entry, Label, StringVar, Tk,
                     messagebox, ttk)

ALPHABET = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
ALPH_TO_NUM = {letter: i for i, letter in enumerate(ALPHABET)}
NUM_TO_ALPH = {v: k for k, v in ALPH_TO_NUM.items()}


def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)


def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        return False
    else:
        return x % m


def gen_primes(limit):
    d = {}
    q = 2
    while q <= limit:  # Максимальное простое число
        if q not in d:
            yield q
            d[q * q] = [q]
        else:
            for p in d[q]:
                d.setdefault(p + q, []).append(p)
            del d[q]
        q += 1


def get_keys():
    if AUTO_KEYS.get():
        primes = [i for i in gen_primes(37)]
        p = choice(primes)
        q = choice(primes)
    else:
        p = enter_p.get()
        q = enter_q.get()
        if not p or not q:
            KEYS.set('Нет p и/или q')
            return
        p = int(p)
        q = int(q)
        primes = [i for i in gen_primes(37)]
    m = p * q
    n = (p - 1) * (q - 1)
    e = choice(primes)
    while(n == e):
        e = choice(primes)
    d = modinv(e, n)
    if d:
        KEYS.set(f'm = {m}, e = {e}, d = {d}')
    else:
        get_keys()


def alg_rsa():
    e_d = enter_e_or_d.get()
    m = enter_m.get()
    if not e_d or not m:
        messagebox.showinfo('Ошибка', 'Нет e/d и/или q')
        return
    e_d = int(e_d)
    m = int(m)
    if ENCRYPTION.get():
        x = []
        text = enter.get()
        text = text.lower()
        for i in text:
            if i not in ALPHABET:
                messagebox.showinfo('Ошибка', 'Введите слово на русском')
                return
        len_text = len(text)
        for i in range(len_text):
            x.append(ALPH_TO_NUM[text[i]])
        for i in range(len_text):
            x[i] = str(x[i]**e_d % m)
        x = ' '.join(x)
        RESULT.set(x)
    else:
        x = enter.get()
        x = x.split()
        for i in x:
            if not i.isdigit() and not 1 == ' ':
                messagebox.showinfo('Ошибка', 'Введите числа через пробел')
                return
        x = [int(i) for i in x]
        len_x = len(x)
        for i in range(len_x):
            x[i] = int(x[i]**e_d % m)
        for i in range(len_x):
            x[i] = NUM_TO_ALPH[x[i]]
        x = ''.join(x)
        RESULT.set(x)


def switch():
    if AUTO_KEYS.get():
        text_p['state'] = 'disabled'
        enter_p['state'] = 'disabled'
        text_q['state'] = 'disabled'
        enter_q['state'] = 'disabled'
    else:
        text_p['state'] = 'normal'
        enter_p['state'] = 'normal'
        text_q['state'] = 'normal'
        enter_q['state'] = 'normal'


def switch_e_or_d():
    if ENCRYPTION.get():
        E_OR_D.set(E)
    else:
        E_OR_D.set(D)


window = Tk()
window.title('RSA')
window.geometry('400x600')

ENCRYPTION = BooleanVar(value=True)
AUTO_KEYS = BooleanVar(value=True)
POSITION = {'padx': 6, 'pady': 6, 'anchor': NW}
E = 'Введите e'
D = 'Введите d'
E_OR_D = StringVar(value=E)
RESULT = StringVar()
KEYS = StringVar()

auto_btn = ttk.Radiobutton(text='Автоматическая генерация ключей', value=True,
                           variable=AUTO_KEYS, command=switch)
auto_btn.pack(**POSITION)
not_auto_btn = ttk.Radiobutton(text='Указать p и q вручную', value=False,
                               variable=AUTO_KEYS, command=switch)
not_auto_btn.pack(**POSITION)
text_p = Label(state='disabled', text='Введите p:')
text_p.pack(**POSITION)
enter_p = Entry(state='disabled')
enter_p.pack(**POSITION)
text_q = Label(state='disabled', text='Введите q:')
text_q.pack(**POSITION)
enter_q = Entry(state='disabled')
enter_q.pack(**POSITION)
gt_keys = Button(
    text='Получить ключи\n(m, e, d)',
    command=get_keys
)
gt_keys.pack()
show_keys = Entry(text=KEYS, state='readonly')
show_keys.pack(**POSITION)

encryption_btn = ttk.Radiobutton(text='Шифрование', value=True,
                                 variable=ENCRYPTION, command=switch_e_or_d)
encryption_btn.pack(**POSITION)
decryption_btn = ttk.Radiobutton(text='Дешифрация', value=False,
                                 variable=ENCRYPTION, command=switch_e_or_d)
decryption_btn.pack(**POSITION)
text = Label(text='Введите слово или числа через пробел')
text.pack(**POSITION)
enter = Entry()
enter.pack(**POSITION)
text_m = Label(text='Введите m:')
text_m.pack(**POSITION)
enter_m = Entry()
enter_m.pack(**POSITION)
text_e_or_d = Label(textvariable=E_OR_D)
text_e_or_d.pack(**POSITION)
enter_e_or_d = Entry()
enter_e_or_d.pack(**POSITION)

show_keys = Button(
    text='Выполнить',
    command=alg_rsa
)
show_keys.pack()

result = Entry(text=RESULT, state='readonly')
result.pack(**POSITION)

window.mainloop()

