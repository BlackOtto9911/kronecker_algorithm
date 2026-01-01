# kronecker_algorithm_ver_5.py
# ver 5.0

from itertools import *
from math import *

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
    for i in range(1, int(v ** 0.5) + 1):
        if v % i == 0:
            c += 1
            if i != v // i:
                c += 1
        if c > n:
            return False

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


def eisenstein_criterion(polynomial):
    if len(polynomial) < 2:
        return False

    a0 = abs(polynomial[0])
    if a0 == 0:
        return False

    for p in range(2, a0 + 1):
        is_prime = True
        for i in range(2, int(p ** 0.5) + 1):
            if p % i == 0:
                is_prime = False
                break

        if not is_prime:
            continue

        condition1 = True
        for i in range(len(polynomial) - 1):
            if polynomial[i] % p != 0:
                condition1 = False
                break

        if not condition1:
            continue

        condition2 = (polynomial[-1] % p != 0)
        if not condition2:
            continue

        condition3 = (polynomial[0] % (p * p) != 0)

        if condition1 and condition2 and condition3:
            return True

    return False

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


def print_polynomial_ver_4(p):
    if not p:
        return "0"

    result = ""
    for i in range(len(p) - 1, -1, -1):
        if p[i] != 0:
            k = str(abs(p[i]))
            if abs(p[i]) == 1 and i != 0:
                k = ''

            if i == 0: result += k
            elif i == 1: result += k + 'x'
            else: result += k + 'x^' + str(i)

            if i != 0:
                if i > 0:
                    # Проверяем следующий коэффициент
                    next_nonzero = False
                    for j in range(i - 1, -1, -1):
                        if p[j] != 0:
                            next_nonzero = True
                            if p[j] > 0: result += ' + '
                            else: result += ' - '
                            break
    if result == "":
        result = "0"

    return result

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

    if len(set(x)) != len(x):
        return [0]

    monomials = []
    for i in range(len(x)):
        monomials.append([-x[i], 1])

    multipliers_order = combinations(monomials, n - 1)

    l_polys = []
    for m in multipliers_order:
        v = m[0]
        if n > 2:
            for j in range(1, len(m)):
                v = multiply_polynomials(v, m[j])
        l_polys.insert(0, v)

    k = get_coefficients(x, y)
    answer = [0] * n
    for i in range(len(l_polys)):
        for j in range(len(l_polys[i])):
            answer[j] += l_polys[i][j] * k[i]

    # Проверка целостности коэффициентов
    check = True
    if is_polynomial(answer):
        for aa in answer:
            if abs(aa - round(aa)) > 1e-10:
                check = False
                break
    else:
        check = False

    if check:
        answer = [round(coef) for coef in answer]
        initial_copy = initial.copy()
        p, q = divide_polynomials(initial_copy, answer)

        f = True
        for qq in q:
            if abs(qq) > 1e-10:
                f = False
                break

        if f:
            return answer

    return [0]

####################################################################################

def kronecker_factorization_ver_4(polynomial):
    global count_lagrange
    count_lagrange = 0

    original_poly = polynomial.copy()
    factorization = []

    const_multiplier = gcd(*polynomial)
    polynomial = [k // const_multiplier for k in polynomial]

    while is_polynomial(polynomial):

        # m + 1
        n = len(polynomial) - 1
        m = n // 2 + 1

        # находим лучшие точки, массив a
        a = []
        values = []

        mm = 0
        start_next_rotation = False

        start_a = find_divisors(polynomial[0])
        if len(start_a) != 0:
            for a_i in start_a:
                if a_i not in a:
                    v = get_polynomial_value(polynomial, a_i)
                    if v == 0:
                        root = [-a_i, 1]
                        factorization.append(root)
                        polynomial, q = divide_polynomials(polynomial, root)
                        polynomial = [round(pp) for pp in polynomial]
                        start_next_rotation = True
                        break
                    elif is_good_point(v, n):
                        a.append(a_i)
                        values.append(v)
                        mm += 1
                        if mm >= m: break

        if start_next_rotation: continue

        change_points_choice = False
        a_i = 0
        while mm < m:
            if a_i not in a:
                v = get_polynomial_value(polynomial, a_i)
                if v == 0:
                    root = [-a_i, 1]
                    factorization.append(root)
                    polynomial, q = divide_polynomials(polynomial, root)
                    polynomial = [round(pp) for pp in polynomial]
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
                    polynomial = [round(pp) for pp in polynomial]
                    start_next_rotation = True
                    break
                elif is_good_point(v_negative, n):
                    a.append(-a_i)
                    values.append(v_negative)
                    mm += 1
                    if mm >= m: break

            a_i += 1
            if a_i > n * 2 + 100:
                change_points_choice = True
                break

        if change_points_choice:
            mm = len(a)
            a_i = 0
            while mm < m:
                if a_i not in a:
                    v = get_polynomial_value(polynomial, a_i)
                    a.append(a_i)
                    values.append(v)
                    mm += 1
                    if mm >= m: break
                if -a_i not in a:
                    v_negative = get_polynomial_value(polynomial, -a_i)
                    a.append(-a_i)
                    values.append(v_negative)
                    mm += 1
                    if mm >= m: break
                a_i += 1

        if start_next_rotation: continue

        # делители для каждого значения
        divs = [find_divisors(v, all=False) for v in values]

        # трехмерный массив точек
        points = [[] for i in range(len(divs))]

        for i in range(len(divs)):
            for j in range(len(divs[i])):
                temp = [a[i], divs[i][j]]
                points[i].append(temp)

        found = False
        for k in range(2, m + 1):
            combs = generate_combinations(points, len(a), k)

            for comb in combs:
                x = [point[0] for point in comb]
                y = [point[1] for point in comb]
                # Проверяем различные комбинации знаков
                signs_combs = list(product([1, -1], repeat=k))
                signs_combs = signs_combs[:len(signs_combs) // 2]
                for signs in signs_combs:
                    y_signed = [y[i] * signs[i] for i in range(k)]

                    l = sum(get_coefficients(x, y_signed))
                    if abs(l - round(l)) > 1e-10:
                        continue

                    l_int = round(l)
                    if l_int == 0 or polynomial[-1] % l_int != 0:
                        continue

                    if not check_constant_term_division(x, y_signed, polynomial[0]):
                        continue

                    p = get_lagrange_polynomial(x, y_signed, k, polynomial)
                    if is_polynomial(p):
                        found = True
                        if p[-1] < 0:
                            p = [-1 * round(pp) for pp in p]
                        else:
                            p = [round(pp) for pp in p]
                        factorization.append(p)
                        polynomial, q = divide_polynomials(polynomial, p)
                        polynomial = [round(pp) for pp in polynomial]
                        break
                if found: break
            if found: break

        # этот многочлен неприводим
        if not found:
            p = polynomial.copy()
            p = [round(pp) for pp in p]
            factorization.append(p)
            polynomial = [0]
    if len(factorization) != 0: factorization[0] = [k * const_multiplier for k in factorization[0]]

    return {
        "original": original_poly,
        "factorization": factorization,
        "lagrange_count": count_lagrange
    }