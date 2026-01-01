from itertools import *

def find_divisors(n, all=True):
    if n == 0:
        return []

    n = abs(n)
    divs = [1, n]
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            divs.append(i)
            if i != n//i: divs.append(round(n // i))

    if all: return divs + [-d for d in divs]
    else: return divs

def is_good_point(v, n):
    v = abs(v)

    if v == 0 : return False
    if v == 1 : return True

    c = 2
    for i in range(2, int(v ** 0.5) + 1):
        if v % i == 0:
            c += 2
            if c > n: break

    return c <= n

def check_constant_term_division(x, y, const):
    numerator = 0
    denominator = 1
    n = len(x)

    # вычисляем все знаменатели
    denominators = []
    for i in range(n):
        d = 1
        for j in range(n):
            if i != j:
                d *= (x[i] - x[j])
        denominators.append(d)

    # собираем общий знаменатель для всех дробей
    for d in denominators: denominator *= d

    # собираем числитель
    for i in range(n):
        term_num = y[i]
        for j in range(n):
            if i != j:
                term_num *= (-x[j])
        term_num *= denominator // denominators[i]
        numerator += term_num

    if numerator % denominator != 0: return False

    const_int = numerator // denominator

    if const_int == 0: return False
    if const % const_int != 0: return False

    return True


####################################################################################

def generate_combinations(points, n, k):
    result = []

    # выбираем все возможные комбинации k массивов
    for selected_indexes in combinations(range(n), k):
        selected_points_arrays = [points[i] for i in selected_indexes]

        # генерируем декартово произведение выбранных массивов
        combs = list(product(*selected_points_arrays))
        result.extend(combs)

    return result


def get_all_combinations(points, n): # n - максимальная степень искомого полинома разложения
    result = {}

    # k - количество точек в комбинации, количество точек = степень искомого полинома
    for k in range(2, n+1):
        result[k] = generate_combinations(points, n, k)

    return result

####################################################################################

def is_polynomial(p):
    f = True
    if p[-1] == 0 or len(p) == 1: f=False
    return f

def get_polynomial_value(p, x):
    result = 0
    for i in range(len(p)): result += p[i] * x ** i
    return result

def multiply_polynomials(p, q):
    result = []

    for i in range(len(p)):
        for j in range(len(q)):
            if len(result) - 1 < i + j:
                result.append(p[i] * q[j])
            else:
                result[i + j] += p[i] * q[j]

    return result

def divide_polynomials(p, q):
    result = []

    pi = len(p) - 1
    qi = len(q) - 1
    while pi >= qi:
        multi = p[pi] / q[qi]
        result.insert(0, multi)
        for i, j in zip(range(pi, pi - qi - 1, -1), range(qi, -1, -1)):
            p[i] -= multi * q[j]
        pi -= 1

    if len(result) == 0: result = [0]
    return result, p

def print_polynomial_ver_3(p):
    if not p:
        return "0"

    result = ""
    for i in range(len(p) - 1, -1, -1):
        if p[i] != 0:
            k = str(abs(p[i]))
            if abs(p[i]) == 1 and i != 0:
                k = ''

            if i == 0:
                result += k
            elif i == 1:
                result += k + 'x'
            else:
                result += k + 'x^' + str(i)

            if i != 0:
                if i > 0:
                    # Проверяем следующий коэффициент
                    next_nonzero = False
                    for j in range(i - 1, -1, -1):
                        if p[j] != 0:
                            next_nonzero = True
                            if p[j] > 0:
                                result += ' + '
                            else:
                                result += ' - '
                            break
    if result == "":
        result = "0"

    return result


####################################################################################

def get_coefficients(x, y):
    k = []
    for i in range(0, len(x)):
        temp = y[i]
        for j in range(0, len(x)):
            if i != j:
                temp *= (1 / (x[i] - x[j]))
        k.append(temp)
    return k

count_lagrange = 0

def get_lagrange_polynomial(x, y, n, initial):
    global count_lagrange
    count_lagrange += 1

    monomials = []
    for i in range(0, len(x)):
        monomials.append([-x[i], 1])

    multipliers_order = combinations(monomials, n-1)

    l = []
    for m in multipliers_order:
        v = m[0]
        if n > 2:
            for j in range(1, len(m)):
                v = multiply_polynomials(v, m[j])
        l.insert(0, v)

    k = get_coefficients(x, y)
    answer = [0 for i in range(n)]
    for i in range(len(l)):
        for j in range(n):
            answer[j] += l[i][j] * k[i]

    # проверка
    check = True
    if is_polynomial(answer):
        for aa in answer:
            if aa != int(aa):
                check = False
                break
    else:
        check = False

    if check:
        initial_copy = initial.copy()
        p, q = divide_polynomials(initial_copy, answer)

        f = True
        # 1
        for qq in q:
            if qq != 0:
                f = False
                break

        #2
        for pp in p:
            if pp != int(pp):
                f = False
                break

        if f: return answer
    return [0]

####################################################################################

def kronecker_factorization_ver_3(polynomial):
    global count_lagrange
    count_lagrange = 0

    original_poly = polynomial.copy()
    factorization = []

    while is_polynomial(polynomial):

        # m + 1
        n = len(polynomial)-1
        m = n//2 + 1

        # находим лучшие точки, массив a
        a = []
        values = []

        mm = 0
        start_next_rotation = False

        start_a = find_divisors(polynomial[0])
        for a_i in start_a:
            if a_i not in a:
                v = get_polynomial_value(polynomial, a_i)
                if v == 0:
                    root = [-a_i, 1]
                    factorization.append(root)
                    polynomial, q = divide_polynomials(polynomial, root)
                    start_next_rotation = True
                    break
                elif is_good_point(v, n):
                    a.append(a_i)
                    values.append(v)
                    mm += 1
                    if mm >= m: break

        if start_next_rotation: continue

        a_i = 0
        while mm < m:
            if a_i not in a:
                v = get_polynomial_value(polynomial, a_i)
                if v == 0:
                    root = [-a_i, 1]
                    factorization.append(root)
                    polynomial, q = divide_polynomials(polynomial, root)
                    start_next_rotation = True
                    break
                elif is_good_point(v, n):
                    a.append(a_i)
                    values.append(v)
                    mm += 1
                    if mm >= m: break

            if -a_i not in a and a_i != 0:
                v_negative = get_polynomial_value(polynomial, -a_i)
                if v_negative == 0:
                    root = [a_i, 1]
                    factorization.append(root)
                    polynomial, q = divide_polynomials(polynomial, root)
                    start_next_rotation = True
                    break
                elif is_good_point(v_negative, n):
                    a.append(-a_i)
                    values.append(v_negative)
                    mm += 1
                    if mm >= m: break

            a_i += 1

        if start_next_rotation: continue

        # делители для каждого значения
        divs = [find_divisors(v) for v in values]

        # трехмерный массив точек
        points = [[] for i in range(len(divs))]

        for i in range(len(divs)):
            for j in range(len(divs[i])):
                temp = [a[i], divs[i][j]]
                points[i].append(temp)

        # все декартовы произведения
        combs_in_dict = get_all_combinations(points, m)
        combs = [combs_in_dict[i][j] for i in combs_in_dict.keys() for j in range(len(combs_in_dict[i]))]

        found = False
        checked_combs = {}
        for i in range(len(combs)):
            x = []
            y = []

            for point in combs[i]:
                x.append(point[0])
                y.append(point[1])

            x_tuple = tuple(x)
            if x_tuple not in checked_combs.keys(): checked_combs[x_tuple] = []

            if y not in checked_combs[x_tuple]:
                checked_combs[x_tuple].append(y)
                y_negative = [-yy for yy in y]
                checked_combs[x_tuple].append(y_negative)

                l = sum(get_coefficients(x, y))
                if abs(l - round(l)) > 1e-10: # проверка 1, целая ли сумма коэффициентов? понимание: get_coefficients дает старший коэффициент интерполяционного многочлена
                    continue

                l_int = round(l)
                if l_int == 0 or polynomial[-1] % l_int != 0: # истинная проверка 1
                    continue

                if not check_constant_term_division(x, y, polynomial[0]): # проверка 2, делится ли свободный член исходного полинома на свободный член интерполяционного многочлена
                    continue

                p = get_lagrange_polynomial(x, y, len(combs[i]), polynomial)
                if is_polynomial(p):
                    found = True
                    p = [round(pp) for pp in p]
                    if p[-1] < 0: p = [-1 * round(pp) for pp in p]
                    factorization.append(p)
                    polynomial, q = divide_polynomials(polynomial, p)
                    break

        # этот многочлен неприводим
        if not found:
            p = polynomial.copy()
            p = [round(pp) for pp in p]
            factorization.append(p)
            polynomial = [0]

    return {
        "original": original_poly,
        "factorization": factorization,
        "lagrange_count": count_lagrange
    }